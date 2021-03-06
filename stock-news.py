import pyttsx3
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup

baza = "https://www.marketwatch.com/investing/stock/"

zina = pyttsx3.init()                                                      # BAZA LINK -- https://www.marketwatch.com/
voices = zina.getProperty('voices')
zina.setProperty('voice', voices[0].id)
zina.setProperty('rate', 150)


def voice():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        audio = r.listen(source)
    country = r.recognize_google(audio, language="en-US").lower()
    print(country)
    return country


zina.say("Hi! I will tell the latest news about any joint stock company.  To begin, enter the abbreviation of the "
         "company name.") 
zina.runAndWait()
zina.stop()
name = input().lower()
name = name + "?"
zina.say("Tell me, to which country does it belong? Poland or America?")
zina.runAndWait()
zina.stop()

country = voice().lower()

if country == 'poland' or country == 'america':
    if country == 'poland':
        country = 'countrycode=pl&mod=mw_quote_tab'
    if country == 'america':
        country = 'mod=mw_quote_tab'
else:
    zina.say("Please repeat, Poland or America?")
    zina.runAndWait()
    zina.stop()
    voice()

link = f'{baza}{name}{country}'
print(link)

header = {'user-agent': 'zina'}

response = requests.get(link, headers=header).text
soup = BeautifulSoup(response, 'lxml')

block = soup.find('div', class_="collection__elements")
block1 = block.find('div', class_="element element--article")
block2 = block1.find('a', class_="link").get('href')
link_news = str(block2)

response2 = requests.get(link_news, headers=header).text
soup2 = BeautifulSoup(response2, 'lxml')

b = soup2.find('div', class_="article__body")
b2 = b.find('p').text
b3 = b.find('div', class_="paywall")
b4 = b3.find('p').text

result = (b2 + b4)
zina = pyttsx3.init()
voices = zina.getProperty('voices')
zina.setProperty('voice', voices[0].id)
zina.setProperty('rate', 160)
zina.say(result)
zina.runAndWait()
