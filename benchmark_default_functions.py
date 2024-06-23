benchmark_tools = [
    {
        "type": "function",
        "function": {
            "name": "launch_spotify",
            "description": "Launches a spotify app.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "_play_song",
            "description": "Play a song called Walk n Skank by Macky Gee on spotify",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "weather_today_",
            "description": "Returns the weather in given city with the temperature.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "current_time_date",
            "description": "Returns the current time and date.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "play_song",
            "description": "Play a song on spotify",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_name": {
                        "type": "string",
                        "description": "Name of the song you wish to play",
                    }
                },
                "required": ["song_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "dial_number",
            "description": "Call a given number",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {
                        "type": "integer",
                        "description": "Number you wanna call",
                    }
                },
                "required": ["number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "new_task",
            "description": "Create new task with priority and finish date",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Task description"},
                    "date_time": {
                        "type": "integer",
                        "description": "Set date and time till the task needs to be finished",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Priority of task",
                    },
                },
                "required": ["text", "date_time", "priority"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "weather_today",
            "description": "Return the weather in given city with the temperature unit",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City for whom you wanna know the weather",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["Celsius", "Fahrenheit"],
                        "description": "Temperature unit",
                    },
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "translate_text",
            "description": "Translate the text from one language to another",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to translate"},
                    "from_language": {
                        "type": "string",
                        "enum": ["English", "Spanish", "French"],
                        "description": "Language to translate from",
                    },
                    "to_language": {
                        "type": "string",
                        "enum": ["English", "Spanish", "French"],
                        "description": "Language to translate to",
                    },
                },
                "required": ["text", "from_language", "to_language"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grocery_list_items",
            "description": "Return the items of groceries that needs to be bought",
            "parameters": {
                "type": "object",
                "properties": {
                    "store": {
                        "type": "string",
                        "enum": ["Walmart", "Target", "Zabka"],
                        "description": "Name of the store",
                    },
                    "item": {
                        "type": "array",
                        "description": "List of grocery items",
                        "items": {"type": "string"},
                    },
                },
                "required": ["store", "item"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Sends an email to the given address with the specified subject and message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address"},
                    "subject": {
                        "type": "string",
                        "description": "Subject of the email",
                    },
                    "message": {"type": "string", "description": "Body of the email"},
                },
                "required": ["to", "subject", "message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_reminder",
            "description": "Sets a reminder with the given message and time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Reminder message"},
                    "time": {
                        "type": "string",
                        "description": "Time to set the reminder (ISO 8601 format)",
                    },
                },
                "required": ["message", "time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "Returns the latest news headlines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["technology", "sports", "business", "entertainment"],
                        "description": "Category of news",
                    }
                },
                "required": ["category"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_bmi",
            "description": "Calculates the Body Mass Index (BMI) given weight and height.",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight": {"type": "number", "description": "Weight in kilograms"},
                    "height": {"type": "number", "description": "Height in meters"},
                },
                "required": ["weight", "height"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Converts an amount from one currency to another.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Amount to convert"},
                    "from_currency": {
                        "type": "string",
                        "description": "Currency code to convert from",
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "Currency code to convert to",
                    },
                },
                "required": ["amount", "from_currency", "to_currency"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_joke",
            "description": "Returns a random joke.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_restaurant",
            "description": "Finds a restaurant based on the given cuisine and location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cuisine": {
                        "type": "string",
                        "description": "Type of cuisine (e.g., Italian, Chinese)",
                    },
                    "location": {
                        "type": "string",
                        "description": "Location to search for restaurants",
                    },
                },
                "required": ["cuisine", "location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_flight",
            "description": "Books a flight with the given details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure_city": {
                        "type": "string",
                        "description": "City of departure",
                    },
                    "arrival_city": {
                        "type": "string",
                        "description": "City of arrival",
                    },
                    "departure_date": {
                        "type": "string",
                        "description": "Date of departure (ISO 8601 format)",
                    },
                    "return_date": {
                        "type": "string",
                        "description": "Date of return (ISO 8601 format)",
                    },
                },
                "required": ["departure_city", "arrival_city", "departure_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Returns the exchange rate between two currencies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_currency": {
                        "type": "string",
                        "description": "Currency code to convert from",
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "Currency code to convert to",
                    },
                },
                "required": ["from_currency", "to_currency"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "track_package",
            "description": "Tracks a package with the given tracking number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tracking_number": {
                        "type": "string",
                        "description": "Package tracking number",
                    }
                },
                "required": ["tracking_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_movie",
            "description": "Finds a movie based on the given title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the movie"}
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_event",
            "description": "Creates an event with the given details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the event"},
                    "date": {
                        "type": "string",
                        "description": "Date of the event (ISO 8601 format)",
                    },
                    "location": {
                        "type": "string",
                        "description": "Location of the event",
                    },
                },
                "required": ["title", "date", "location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_quote",
            "description": "Returns a random motivational quote.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_book",
            "description": "Finds a book based on the given title or author.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the book"},
                    "author": {"type": "string", "description": "Author of the book"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_alarm",
            "description": "Sets an alarm for the given time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time": {
                        "type": "string",
                        "description": "Time to set the alarm (ISO 8601 format)",
                    }
                },
                "required": ["time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_recipe",
            "description": "Returns a recipe for the given dish.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dish": {"type": "string", "description": "Name of the dish"}
                },
                "required": ["dish"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_sms",
            "description": "Sends an SMS to the given phone number with the specified message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient phone number"},
                    "message": {"type": "string", "description": "Message to send"},
                },
                "required": ["to", "message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Returns the current stock price for the given company symbol.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol of the company",
                    }
                },
                "required": ["symbol"],
            },
        },
    },
]
