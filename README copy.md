[![Run pytest](https://github.com/EsportDynamics/LLM_Research/actions/workflows/pytest.yml/badge.svg?branch=feat%2FRAN-619-create-automatized-function-tests&event=push)](https://github.com/EsportDynamics/LLM_Research/actions/workflows/pytest.yml)

# LLM Research

This project serves as a coding base for the research of "OpenAI functions saved in vectorDB for token cost reduction". 

## Standard extensions

### VSCode
- AutoDocstring
- BlackFormatter
- Flake8
- Pylint

### Prerequisites
- OS: Linux/macOS/Windows
- Python version: Python 3.11.7
- Packages:
  - pydantic
  - chromadb
  - openai


## Installation
Make sure to install Python with the right version
1. Clone project - ```git clone https://github.com/EsportDynamics/LLM_Research.git```
2. Go to project - ```cd LLM_Research```
3. Crete new venv for the project - ```python3 -m venv {venv_name}```
4. Activate venv - ```source {venv_name}/bin/activate```
5. Install requirements ```pip install -r requirements.txt```

## Run
Run the with the debug button on top of your IDE or by ```python function_holder.py```

## Usage

1. Create a new function by using either the **"shallow" function** or a **"pydantic" defined function**
2. Wrap the function inside the FunctionHolder
3. Insert the FunctionHolder into the vectorDB
4. Create query
5. Check the openai response

Current functionality is defined as follows:
1. If the similarity of 2 queries is not close enough, the closest function to your query will be executed, then the result will be given to GPT-model to form a "human-like" sentence
2. If the similarity of 2 queries is close, the functions are given to GPT-model, where the model picks the best match, and then gives you the output 

### Shallow function
Function without arguments, returning defined output

**Example** 
```python
#Define function
def mass_of_sun() -> str:
    return "The mass of sun is approximately 1,989E30 kg."

#Wrap into FunctionHolder
suns_mass = FunctionHolder(function=mass_of_sun, 
                            description="Return the approximate mass of sun")

#Insert into vectorDB
vectordb.insert_function_into_vectordb(suns_mass)

```

### Pydantic defined function
Function created with Pydantic types

**Example**
```python
#Define Pydantic Input
class FunctionInput(BaseModel):
    name: str = Field(..., description="Name of the planet")

#Define function
def mass_of_planet(params: FunctionInput):
    return f"Approximate mass of {params.name} in kilograms."

#Wrap into FunctionHolder
planets_mass = FunctionHolder(function=mass_of_planet,
                             description="Returns the mass of the planet in kilograms")

#Insert into vectorDB
vectordb.insert_function_into_vectordb(suns_mass)
```
Functions support these argument types:
- **Integer**
- **String**
- **Enum**
- **Array**


Argument types tested together:
| Argument types    | Tested   | 
| :---                          |:----: |
| No params                     | ✅    |
| String                        | ✅    |
| String + integer              | ✅    |
| Enum + string                 | ✅    |
| Enum + array                  | ✅    |




 
