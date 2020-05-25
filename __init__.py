# Netatmo Weather Skill
# Mycroft <=> Netatmo
# Parameters for home.mycroft.ai skills page
#'username': "your Netatmo account id"
#'password': "your Netatmo account password"
# device_id : "your device MAC address, or go to my.netatmo.com/app/station and check parameters"
#'client_id': "go to dev.netatmo.com, create/add an app and get a client Id" 
#'client_secret': "from dev.netatmo.com too" 

# Mycroft libraries

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft import intent_handler
from mycroft.skills.context import adds_context, removes_context

import requests

__author__ = 'henridbr'

LOGGER = getLogger(__name__)

class NetatmoWeatherSkill(MycroftSkill):

    def __init__(self):
        super(NetatmoWeatherSkill, self).__init__(name="NetatmoWeatherSkill")
      
#### Netatmo device connection
        self.user_name = self.settings.get('username') 
        self.pass_word = self.settings.get('password') 
        self.client_Id = self.settings.get('clientId') 
        self.client_Secret = self.settings.get('clientSecret') 
        self.device_Id = self.settings.get('deviceId')
        self.access_token = ''
        self.data = {}
        

        payload = {'grant_type': "password",
                   'username': self.user_name,
                   'password': self.pass_word,
                   'client_id': self.client_Id, 
                   'client_secret': self.client_Secret, 
                   'scope': "read_station"} 
                
        try:
            response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
            response.raise_for_status()
            self.access_token=response.json()["access_token"]
            self.refresh_token=response.json()["refresh_token"]
            scope=response.json()["scope"]
            
        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)           
                
#### Read Netatmo Data 
# Netatmo data structure :
# dict 'body' : {'devices' : ... , 'status' : .... , 'time_exec' : ... , 'time_server : ... }
# list 'devices' : [ { main_0 } , { main_1 } , ... ]
# dict 'main_0' : { ... , 'station_name' : 'xxxxx' , ... , 'dasboard_data' : { d_data } , ... , 'modules' : ... }
# dict 'dasboard_data' : { ... , 'Temperature' : 23 , ... , 'Pressure' : 1034 , ... }
# 'modules' has the same structure than 'devices'
# find station name :
#   ['devices'][0]['station_name']
# find Temperature (int) :
#   ['devices'][0]['dashboard_data']['Temperature']
# find Temperature (ext) :
#   ['devices'][0]['modules'][0]['dashboard_data']['Temperature']


        params = {'access_token': self.access_token,
                  'device_id': self.device_Id}
        try:
            response = requests.post("https://api.netatmo.com/api/getstationsdata", params=params)
            response.raise_for_status()
            self.data = response.json()["body"]
            
        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)
        
#### Intents
# Conversation example
# user : netatmo
# mycroft : gives the station name (to get the context)
# user : home temperatures 
# mycroft : says inside and outside temperatures

    @intent_handler(IntentBuilder("NetatmoIntent").require("NetatmoKeyword"))
    @adds_context('NetatmoContext','netatmo')
    def handle_netatmo_intent(self, message):             
        sta_name = self.data['devices'][0]['station_name']
        self.speak_dialog('netatmo',{"sta_name":sta_name})        
            
    @intent_handler(IntentBuilder("HomeTemperaturesIntent").require("HomeTemperaturesKeyword").require('NetatmoContext'))
    @adds_context('NetatmoContext','netatmo') 
    def handle_home_temperatures_intent(self, message):             
        temp_int = self.data['devices'][0]['dashboard_data']['Temperature']
        temp_ext = self.data['devices'][0]['modules'][0]['dashboard_data']['Temperature']
        self.speak_dialog('HomeTemperatures',{"temp_int":temp_int, "temp_ext":temp_ext})
   
    @intent_handler(IntentBuilder("InsideTemperatureIntent").require("InsideTemperatureKeyword").require('NetatmoContext'))
    @adds_context('NetatmoContext','netatmo')
    def handle_inside_temperatures_intent(self, message):            
        temp_int = self.data['devices'][0]['dashboard_data']['Temperature']
        temp_trend = self.data['devices'][0]['dashboard_data']['temp_trend']
        self.speak_dialog('InsideTemperature', {"temp_int": temp_int, "temp_trend": temp_trend})

    @intent_handler(IntentBuilder("OutsideTemperatureIntent").require("OutsideTemperatureKeyword").require('NetatmoContext'))
    @adds_context('NetatmoContext','netatmo') 
    def handle_outside_temperature_intent(self, message):             
        temp_ext = self.data['devices'][0]['modules'][0]['dashboard_data']['Temperature']
        temp_trend = self.data['devices'][0]['modules'][0]['dashboard_data']['temp_trend']
        self.speak_dialog('OutsideTemperature', {"temp_ext": temp_ext, "temp_trend": temp_trend})       

    @intent_handler(IntentBuilder("HomeHumidityIntent").require("HomeHumidityKeyword").require('NetatmoContext'))
    @adds_context('NetatmoContext','netatmo') 
    def handle_home_humidity_intent(self, message):             
        hum_int = self.data['devices'][0]['modules'][0]['dashboard_data']['Humidity']
        self.speak_dialog('HomeHumidity', {"hum_int": hum_int}) 
        
    @intent_handler(IntentBuilder("HomePressureIntent").require("HomePressureKeyword").require('NetatmoContext'))
    @adds_context('NetatmoContext','netatmo') 
    def handle_home_pressure_intent(self, message):             
        press_abs = self.data['devices'][0]['dashboard_data']['AbsolutePressure']
        press_trend = self.data['devices'][0]['dashboard_data']['pressure_trend']
        self.speak_dialog('HomePressure', {"press_abs": press_abs, "press_trend": press_trend})
                
         
    def stop(self):
        pass

def create_skill():
    return NetatmoWeatherSkill()
