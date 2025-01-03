# python D:\pythonFile\python_task\Lab3\weather.py C:\Users\22390\Desktop\europe.csv
import asyncio
import aiohttp
import csv
from typing import Dict, List


async def get_weather(session, city_name, latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    async with session.get(url) as response:
        data = await response.json()
        temperature = data['current_weather']['temperature']
        return f"{city_name}: {temperature}°C"


async def load_city_coordinates(file_path: str) -> List[Dict[str, str]]:
    cities = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cities.append({
                'city': row['capital'],
                'country': row['country'],
                'latitude': float(row['latitude']),
                'longitude': float(row['longitude']),
            })
    return cities


async def fetch_weather_for_all(cities: List[Dict[str, str]]):
    async with aiohttp.ClientSession() as session:
        tasks = [
            get_weather(session, f"{city['city']}, {city['country']}", city['latitude'], city['longitude'])
            for city in cities
        ]
        weather_results = await asyncio.gather(*tasks)

        for result in weather_results:
            print(result)


async def main(city_file_path: str):
    cities = await load_city_coordinates(city_file_path)
    await fetch_weather_for_all(cities)


if __name__ == '__main__':
    city_file_csv = 'D:\pythonFile\python_task\weather\my_project\europe.csv'
    asyncio.run(main(city_file_csv))
