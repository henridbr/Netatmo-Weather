# <img src='https://raw.githubusercontent.com/henridbr/Netatmo-Weather/master/images/Home_Temp.png' card_color='#32B28F' width='50' height='50' style='vertical-align:bottom'/> Netatmo Weather
A Mycroft Skill for Home Temperatures and more with Netatmo.

## About 
Netatmo weather device is part of your home network using wifi and you can look at some parameters from Netatmo website on your desktop, or apps on smartphones and tablets.

[![Netatmo_weather station](https://raw.githubusercontent.com/henridbr/Netatmo-Weather/master/images/Netatmo-device.png
)](https://www.netatmo.com/en-US/product/weather/)

What's new with Mycroft ? "Hey Mycroft, what's the room temperature ?", it's easier and faster.

## Examples
* "Hey Mycroft, I need info from Netatmo" and Mycroft will connect to Netatmo
* "What's home temperature ?" and Mycroft says inside and out side temperatures
* "What's room temperature ?" and Mycroft says inside temperature and its trend
* "What's the temperature in our garden ?" and Mycroft says outside temperature and its trend
* "What's the pressure ?" and Mycroft says absolute (at sea level) atmospheric pressure and its trend
* "What's the humidity ?" and Mycroft says outside temperature and its trend

## Authorization
To connect Mycroft to Netatmo an authorization is required.
Besides your Netatmo account, register on dev.netatmo.com and create a new app to get some Ids.

After skill installation completed, check your skills on home.mycroft.ai.
Fill in the form named "Netatmo Weather Skill" and save. 

## Note
Temperature unit : Celsius degrees

Pressure unit : hectopascal

## Credits 
Henri Debierre (@henridbr)

[Netatmo SDK](https://dev.netatmo.com/resources/technical/samplessdks/codesamples#getstationsdata) 

## Supported Devices 
platform_picroft 

## Category
**Daily**
IoT

## Tags
#Netatmo
#Weather
#Picroft

## todo
* improve intents and context
* adapt to US units : °F, inch Hg (?)
