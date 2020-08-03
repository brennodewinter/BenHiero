import os
os.environ["KCFG_KIVY_LOG_LEVEL"] = "warning"

import kivy
import numpy as np
assert np
import pymumble_py3 as pymumble
assert pymumble
import sounddevice as sd
assert sd


kivy.require('1.10.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.config import ConfigParser
from kivy.properties import ObjectProperty
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
    },
    {
        "type": "bool",
        "title": "Enable managed communication mode",
        "section": "Communicator",
        "desc": "Enable a mode where the communication is managed by a central post",
        "key": "managed"
    }
]
'''

config = ConfigParser()
config.read('benhiero.ini')

#Screen
thescreen = '''
<BenHieroScreen>:    
    label: channel
    button: chandown
    button: chanup
    anim_type: 'fade_in'
    canvas:
        Rectangle:
            source: "images/hiero.jpeg"
            pos: self.pos
            size: self.size
        

    BoxLayout:
        top: root.height-self.height
        size: root.width /8,root.height/12
        Button:
            id: btnclose
            text: "Close"
            font_size: 20
            size: self.size
            size_hint: (None,None)
            #center_x: root.width / 2

 
            on_press: quit()
        Button:
            id: brnOpenSettings
            text: "Settings"
            font_size: 20
            size_hint: (None,None)
            size: self.size
            on_release: app.open_settings()
    Label:
        text: "Current Channel: <UNKOWN>"
        id: channel
        font_size: 42
        center_x: root.width / 2
        top: root.height/3
        markup: True
        shorten: True

    BoxLayout:
        Button:
            id: chandown
            text: 'Down'
            font_size: 42
            size_hint: (None,None)
            size: root.width / 4, root.height/6
            
            on_press: 
                #Here comes a routine that trys obtaining access to the channel
                #Then if talking is granted a sound and one can talk
                
                #placeholder feature
                root.update_txt(channel, chandown)

            on_release: 
                #Here comes a routine
                self.text="Neer"
            on_state:
                print("my current state is {}".format(self.state))
                    
        Button:
            id: ptt
            text: 'PTT'
            font_size: 42
            size_hint: (None,None)
            size: root.width / 2, root.height/6
            
            on_press: 
                #Here comes a routine that trys obtaining access to the channel
                #Then if talking is granted a sound and one can talk
                
                #placeholder feature
                self.text = "BLAHBLAH"

            on_release: 
                #Here comes a routine
                self.text="PTT!"
            on_state:
                print("my current state is {}".format(self.state))
        
        Button:
            id: chanup
            text: 'Up'
            font_size: 42
            size_hint: (None,None)
            size: root.width / 4, root.height/6
            
            on_press: 
                #Here comes a routine that tries obtaining access to the channel
                #Then if talking is granted a sound and one can talk
                
                #placeholder feature
                root.update_txt(channel,"up")

            on_release: 
                #Here comes a routine
                self.text="Op"
            on_state:
                print("my current state is {}".format(self.state))
'''
Builder.load_string(thescreen)

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
        config.setdefaults("Communicator", {"server": "srv.benhiero.nl", "sharegps": False,  "managed": 1})
        
    def build_settings(self, settings):
        settings.add_json_panel('Communicator', self.config, data= settingspanel)
    
    def on_config_change(self,  config, section, key,  value):
        print (config, section, key, value)
        config.write
        
if __name__ == '__main__':
    BenHieroApp().run()
