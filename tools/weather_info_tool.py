import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from utils.weather_info import WeatherForcastTool
from langchain.tools import tool

class WeatherInfoTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENWEATHER_API_KEY")
        self.weather_Service = WeatherForcastTool(self.api_key)
        self.weather_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """setup all the tools for the weather forecast tool"""
        @tool
        def get_current_weather(city:str) -> str:
            """Get the current weather in a given city."""
            weather_data = self.weather_Service.get_weather_current(city)
            if weather_data:
                temp = weather_data.get('main', {}).get('temp' , 'N/A')
                desc = weather_data.get('weather', [{}])[0].get('description', 'N/A')
                return f"The current weather in {city} is {desc} with a temperature of {temp}°C."
            return f"Could not retrieve weather data for {city}."

        @tool
        def get_weather_forecast(city:str) -> str:
            """Get the weather forecast for the city."""
            forecast_data = self.weather_Service.get_forecast_weather(city)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data['list'])):
                    item = forecast_data['list'][i]
                    date = item['dt_txt'].split(' ')[0]
                    temp = item['main']['temp']
                    desc = item['weather'][0]['description']
                    forecast_summary.append(f"{date}: {desc} with a temperature of {temp}°C")
                return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
            return f"Could not retrieve weather forecast for {city}."
        
        return [get_current_weather, get_weather_forecast]
                