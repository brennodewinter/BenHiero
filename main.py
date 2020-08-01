import os
os.environ["KCFG_KIVY_LOG_LEVEL"] = "warning"

import kivy
import numpy as np
assert numpy
import sounddevice as sd


kivy.require('1.10.1')

from kivy.app import App
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.graphics import Rectangle, Color  
from kivy.lang import Builder   
from kivy.properties import ObjectProperty, StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.settings import Settings
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

#Some constants
appversion = 0.01
channellist = ["CP",  "Safe Harbour",  "Orga",  "Content", "Security",  "First AID",  "Bullshiting"]
currentchannel = 5

#Config
settingspanel = '''
[
    {
        "type": "title",  
        "title": "Ben Hiero"
    }, 
    {
        "type": "string", 
        "title": "Communication server", 
        "section": "Communicator", 
        "desc": "Enter the FQDN for the communication server",
        "key": "server"
    }, 
    {
        "type": "bool", 
        "title": "Share GPS-location", 
        "section": "Communicator", 
        "desc": "Allow the GPS to be sent along with messages",
        "key": "sharegps"
    }
]
'''

config = ConfigParser()
config.read('benhiero.ini')


class BenHieroScreen(Widget):
    channel = ObjectProperty(None)
    def update_txt(self, lbl,  choice):
        global currentchannel,  channelist
        if choice == "up":
            currentchannel+=1
            if currentchannel == len(channellist):
                currentchannel=0
        else:
            currentchannel-=1
            if currentchannel < 0:
                currentchannel == len(channellist)-1
        chosenchannel=channellist[currentchannel]
        lbl.text=f"Current Channel:{chosenchannel} "

class BenHieroApp(App):
       
    def build(self):
        global appversion, currentchannel 
        global settingspanel
  
        self.config
        
        #self.use_kivy_settings = False
        return BenHieroScreen()
     
    def build_config(self, config):
        config.setdefaults("Communicator", {"server": "main.benhiero.nl", "sharegps": False})
        
    def build_settings(self, settings):
        settings.add_json_panel('Communicator', self.config, data= settingspanel)
    
    def on_config_change(self,  config, section, key,  value):
        print (config, section, key, value)
        config.write
        
if __name__ == '__main__':
    BenHieroApp().run()
