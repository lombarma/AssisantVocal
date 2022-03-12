import datetime
from bs4 import BeautifulSoup
import requests as req
import pyjokes
import wikipediaapi
import speech_recognition as sr
import pyaudio
import listsOfCommands
import pyttsx3

MONTHS = dict([("01", "janvier"), ("02", "février"), ("03", "mars"), ("04", "avril"), ("05", "mai"),
               ("06", "juin"), ("07", "juillet"), ("08", "août"), ("09", "septembre"),
               ("10", "octobre"), ("11", "novembre"), ("12", "décembre")])


def get_current_date():
    date_brut = str(datetime.date.today())
    date_brut = date_brut.split("-")
    return f"Nous sommes le {date_brut[2]} {MONTHS[date_brut[1]]} {date_brut[0]}."


def get_description(temperature, description, rain_risk, feeling, wind, details_or_no, day):
    if details_or_no == "Non":
        return f"{day}. \nAujourd'hui, il fait {temperature}°C. \n{description}."
    elif details_or_no == "Oui":
        return f"{day}. \nAujourd'hui, il fait {temperature}°C. \nLe risque de pluie est de {rain_risk}, " \
               f"le ressenti est de {feeling} et il y a un vent de {wind}.\n{description}. "


def get_current_weather(details_or_no):
    resp = req.get("https://www.meteocity.com/france/paris-v2988507")
    soup = BeautifulSoup(resp.text, "html.parser")

    resp1 = req.get("https://www.meteo-paris.com/ile-de-france/previsions")
    soup1 = BeautifulSoup(resp1.text, "html.parser")

    day = soup.find(class_="weather-title").text
    temperature = soup.find(class_="temp").text
    details = (soup.find(class_="weather-details").text.split())
    rain_risk = ' '.join(details[2:4])
    feeling = ' '.join(details[5:6])
    wind = ' '.join(details[7:])
    description = ' '.join(soup1.find(class_="forecast-line__legend--text").text.split())
    return get_description(temperature, description, rain_risk, feeling, wind, details_or_no, day)


def get_joke():
    return pyjokes.get_joke()


def get_definition_from_wikipedia(topic):
    wiki_wiki = wikipediaapi.Wikipedia('fr')
    page_py = wiki_wiki.page(topic)
    return page_py.summary


def get_vocal_to_string():
    r = sr.Recognizer()
    micro = sr.Microphone()
    with micro as source:
        print("Je vous écoute !")
        audio_data = r.listen(source)
        print("Analyse en cours...")
    result = r.recognize_google(audio_data, language="fr-FR")
    return result


def spell_answers(answer):
    print(answer)
    engine = pyttsx3.init()
    engine.say(answer)
    engine.runAndWait()


def run():
    a = get_vocal_to_string().split()
    for i in a:
        if i in listsOfCommands.weather_commands:
            spell_answers(get_current_weather("Oui"))
        elif i in listsOfCommands.date_commands:
            spell_answers(get_current_date())
        elif i in listsOfCommands.joke_commands:
            spell_answers(get_joke())
        elif i in listsOfCommands.wiki_commands:
            spell_answers(get_definition_from_wikipedia(a[-1]))


if __name__ == "__main__":
    run()
