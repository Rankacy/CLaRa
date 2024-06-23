"""MIT License with Commercial Use Clause

Software Copyright (c) 2024 Rankacy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

2. The Software may be used for personal, educational, and non-commercial purposes.

3. Commercial use of the Software is not permitted without prior written
   permission from the copyright holders. For commercial use, please contact us at
   info@rankacy.com

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import json
import os
import inspect
import time

from datetime import datetime
from typing import Callable, Dict, Type
import openai
from dotenv import load_dotenv
from pydantic import BaseModel


from chromadb import Client
from chromadb.utils import embedding_functions
from openai import OpenAI

# from openai import embeddings

from bases import (
    FunctionInput,
    FunctionInputNumber,
    FunctionInputArray,
    FunctionInputTranslation,
    FunctionInputSong,
    FunctionInputSongOR,
    FunctionInputTask,
)

load_dotenv()


def return_params_of_function(function: Callable):
    """Return parameters of given function

    Args:
        function (Callable): Input function in FunctionHolder type

    Returns:
        _type_: returns a JSON schema
    """
    parameters = inspect.signature(function).parameters
    for name, param in parameters.items():
        return param.annotation.schema()


function_registry = {}

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


class FunctionHolder(BaseModel):
    """Wrapper for a function

    Args:
        BaseModel (_type_): Function and desciption

    Returns:
        _type_: returns JSON in OpenAI function call format
    """

    function: Callable
    description: str
    name: str

    parameters: dict

    def __init__(self, function: Callable, description: str) -> None:
        name = function.__name__
        function_call = self._create_function_call(name, description, function)

        super().__init__(
            function=function,
            description=description,
            name=name,
            parameters=function_call,
        )

        function_registry[self.name] = self.to_dict()

    @staticmethod
    def _create_function_call(name: str, description: str, function: Callable):
        new_schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        }

        parameters = return_params_of_function(function)
        print(parameters)
        if parameters is not None:
            for key, value in parameters["properties"].items():
                if (
                    "$defs" in parameters
                ):  # Handle if there`s $defs or definitions since it seems unpredictable
                    for key2, value2 in parameters["$defs"].items():
                        if "anyOf" in value or "allOf" in value:
                            _props = {
                                "type": "string",  # Not sure whether this should be string or actual enum type class name => value2.get("title"),
                                "enum": value2.get("enum"),
                                "description": value.get("description"),
                            }
                        elif value.get("type") == "array":
                            _props = {
                                "type": "array",
                                "description": value["description"],
                                "items": {"type": value["items"]["type"]},
                            }
                        else:
                            _props = {
                                "type": value.get(
                                    "type"
                                ),  # Not sure whether this should be string or actual enum type class name => value2.get("title"),
                                "description": value.get("description"),
                            }
                elif "items" in value:
                    # Type is array
                    _props = {
                        "type": "array",
                        "description": value["description"],
                        "items": {"type": value["items"]["type"]},
                    }
                else:
                    # Type is basic variable of either string on integer
                    _props = {
                        "type": value.get("type"),
                        "description": value.get("description"),
                    }
                new_schema["function"]["parameters"]["properties"][key] = _props

            new_schema["function"]["parameters"]["required"] = parameters["required"]

        print(new_schema)

        return new_schema

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.description}"

    def to_dict(self) -> Dict[str, any]:
        """Convert descriptions, name and parameters to a dictionary

        Returns:
            Dict[str, any]: Dictionary representation of the function holder
        """
        return {
            "description": self.description,
            "name": self.name,
            "parameters": self.parameters,
        }


class InitVectorDB:
    """Initializes the VectorDB and OpenAI API"""

    def __init__(self, collection_name: str = "test_collection") -> None:
        self.client = Client()
        self.collection = self.client.create_collection(collection_name)
        self.openai = OpenAI()
        self.embedding_func = embedding_functions.DefaultEmbeddingFunction()

    def insert_function_into_vectordb(self, function_holder: FunctionHolder):
        """Creates embedding from the description then saves it into the VectorDB

        Args:
            function_holder (FunctionHolder): Take the FunctionHolder object and insert it into the VectorDB
        """
        embedding = self.embedding_func([function_holder.description])
        self.collection.upsert(
            embeddings=embedding,
            ids=[function_holder.name],
            metadatas=[{"function_metadata": function_holder.name}],
        )

    def query_vectordb(self, query: str, n_results: int = 1):
        """Funtion to query the VectorDB and return the results if any

        Args:
            query (str): Query to look for in the VectorDB
            n_results (int, optional): Number of results to return. Defaults to 1.

        Returns:
            _type_: List of results from the VectorDB
        """

        # Boolean to check whether the query returned only one result
        single_response = False

        query_results = self.collection.query(query_texts=[query], n_results=n_results)

        print(query_results)

        # Redefine logic to return only one query if the distance from the first and second result is too small using statistics
        if (query_results["distances"][0][1] - query_results["distances"][0][0]) > 0.1:
            single_response = True
            query_results = self.collection.query(query_texts=[query], n_results=1)
            return single_response, query_results
        elif n_results == 1:
            single_response = True

        return single_response, query_results

    def execute_function(self, function_name: str, *args, **kwargs):
        """Function to execute the Function from FunctionHolder

        Args:
            function_name (str): Name of the function (get from VectorDB results)

        Returns:
            _type_: Return the return type from the called function
        """
        if function_name in function_registry:
            function_metadata = function_registry[function_name]
            actual_function = globals().get(function_metadata["name"])
            if actual_function:
                return actual_function(*args, **kwargs)
        return None

    def return_openai_query(self, function_name: str):
        """Function to return the OpenAI prompt for the function

        Args:
            function_name (str): Name of the function (get from VectorDB results)

        Returns:
            _type_: OpenAI prompt for the given function
        """
        if function_name in function_registry:
            function_metadata = function_registry[function_name]
            return function_metadata["parameters"]
        return None

    def delete_record(self, function_name: str):
        """Delete a record from ChromaDB by given function name

        Args:
            function_name (str): name of the function you wanna delete
        """
        self.collection.delete(ids=[function_name])


# Example usage
vectordb = InitVectorDB()


def launch_spotify():
    return "Launching spotify"


def weather_today_():
    return "Today will be sunny, with a high of 20 degrees celsius."


def current_time_date():
    now = datetime.now()
    return f"The current time is {now.strftime('%H:%M')} and today's date is {now.strftime('%Y-%m-%d')}."


def _play_song():
    return "Playing Walk n Skank by Macky Gee on spotify.."


def new_task(param: FunctionInputTask):
    return f"Task: {param.text} with {param.priority} is set to {param.date_time}"


def weather_today(param: FunctionInput):
    return f"The weather in {param.city} is currently 20 degrees {param.unit.value}."


def dial_number(param: FunctionInputNumber):
    return f"Calling {param.number}..."


def play_song(params: FunctionInputSong):
    return f"Playing {params.song_name} on spotify.."


def translate_text(param: FunctionInputTranslation):
    return f"Translate '{param.text}' from {param.from_language.value} to {param.to_language.value}."


def grocery_list_items(params: FunctionInputArray):
    return (
        f"I am going to {params.store}, the items in grocery list are: {params.item}."
    )


launches_app = FunctionHolder(launch_spotify, description="Launches a spotify app.")

playing_song_ = FunctionHolder(
    _play_song,
    description="Play a song called Walk n Skank by Macky Gee on spotify",
)

current_time = FunctionHolder(
    current_time_date, description="Returns the current time and date."
)

playing_song = FunctionHolder(play_song, description="Play a song on spotify")

call_number = FunctionHolder(dial_number, description="Call a given number")

create_task = FunctionHolder(
    new_task, description="Create new task with priority and finish date"
)

todays_weather = FunctionHolder(
    weather_today,
    description="Return the weather in given city with the temperature unit",
)

text_translation = FunctionHolder(
    translate_text, description="Translate the text from one language to another"
)

todays_weather_ = FunctionHolder(
    weather_today_,
    description="Returns the weather in given city with the temperature.",
)

grocery_list = FunctionHolder(
    grocery_list_items,
    description="Return the items of groceries that needs to be bought",
)

vectordb.insert_function_into_vectordb(launches_app)
vectordb.insert_function_into_vectordb(current_time)
vectordb.insert_function_into_vectordb(playing_song_)
vectordb.insert_function_into_vectordb(playing_song)
vectordb.insert_function_into_vectordb(call_number)
vectordb.insert_function_into_vectordb(create_task)
vectordb.insert_function_into_vectordb(todays_weather)
vectordb.insert_function_into_vectordb(todays_weather_)
vectordb.insert_function_into_vectordb(text_translation)
vectordb.insert_function_into_vectordb(grocery_list)


def get_response_from_openai(question):
    """Function to get response from OpenAI

    Args:
        question (str): Question to ask the OpenAI

    Returns:
        _type_: message content from OpenAI
    """
    # Query the database
    num_response, query_result = vectordb.query_vectordb(question, n_results=2)

    if query_result["distances"][0][0] > 1:
        prompt = f"You are a personal assistant, please answer me to the question: {question}."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )

        print(response)
        return response.choices[0].message.content

    if num_response is True:
        function_metadata_name = query_result["metadatas"][0][0]["function_metadata"]
        print(function_metadata_name)

        if query_result:
            # check whether it has params or not
            tools = vectordb.return_openai_query(function_metadata_name)
            if not tools["function"]["parameters"]["properties"]:
                result = vectordb.execute_function(function_metadata_name)

                prompt = f"You are a personal assistant, please answer me to the question {question}, extract the information from this {result} and not from anywhere else, and add some more semantics to it aka make it more human-like."

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    # function_call="auto"
                )

                print(response)
                print(response.choices[0].message.content)
                return response.choices[0].message.content
            else:
                messages = []
                messages.append(
                    {
                        "role": "system",
                        "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.",
                    }
                )
                messages.append({"role": "user", "content": question})

                toolkit = []
                toolkit.append(tools)

                print("----------")
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    tools=toolkit,
                    tool_choice={
                        "type": "function",
                        "function": {"name": function_metadata_name},
                    },
                )
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls
                print(response)

                if tool_calls:
                    available_functions = {
                        str(function_metadata_name): globals()[function_metadata_name],
                    }

                    messages.append(response_message)
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_to_call = available_functions[function_name]
                        function_args = json.loads(tool_call.function.arguments)
                        input_types = globals()[
                            return_params_of_function(function_to_call)["title"]
                        ]
                        instance = input_types(**function_args)

                        function_response = function_to_call(instance)
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response,
                            }
                        )

                    second_response = client.chat.completions.create(
                        model="gpt-3.5-turbo", messages=messages
                    )
                    print(second_response)
                    return second_response

    elif num_response is False:
        if query_result:
            tools = []
            available_functions = {}
            for i in range(len(query_result["distances"][0])):
                function_metadata_name = query_result["metadatas"][0][i][
                    "function_metadata"
                ]

                available_functions.update(
                    {
                        str(function_metadata_name): globals()[function_metadata_name],
                    }
                )

                tools.append(vectordb.return_openai_query(function_metadata_name))

            messages = []
            messages.append(
                {
                    "role": "system",
                    "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.",
                }
            )
            messages.append({"role": "user", "content": question})

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=tools,
            )

            # Call the function explicitly if no args are given
            try:
                function_args = (
                    response.choices[0].message.tool_calls[0].function.arguments
                )
                function_name = response.choices[0].message.tool_calls[0].function.name
            except TypeError:
                print(
                    "The agent wanted to know some details about your question, this is not implemented yet therefor it crashed"
                )

            if function_args == "{}":
                result = vectordb.execute_function(function_name)

                prompt = f"You are a personal assistant, please answer me to the question {question}, extract the information from this {result} and not from anywhere else, and add some more semantics to it aka make it more human-like."
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    # function_call="auto"
                )

                print(response)
                print(response.choices[0].message.content)
                return response.choices[0].message.content
            else:
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls

                if tool_calls:
                    messages.append(response_message)
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_to_call = available_functions[function_name]
                        function_args = json.loads(tool_call.function.arguments)
                        input_types = globals()[
                            return_params_of_function(function_to_call)["title"]
                        ]
                        instance = input_types(**function_args)

                        function_response = function_to_call(instance)
                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response,
                            }
                        )

                    second_response = client.chat.completions.create(
                        model="gpt-3.5-turbo", messages=messages
                    )
                    print(second_response)
                    return second_response


start_time = time.time()
# get_response_from_openai("Launch a spotify app please")
# get_response_from_openai("Can you please play Walk n Skank by macky gee on spotify")
# get_response_from_openai("What is the current time and date ?")
get_response_from_openai("What is the weather today ?")
# get_response_from_openai("What is the weather today in Prague in celsius?")
# get_response_from_openai("Can you please create new task: feed dog with high priority for 15:00 today")
# get_response_from_openai("Can you please dial 420696669")
# get_response_from_openai("Can you play Let me hold you by Netsky on spotify please")
# get_response_from_openai("Can you translate hello, how are you from english to spanish ?")
# get_response_from_openai("Im going to Zabka and I need Apples, milk, beer, coffee, bread and ketchup")

end_time = time.time()
print(f"Completion time: {end_time - start_time}")


# Tests
# Some functions are unfortunate and needs to be defined globally :/
def play_song(params: FunctionInputSong):
    return f"Playing {params.song_name} on spotify.."


def play_song_on_repeat(params: FunctionInputSongOR):
    return (
        f"The {params.song_name} will be played {params.repeat_time} times on spotify.."
    )


def query_to_test(question: str, type: Type):
    message = get_response_from_openai(question)
    print(message)
    assert isinstance(message, type), "OpenAI response should be string"


def test_function_no_args():
    def _play_song():
        return f"Playing Walk n Skank by Macky Gee on spotify.."

    playing_song = FunctionHolder(
        _play_song,
        description="Play a song called Walk n Skank by Macky Gee on spotify",
    )
    vectordb.insert_function_into_vectordb(playing_song)

    query_to_test("Can you please play Walk n Skank by Macky gee on spotify", str)

    vectordb.delete_record(playing_song.name)


def test_function_w_args_string():
    playing_song = FunctionHolder(play_song, description="Play a song on spotify")

    vectordb.insert_function_into_vectordb(playing_song)

    query_to_test(
        "Play Walk n Skank by Macky Gee on spotify please",
        openai.types.chat.chat_completion.ChatCompletion,
    )

    vectordb.delete_record(playing_song.name)


def test_function_w_args_string_int():
    playing_song = FunctionHolder(
        play_song_on_repeat,
        description="Play a song on repeat for many times on spotify",
    )

    vectordb.insert_function_into_vectordb(playing_song)

    query_to_test(
        "Play Walk n Skank by Macky Gee on spotify 2 times please",
        openai.types.chat.chat_completion.ChatCompletion,
    )

    vectordb.delete_record(playing_song.name)


def test_function_with_enum_string():
    query_to_test("Translate: Hi, how are you from english to spanish", str)


def test_function_with_enum_array():
    query_to_test(
        "Im going to Zabka and I need Apples, milk, beer, coffee, bread and ketchup",
        str,
    )
