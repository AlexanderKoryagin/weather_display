# Weather display
Show weather forecast for displaying on Raspberry Pi 3 display.


## Rendered page should looks like:
_(It is in Russian)_
![PageView](./img/weather_display_page_rendered.png)


## Python virtualenv on Windows
```bash
python -m pip install -U pip
python -m pip install -U setuptools
python -m pip install -U virtualenv

virtualenv -p python --clear .venv --clear
source .venv/Scripts/activate

python -m pip install -U -r requirements.txt
```


## More info:
https://tech.yandex.ru/weather/doc/dg/concepts/forecast-response-test-docpage

### Ignore API KEY file 
```bash
git update-index --assume-unchanged api_key.yml
```
