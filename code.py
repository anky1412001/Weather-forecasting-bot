import discord
import os
import re
import requests
import json
import datetime

# Function to validate the date

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    else:
      return True
# Creating regular expressions to detect commands 

redexc = '\$current.*'
redexf ='\$forecast.*'
redexca = '\$advanced current.*'
redexfa ='\$advanced forecast.*'

# Functions for displaying current weather conditions

def current(place):
    if(place.isalpha()==False):
      return "🚫Incorrect arguments!"
    place = place.title()
    var = "http://api.weatherapi.com/v1/current.json?key=4cc2be672eca4a6282a165515210412&q="
    var = var + place
    respons = requests.get(var)
    if (respons.status_code >299):
        return "🚫Incorrect arguments!"

   # In API if our request is correct the status code is less than 300 and if it's wrong then the value of the status code is 300 and more depending upon the error

    abc = respons.text
    res = json.loads(abc)

    # Response.text is the json file we are converting it to dictionary here

    # Obtaining the right data and returning as string

    curr = res['current']
    out = "Last recorded : " + curr['last_updated'] + "\nTemp: "+ str(curr['temp_c']) +u'\N{DEGREE SIGN}' +"C\nCondition: " + curr['condition']['text']
    return out

# Returns basic weather forecast for any date in the next 10 days

def forecast(place,date):
    if(place.isalpha()==False):
      return "🚫Incorrect arguments!"
    if(validate(date)==False):
      return "Wrong date"
    var = "http://api.weatherapi.com/v1/forecast.json?key=4cc2be672eca4a6282a165515210412&q="
    place = place.title()
    var = var + place
    var = var +"&dt="
    var = var + date
    respons = requests.get(var,date)
    if (respons.status_code >299):
        return "🚫Incorrect arguments!"
    abc = respons.text
    res = json.loads(abc)
    a = res['forecast']['forecastday'][0]
    fore = a['day']
    out = "Max Temp: "+ str(fore['maxtemp_c']) +u'\N{DEGREE SIGN}'+"C\nMin Temp: "+ str(fore['mintemp_c']) + u'\N{DEGREE SIGN}'+"C\nCondition: " + fore['condition']['text']
    return out

# Returns the current weather conditions in a detailed manner

def currentadvance(place):

    if(place.isalpha()==False):
      return "🚫Incorrect arguments!"
    place = place.title()
    var = "http://api.weatherapi.com/v1/current.json?key=4cc2be672eca4a6282a165515210412&q="
    var = var + place
    respons = requests.get(var)
    if (respons.status_code >299):
        return "🚫Incorrect arguments!"
    abc = respons.text
    res = json.loads(abc)
    curr = res['current']
    out = "Last recorded : " + curr['last_updated'] + "\nTemp: "+ str(curr['temp_c']) +u'\N{DEGREE SIGN}' +"C\nFeels like: "+ str(curr['feelslike_c'])+ u'\N{DEGREE SIGN}'+ "C\nCondition: " + curr['condition']['text'] +"\nWindspeed :" + str(curr['wind_kph']) +" Km/h\nWind direction:" + curr['wind_dir'] +"\nPrecipitaion:"+ str(curr['precip_mm']) + " mm" +"\nHumidity:" + str(curr['humidity']) + "%"
    return out

# Returns the forecasted weather conditions in a detailed manner

def forecastadvance(place,date):
    if(place.isalpha()==False):
      return "🚫Incorrect arguments!"
    if(validate(date)==False):
      return "Wrong date"
    var = "http://api.weatherapi.com/v1/forecast.json?key=4cc2be672eca4a6282a165515210412&q="
    place = place.title()
    var = var + place
    var = var +"&dt="
    var = var + date
    respons = requests.get(var,date)
    if (respons.status_code >299):
        return "🚫Incorrect arguments!"
    abc = respons.text
    res = json.loads(abc)
    a = res['forecast']['forecastday'][0]
    fore = a['day']
    out = "Max Temp: "+ str(fore['maxtemp_c']) +u'\N{DEGREE SIGN}'+"C\nMin Temp: "+ str(fore['mintemp_c']) + u'\N{DEGREE SIGN}'+"C\nCondition: " + fore['condition']['text'] + "\nAverage Windspeed :" + str(fore['avgvis_km']) + "\nChance of rain: "+ str(fore['daily_chance_of_rain']) + "%\nAverage humidity: "  + str(fore['avghumidity']) + "%"
    return out


client = discord.Client()
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

# Console message log
@client.event
async def  on_message(message):
  username = str(message.author).split('#')[0]
  user_message = str(message.content)
  channel = str(message.channel.name)
  print(f'{username}: {user_message} ({channel})')

  if message.author == client.user:
    return

# Reading the user's command and executing the respective functions

  if message.channel.name == 'general':
    if user_message.lower() == '$hello':
      out = f"Hello {username}! 👋" + "\n I am at your service \n These are my commands " + " :\n1️⃣ $forecast city date(YYYY-MM-DD)\n2️⃣ $current city \n3️⃣ $advanced forecast city date(YYYY-MM-DD)\n4️⃣ $advanced current city\n5️⃣ $hello\n6️⃣ $bye"
      await message.channel.send(out)
      return
    if user_message.lower() == '$bye':
      await message.channel.send(f'See you later {username}! 🤝')
      return

    if(re.match(redexc,user_message)):
      
      abc = user_message.split()
      loc = abc[1]
      out = current(loc)
      await message.channel.send(out)
      return

    if(re.match(redexca,user_message)):
      
      abc = user_message.split()
      loc = abc[2]
      out = currentadvance(loc)
      await message.channel.send(out)
      return

    if(re.match(redexf,user_message)):
      
      abc = user_message.split()
      loc = abc[1]
      t = abc[2]
      out = forecast(loc,t)
      await message.channel.send(out)
      return

    if(re.match(redexfa,user_message)):
      
      abc = user_message.split()
      loc = abc[2]
      t = abc[3]
      out = forecastadvance(loc,t)
      await message.channel.send(out)
      return

  if user_message.lower() == '!anywhere':
      await message.channel.send(user_message)
      return
     
# Secret key(token) has been imported
#my_secret = os.environ['token']
my_secret = os.environ['TOKEN']
client.run(os.environ['TOKEN'])
