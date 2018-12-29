# -*- coding: utf-8 -*-

import calendar
import json
from datetime import datetime
from datetime import timedelta
from time import sleep

import requests
from jinja2 import Template

# from structures import TimeCurrent
from structures import TimeLastUpdate
from structures import WeatherCurrent
from structures import WeatherForecast
from structures import WeatherForecastPart
from translation import condition_map
# from translation import day_of_week_map
from translation import daytime_map
# from translation import month_map
from translation import moon_code_map
from translation import wind_dir_map


key = '...'        # weather on site
url = 'https://api.weather.yandex.ru/v1/informers'  # weather on site
icon_url = (
    'https://yastatic.net/weather/i/icons/blueye/color/svg/{icon}.svg'
)
coordinates = {
    'lat': 56.284127,
    'lon': 44.070468,
}


def temp_convert(temp):
    if temp > 0:
        return '+{0}'.format(temp)
    return str(temp)


def translate(value, mapping):
    res = mapping.get(value, None)
    return res


def template_read():
    template_file = 'html/page_template.html'
    with open(template_file, 'r') as fileo:
        template_content = fileo.read()
    template = Template(template_content.decode('utf-8'))
    return template


def template_render(template, **kwargs):
    rendered_file = 'html/page_rendered.html'
    with open(rendered_file, 'w') as fileo:
        fileo.write(
            template.render(**kwargs).encode('utf-8')
        )


def get_weather():
    headers = {'X-Yandex-API-Key': key}
    payload = {'lang': 'en_US'}
    payload.update(coordinates)
    f_name = 'json/resp_last.json'

    try:
        r = requests.get(url, params=payload, headers=headers)
        out = r.json()
    except Exception:
        with open(f_name, 'r') as fileo:
            out = json.loads(fileo.read())
    else:
        with open(f_name, 'w') as fileo:
            fileo.write(
                json.dumps(out, indent=4, sort_keys=True)
            )
    return out


def prepare_calendar(now=None):
    now = now or datetime.now()
    cal = calendar.LocaleHTMLCalendar(firstweekday=calendar.MONDAY, locale='Russian_Russia')
    res = cal.formatmonth(now.year, now.month, withyear=False)
    return res


def prepare_time_last_upd(upd_time):
    last_update_time = datetime.fromtimestamp(upd_time)
    result = TimeLastUpdate(
        upd_time=last_update_time.strftime('%H:%M'),
    )
    return result


def prepare_weather_current(fact):
    result = WeatherCurrent(
        temp=temp_convert(fact['temp']),
        feels_like=temp_convert(fact['feels_like']),
        condition=translate(fact['condition'], condition_map),
        pressure_mm=fact['pressure_mm'],
        humidity=fact['humidity'],
        wind_speed=fact['wind_speed'],
        wind_gust=fact['wind_gust'],
        wind_dir=translate(fact['wind_dir'], wind_dir_map),
        icon=icon_url.format(icon=fact['icon']),
    )
    return result


def prepare_weather_forecast(forecast):
    # get day duration
    sunrise = datetime.strptime(forecast['sunrise'], '%H:%M')
    sunset = datetime.strptime(forecast['sunset'], '%H:%M')
    seconds = (sunset - sunrise).seconds
    minutes, _ = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    # forecast for 2 next parts
    parts = []
    for part in forecast['parts']:
        parts.append(
            WeatherForecastPart(
                condition=translate(part['condition'], condition_map),
                feels_like=temp_convert(part['feels_like']),
                humidity=part['humidity'],
                icon=icon_url.format(icon=part['icon']),
                part_name=translate(part['part_name'], daytime_map),
                pressure_mm=part['pressure_mm'],
                temp_avg=temp_convert(part['temp_avg']),
                temp_max=temp_convert(part['temp_max']),
                temp_min=temp_convert(part['temp_min']),
                wind_dir=translate(part['wind_dir'], wind_dir_map),
                wind_gust=part['wind_gust'],
                wind_speed=part['wind_speed'],
            )
        )
    result = WeatherForecast(
        moon_text=translate(forecast['moon_text'], moon_code_map),
        sunrise=forecast['sunrise'],
        sunset=forecast['sunset'],
        day_length=u'{0}ч {1}мин'.format(hours, minutes),
        parts=parts,
    )
    return result


if __name__ == "__main__":

    while True:
        weather = get_weather()
        time_last_upd = prepare_time_last_upd(weather['now'])
        weather_current = prepare_weather_current(weather['fact'])
        weather_forecast = prepare_weather_forecast(weather['forecast'])

        template_render(
            template=template_read(),
            WEATHER_CURRENT=weather_current,
            WEATHER_FORECAST=weather_forecast,
            # CALENDAR=prepare_calendar(),
            CALENDAR=None,
            LAST_UPD=prepare_time_last_upd(weather['now']),
        )

        print 'Updated: {}'.format(datetime.now())
        sleep(30 * 60)
        # break
