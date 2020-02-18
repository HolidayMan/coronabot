from collections import namedtuple
import datetime
import requests


def get_json(url):
    return requests.get(url).json()


def get_basic_statistics():
    url = "https://coronavirus-monitor.ru/api/v1/statistics/get-cities"
    json = get_json(url)
    totalDeaths = json['data']['totalDeaths']
    totalConfirmed = json['data']['totalConfirmed']
    cured = json['data']['cured']
    return totalConfirmed, totalDeaths, cured


def get_counties_info():
    url = "https://coronavirus-monitor.ru/api/v1/statistics/get-countries"
    json = get_json(url)
    countries = json['data']['countries']
    Country = namedtuple("Country", ("name", "confirmed", "deaths"))
    info = tuple(Country(c['ru'], c['confirmed'], c['deaths']) for c in countries)
    return info


def build_tagged_string(tag, string):
    opening_tag = f'<{tag}>'
    closing_tag = f'</{tag}>'
    return f"{opening_tag}{string}{closing_tag}"


def build_tg_message():
    message_text = ""

    confirmed, deaths, cured = get_basic_statistics()
    message_text += f"{build_tagged_string('b', 'Всего зараженных: ')} {confirmed}\n"
    message_text += f"{build_tagged_string('b', 'Погибших: ')} {deaths}\n"
    message_text += f"{build_tagged_string('b', 'Выздоровело: ')} {cured}\n"

    message_text += "\n\n"
    message_text += "По странам: (страна: заражений, смертей):\n"
    countries_template = "{}: {}, {}\n"
    for country in get_counties_info():
        message_text += countries_template.format(build_tagged_string('b', country.name), country.confirmed, country.deaths)

    message_text += "\n\n"
    message_text += datetime.datetime.utcnow().strftime("%A %d.%m.%Y %H:%M UTC+0")

    return message_text
