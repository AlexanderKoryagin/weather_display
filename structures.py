# -*- coding: utf-8 -*-

from collections import namedtuple


TimeCurrent = namedtuple(
    'TimeCurrent',
    (
        'time',  # 23:20
        'day',   # 31 Июль, Вторник
        'week',  # w31.2
    )
)

TimeLastUpdate = namedtuple(
    'TimeLastUpdate',
    (
        'upd_time',        # 08:46
    )
)

WeatherCurrent = namedtuple(
    'WeatherCurrent',
    (
        'temp',         # 21
        'feels_like',   # 20
        'condition',    # Ясно
        'pressure_mm',  # 758
        'humidity',     # 64
        'wind_speed',   # 2.5
        'wind_gust',    # 6.6
        'wind_dir',     # Северо-Восточный
        'icon',         # https://yastatic.net/...
    )
)

WeatherForecast = namedtuple(
    'WeatherForecast',
    (
        'moon_text',   # Убывающая Луна
        'sunrise',     # 04:03
        'sunset',      # 20:15
        'day_length',  # 16ч 12мин
        'parts',       # [...]
    )
)

WeatherForecastPart = namedtuple(
    'WeatherForecastPart',
    (
        'condition',    # Ясно
        'feels_like',   # 23
        'humidity',     # 41
        'icon',         # https://yastatic.net/...
        'part_name',    # День
        'pressure_mm',  # 758
        'temp_avg',     # 25
        'temp_max',     # 26
        'temp_min',     # 24
        'wind_dir',     # Северо-Восточный
        'wind_gust',    # 8.1
        'wind_speed',   # 3.4
    )
)
