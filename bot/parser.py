from collections import namedtuple
import datetime
import requests


def get_json(url):
    return requests.get(url).json()


def get_basic_statistics():
    url = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/1/query?f=json&where=Confirmed > 0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=[{"statisticType":"sum","onStatisticField":"%s","outStatisticFieldName":"value"}]'

    totalDeaths = get_json(url % "Deaths")['features'][0]['attributes']['value']
    totalConfirmed = get_json(url % "Confirmed")['features'][0]['attributes']['value']
    cured = get_json(url % "Recovered")['features'][0]['attributes']['value']
    return totalConfirmed, totalDeaths, cured


def get_counties_info():
    url = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed > 0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed desc&outSR=102100&resultOffset=0&resultRecordCount=100"
    json = get_json(url)
    countries = json['features']
    Country = namedtuple("Country", ("name", "confirmed", "deaths", "recovered"))
    # info = tuple(Country(c['attributes']['Country_Region'],
    #                      c['attributes']['Confirmed'],
    #                      c['attributes']['Deaths'],
    #                      c['attributes']['Recovered']) for c in countries)
    info = []
    for country in countries:
        if country['attributes']['Country_Region'] == "Mainland China":
            country['attributes']['Country_Region'] = "China"
        info.append(Country(country['attributes']['Country_Region'],
                            country['attributes']['Confirmed'],
                            country['attributes']['Deaths'],
                            country['attributes']['Recovered']))
    return info


def build_tagged_string(tag, string):
    opening_tag = f'<{tag}>'
    closing_tag = f'</{tag}>'
    return f"{opening_tag}{string}{closing_tag}"


def build_tg_message():
    message_text = ""

    confirmed, deaths, cured = get_basic_statistics()
    message_text += f"{build_tagged_string('b', 'Всего зараженных☣️: ')} {confirmed}\n"
    message_text += f"{build_tagged_string('b', 'Погибших☠️: ')} {deaths}\n"
    message_text += f"{build_tagged_string('b', 'Выздоровело💊: ')} {cured}\n"

    message_text += "\n\n"
    message_text += "По странам: (страна: инфицировано, смертей, выздоровлений):\n\n"
    countries_template = "{}: {}, {}, {}\n"
    for country in sorted(get_counties_info(), key=lambda country: country.confirmed, reverse=True):
        message_text += countries_template.format(build_tagged_string('b', country.name),
                                                  country.confirmed,
                                                  country.deaths,
                                                  country.recovered)

    message_text += "\n\n"
    message_text += datetime.datetime.utcnow().strftime("%A %d.%m.%Y %H:%M UTC+0")

    return message_text
