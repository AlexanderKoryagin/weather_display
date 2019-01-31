# -*- coding: utf-8 -*-

import json
from datetime import datetime
from time import sleep

import requests
import yaml
from jinja2 import Template

from srs.structures import TimeLastUpdate
from srs.structures import WeatherCurrent
from srs.structures import WeatherForecast
from srs.structures import WeatherForecastPart
from srs.translation import condition_map
from srs.translation import daytime_map
from srs.translation import moon_code_map
from srs.translation import wind_dir_map


def read_config():
    cfg_file = "config.yml"
    with open(cfg_file, "r") as filo:
        config = yaml.load(filo)
    return config


CONFIG = read_config()


def read_api_key():
    key_file = "api_key.yml"
    with open(key_file, "r") as filo:
        config = yaml.load(filo)
    return config["key"]


def get_weather():
    headers = {"X-Yandex-API-Key": read_api_key()}
    payload = {"lang": "en_US"}
    payload.update(CONFIG["yandex"]["coordinates"])
    # get data
    resp = requests.get(CONFIG["yandex"]["url"], params=payload, headers=headers)
    resp_json = resp.json()

    if not resp.ok:
        raise Exception("Can not get {0.url}.\nReason: {0.reason} ({0.status_code})".format(resp))

    with open(CONFIG["files"]["weather_json_file"], "w") as fileo:
        fileo.write(json.dumps(resp_json, indent=4, sort_keys=True))
    return resp_json


def temp_convert(temp):
    if temp > 0:
        return "+%s" % temp
    return str(temp)


def translate(value, mapping):
    res = mapping.get(value, None)
    return res


def template_read():
    with open(CONFIG["files"]["html_template_file"], "r", encoding="utf-8") as fileo:
        template_content = fileo.read()
    template = Template(template_content)
    return template


def template_render(template, **kwargs):
    with open(CONFIG["files"]["html_rendered_file"], "w", encoding="utf-8") as fileo:
        rendered_template = template.render(**kwargs)
        fileo.write(rendered_template)


def prepare_time_last_upd(upd_time):
    last_update_time = datetime.fromtimestamp(upd_time)
    result = TimeLastUpdate(upd_time=last_update_time.strftime("%H:%M"))
    return result


def prepare_weather_current(fact):
    result = WeatherCurrent(
        temp=temp_convert(fact["temp"]),
        feels_like=temp_convert(fact["feels_like"]),
        condition=translate(fact["condition"], condition_map),
        pressure_mm=fact["pressure_mm"],
        humidity=fact["humidity"],
        wind_speed=fact["wind_speed"],
        wind_gust=fact["wind_gust"],
        wind_dir=translate(fact["wind_dir"], wind_dir_map),
        icon=CONFIG["yandex"]["icon_url"].format(icon=fact["icon"]),
    )
    return result


def prepare_weather_forecast(forecast):
    # get day duration
    sunrise = datetime.strptime(forecast["sunrise"], "%H:%M")
    sunset = datetime.strptime(forecast["sunset"], "%H:%M")
    seconds = (sunset - sunrise).seconds
    minutes, _ = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    # forecast for 2 next parts
    parts = []
    for part in forecast["parts"]:
        parts.append(
            WeatherForecastPart(
                condition=translate(part["condition"], condition_map),
                feels_like=temp_convert(part["feels_like"]),
                humidity=part["humidity"],
                icon=CONFIG["yandex"]["icon_url"].format(icon=part["icon"]),
                part_name=translate(part["part_name"], daytime_map),
                pressure_mm=part["pressure_mm"],
                temp_avg=temp_convert(part["temp_avg"]),
                temp_max=temp_convert(part["temp_max"]),
                temp_min=temp_convert(part["temp_min"]),
                wind_dir=translate(part["wind_dir"], wind_dir_map),
                wind_gust=part["wind_gust"],
                wind_speed=part["wind_speed"],
            )
        )
    result = WeatherForecast(
        moon_text=translate(forecast["moon_text"], moon_code_map),
        sunrise=forecast["sunrise"],
        sunset=forecast["sunset"],
        day_length="%sч %sмин" % (hours, minutes),
        parts=parts,
    )
    return result


def main():
    weather = get_weather()
    weather_current = prepare_weather_current(weather["fact"])
    weather_forecast = prepare_weather_forecast(weather["forecast"])
    template_render(
        template=template_read(),
        WEATHER_CURRENT=weather_current,
        WEATHER_FORECAST=weather_forecast,
        LAST_UPD=prepare_time_last_upd(weather["now"]),
    )
    print("Updated: %s" % datetime.now())


if __name__ == "__main__":

    while True:
        main()
        # break
        sleep(30 * 60)
