# Tools :-
"""
Models can request to call tools that perform tasks such as fetching data from a database, searching the web, or running code. Tools are pairing of:-
1. A schema, including the name of the tool, a description, and/or argument definitions (often a JSON schema)
2. A function or coroutine to execute
"""

import os 
import datetime
import requests
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.tools import tool
from pprint import pprint
load_dotenv()

GROQ_API_KEY= os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    RuntimeError("GROQ_API_KEY is not found in the .env file. Check your configurations again.")
groq_model = init_chat_model("groq:qwen/qwen3-32b")
# response = groq_model.invoke("Where is Bali located?")
# print(response)

OPENWEATHER_API_KEY = os.getenv["WEATHERMAP_API_KEY"]

@tool
def get_weather(location:str)->str:
    """Fetching the weather through the weatherMAP API key"""
    api_key = OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={units}&lang=en"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return display_weather_data(response.json())
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}

def parse_datetime(timestamp:int, timezone_shift:int)->str:
  tz = datetime.timezone(datetime.timedelta(seconds=timezone_shift))
  zone = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).astimezone(tz)
  return zone.strftime("%A-%Y/%b/%d %I:%M:%S %p")

def display_weather_data(weather_data):
    parse_data = {}
    # Temperature Information 
    main_data = weather_data["main"] 
    parse_data.setdefault("Temperature", f"{main_data['temp']}°F")
    parse_data.setdefault("Feels Like", f"{main_data['feels_like']}°F")
    parse_data.setdefault("Min Temp", f"{main_data['temp_min']}°F")
    parse_data.setdefault("Max Temp", f"{main_data['temp_max']}°F")
    parse_data.setdefault("Humidity", f"{main_data['humidity']}%")
    parse_data.setdefault("Pressure", f"{main_data['pressure']}hPa")

     # Weather Description 
    desc = weather_data["weather"][0]
    parse_data.setdefault("Conditions", f"{desc['main']}—{desc['description']}")
    # Sunrise Sunset 
    sun = weather_data["sys"]
    tz = weather_data["timezone"]
    sunrise = parse_datetime(sun["sunrise"], tz)
    parse_data.setdefault("Sunrise", f"{sunrise}")
    sunset = parse_datetime(sun["sunset"], tz)
    parse_data.setdefault("Sunset", f"{sunset}")
    # Wind Informtion 
    parse_data.setdefault("Wind Speed", f"{weather_data['wind']['speed']} Kmph")
    parse_data.setdefault("Wind Direction", f"{weather_data['wind']['deg']}")
    # Visibility 
    parse_data.setdefault("Visibility", f"{weather_data['visibility']//1000}km")
    return parse_data

model_with_tools = groq_model.bind_tools([get_weather])

# Response 
city = input("Enter the city to search for weather: ")
response = model_with_tools.invoke(city)
pprint(response)
print("\n\n")
for tool_call in response.tool_calls:
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")
print("--------------------------------------------------------")
# Tool Execution Loop 
## Step-1:- Model generate tool calls
messages = [{"role": "user", "content": f"What's the weather in {city}?"}]
ai_msg = model_with_tools.invoke(messages)
## Step-2:- Execute tools and collect results
for tool_call in ai_msg.tool_calls:
    # Executed the tool with generated arguments
    tool_result = get_weather.invoke(tool_call)
    messages.append(tool_result)
## Step-3:- Pass results back to model for final response
final_response = model_with_tools.invoke(messages)
pprint(final_response.text)