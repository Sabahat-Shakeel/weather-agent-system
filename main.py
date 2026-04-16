import os
import requests
from typing import cast
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import  BaseModel
from openai.types.responses import ResponseTextDeltaEvent
from agents import (Agent, function_tool, Runner )
from agents import (OpenAIChatCompletionsModel, RunConfig, ModelProvider, ModelSettings, set_default_openai_client,set_tracing_disabled )




load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not founded : ")



external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client= external_client

)

config = RunConfig(
    model = model,
    model_provider = cast(ModelProvider , external_client),
    tracing_disabled = True

)

set_default_openai_client(external_client)
set_tracing_disabled(True)


class WeatherRequest(BaseModel):
    city: str

@function_tool()
def get_weather(city: WeatherRequest) -> str:
    """
    Get the current weather for a given city
    """
    try:
            fetch = requests.get(f"{os.getenv('WEATHER_API_KEY')}")
            data = fetch.json()
            return f"The current weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."

    except Exception as e:
        return f"Error fetching weather data: {e}"        
           
           
weather_Agent = Agent[WeatherRequest](
    name="weather_agent",
    instructions="you are helpfull assistant, Use this tool to get the current weather for a given city. and said im sabahat ai assisatnt for weather forecasting tjis type of prompt like eg: hi, hello, hey etc. ",
    tools=[get_weather],
    tool_use_behavior= "run_llm_again", 
    model_settings=ModelSettings(tool_choice="auto"),
)


import chainlit as cl

@cl.on_chat_start
async def on_start():

    cl.user_session.set("memory",[])
 
    await cl.Message(content= "Sabahat").send()
    await cl.Message(content="AI Assistant For Weather Forecasting. ask me about the weather in any city!" ).send()


@cl.on_message
async def handle_message(message: cl.Message):
 
    memory = cl.user_session.get("memory", [])
    if not isinstance(memory, list):
        memory = []


    memory.append({"role": "user", "content": message.content})

    cl.user_session.set("memory", memory)


    msg = cl.Message(content="")
    await msg.send()

    try:
      
        result = Runner.run_streamed(weather_Agent, input=memory, run_config=config)

   
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                await msg.stream_token(event.data.delta)


        final_response = result.final_output if hasattr(result, "final_output") else msg.content

        memory.append({"role": "assistant", "content": final_response})

        cl.user_session.set("memory", memory)


    except Exception as e:
        error_message = f"An error occurred\nResponse not found, please try later: {str(e)}"
        memory.append({"role": "assistant", "content": error_message})

        cl.user_session.set("memory", memory)

        await cl.Message(content=error_message).send()
        return