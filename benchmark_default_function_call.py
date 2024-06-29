import json
import time
from datetime import datetime
import string
from openai import OpenAI
from benchmark_default_functions import benchmark_tools


GPT_MODEL = "gpt-3.5-turbo-0125"
client = OpenAI()
tools = benchmark_tools


def launch_spotify():
    return "Launching spotify"


def weather_today_():
    return "Today will be sunny, with a high of 20 degrees celsius."


def current_time_date():
    now = datetime.now()
    return f"The current time is {now.strftime('%H:%M')} and today's date is {now.strftime('%Y-%m-%d')}."


def _play_song():
    return "Playing Walk n Skank by Macky Gee on spotify.."


def new_task(text: string, date_time: int, priority: str):
    return f"Task: {text} with {priority} is set to {date_time}"


def weather_today(city: str, unit: str):
    return f"The weather in {city} is currently 20 degrees {unit}."


def dial_number(dial_number: int):
    return f"Calling {dial_number}..."


def play_song(song_name: string):
    return f"Playing {song_name} on spotify.."


def translate_text(text: str, from_language: str, to_language: str):
    return f"Translate '{text}' from {from_language} to {to_language}."


def grocery_list_items(store: str, item: list):
    return f"I am going to {store}, the items in grocery list are: {item}."


def send_email(to: str, subject: str, message: str):
    return f"Sending email to {to} with subject '{subject}' and message '{message}'."


def set_reminder(message: str, time: str):
    return f"Setting a reminder with message '{message}' at {time}."


def get_news(category: str):
    return f"Fetching the latest news in the {category} category."


def calculate_bmi(weight: float, height: float):
    bmi = weight / (height**2)
    return f"The BMI is {bmi:.2f}."


def convert_currency(amount: float, from_currency: str, to_currency: str):
    # This would require external API call in real scenario
    converted_amount = amount * 1.1  # Dummy conversion rate for illustration
    return f"{amount} {from_currency} is equal to {converted_amount} {to_currency}."


def get_joke():
    return "Why don't scientists trust atoms? Because they make up everything!"


def find_restaurant(cuisine: str, location: str):
    return f"Searching for {cuisine} restaurants in {location}."


def book_flight(
    departure_city: str, arrival_city: str, departure_date: str, return_date: str = None
):
    return f"Booking a flight from {departure_city} to {arrival_city} on {departure_date} with return on {return_date}."


def get_exchange_rate(from_currency: str, to_currency: str):
    # This would require external API call in real scenario
    exchange_rate = 1.1  # Dummy exchange rate for illustration
    return (
        f"The exchange rate from {from_currency} to {to_currency} is {exchange_rate}."
    )


def track_package(tracking_number: str):
    return f"Tracking the package with tracking number {tracking_number}."


def find_movie(title: str):
    return f"Searching for the movie titled '{title}'."


def create_event(title: str, date: str, location: str):
    return f"Creating an event titled '{title}' on {date} at {location}."


def get_quote():
    return "The only way to do great work is to love what you do. - Steve Jobs"


def find_book(title: str = None, author: str = None):
    if title:
        return f"Searching for the book titled '{title}'."
    elif author:
        return f"Searching for books by author '{author}'."
    else:
        return "Please provide a title or author to search for a book."


def set_alarm(time: str):
    return f"Setting an alarm for {time}."


def get_recipe(dish: str):
    return f"Fetching a recipe for {dish}."


def send_sms(to: str, message: str):
    return f"Sending SMS to {to} with message '{message}'."


def get_stock_price(symbol: str):
    # This would require external API call in real scenario
    stock_price = 100.0  # Dummy stock price for illustration
    return f"The current stock price for {symbol} is {stock_price}."


def get_response_from_openai(question: str):
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
        # tool_choice=tool_choice,
    )
    print(response)
    response_message = response.choices[0].message
    # messages.append(assistant_message)
    # print(response_message)

    tool_calls = response_message.tool_calls

    if tool_calls:
        messages.append(response_message)

        available_functions = {
            "weather_today_": weather_today_,
            "_play_song": _play_song,
            "launch_spotify": launch_spotify,
            "current_time_date": current_time_date,
            "play_song": play_song,
            "dial_number": dial_number,
            "new_task": new_task,
            "weather_today": weather_today,
            "translate_text": translate_text,
            "grocery_list_items": grocery_list_items,
            "send_email": send_email,
            "set_reminder": set_reminder,
            "get_news": get_news,
            "calculate_bmi": calculate_bmi,
            "convert_currency": convert_currency,
            "get_joke": get_joke,
            "find_restaurant": find_restaurant,
            "book_flight": book_flight,
            "get_exchange_rate": get_exchange_rate,
            "track_package": track_package,
            "find_movie": find_movie,
            "create_event": create_event,
            "get_quote": get_quote,
            "find_book": find_book,
            "set_alarm": set_alarm,
            "get_recipe": get_recipe,
            "send_sms": send_sms,
            "get_stock_price": get_stock_price,
        }

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            fuction_to_call = available_functions[function_name]
            response_message = fuction_to_call(*list(function_args.values()))

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": response_message,
                }
            )
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        print(second_response)


start_time = time.time()
get_response_from_openai("Launch a spotify app please")
# get_response_from_openai("Can you please play Walk n Skank by macky gee on spotify")
# get_response_from_openai("What is the current time and date ?")
# get_response_from_openai("What is the weather today ?")
# get_response_from_openai("What is the weather today in Prague in celsius?")
# get_response_from_openai("Can you please create new task: feed dog with high priority for 15:00 today")
# get_response_from_openai("Can you please dial 420696669")
# get_response_from_openai("Can you play Let me hold you by Netsky on spotify please")
# get_response_from_openai("Can you translate hello, how are you from english to spanish ?")
# get_response_from_openai("Im going to Zabka and I need Apples, milk, beer, coffee, bread and ketchup")

end_time = time.time()
print(f"Completion time: {end_time - start_time}")
