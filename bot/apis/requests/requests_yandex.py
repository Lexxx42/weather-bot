import requests as req
import json
import logging
from ... import tokens
from os import path

FILE_NAME_JSON = 'yandex_weather.json'
headers = {'X-Yandex-API-Key': tokens.token_yandex_weather}


# token = ""

def yandex_weather(latitude, longitude, token_yandex: str):
    url_yandex = f'https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&[lang=ru_RU]'
    yandex_req = req.get(url_yandex, headers={'X-Yandex-API-Key': tokens.token_yandex_weather})
    logging.info(f"made request to API yandex {url_yandex}")
    return yandex_req


async def save_to_file(data):
    with open(FILE_NAME_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        logging.info(f"data saved to {FILE_NAME_JSON}")


async def get_weather_yandex(lat: float, lon: float):
    latitude_input = lat
    longitude_input = lon
    data_request = yandex_weather(latitude_input, longitude_input, tokens.token_yandex_weather).json()
    logging.info("data collected from response")
    await save_to_file(data_request)
    conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                  'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                  'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                  'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                  'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                  'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                  'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                  }
    wind_dir = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное',
                'se': 'юго-восточное', 's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'с': 'штиль'}

    yandex_json = load_from_file()
    yandex_json['fact']['condition'] = conditions[yandex_json['fact']['condition']]
    yandex_json['fact']['wind_dir'] = wind_dir[yandex_json['fact']['wind_dir']]
    for parts in yandex_json['forecasts']['parts']:
        parts['condition'] = conditions[parts['condition']]
        parts['wind_dir'] = wind_dir[parts['wind_dir']]

    pogoda = dict()
    params = ['condition', 'wind_dir', 'pressure_mm', 'humidity']
    for parts in yandex_json['forecasts']['parts']:
        pogoda[parts['part_name']] = dict()
        pogoda[parts['part_name']]['temp'] = parts['temp_avg']
        for param in params:
            pogoda[parts['part_name']][param] = parts[param]

    pogoda['fact'] = dict()
    pogoda['fact']['temp'] = yandex_json['fact']['temp']
    for param in params:
        pogoda['fact'][param] = yandex_json['fact'][param]

    pogoda['link'] = yandex_json['info']['url']
    print(pogoda)
    return pogoda


def load_from_file():
    if path.exists(FILE_NAME_JSON):
        with open(FILE_NAME_JSON, encoding="utf-8") as file:
            data = json.load(file)
        print(f"json {FILE_NAME_JSON} loaded")
    else:
        data = None
        print(f"there is no file {FILE_NAME_JSON}")
    return data
