from attr import attrib
from attr import attrs
# from attr.validators import instance_of


# @attrs
# class TimeCurrent:
#     time = attrib()  # 23:20
#     day = attrib()   # 31 Июль, Вторник
#     week = attrib()  # w31.2


@attrs
class TimeLastUpdate:
    upd_time = attrib()  # 08:46


@attrs
class WeatherCurrent:
    temp = attrib()         # 21
    feels_like = attrib()   # 20
    condition = attrib()    # Ясно
    pressure_mm = attrib()  # 758
    humidity = attrib()     # 64
    wind_speed = attrib()   # 2.5
    wind_gust = attrib()    # 6.6
    wind_dir = attrib()     # Северо-Восточный
    icon = attrib()         # https://yastatic.net/...


@attrs
class WeatherForecast:
    moon_text = attrib()   # Убывающая Луна
    sunrise = attrib()     # 04:03
    sunset = attrib()      # 20:15
    day_length = attrib()  # 16ч 12мин
    parts = attrib()       # [...]


@attrs
class WeatherForecastPart:
    condition = attrib()    # Ясно
    feels_like = attrib()   # 23
    humidity = attrib()     # 41
    icon = attrib()         # https://yastatic.net/...
    part_name = attrib()    # День
    pressure_mm = attrib()  # 758
    temp_avg = attrib()     # 25
    temp_max = attrib()     # 26
    temp_min = attrib()     # 24
    wind_dir = attrib()     # Северо-Восточный
    wind_gust = attrib()    # 8.1
    wind_speed = attrib()   # 3.4
