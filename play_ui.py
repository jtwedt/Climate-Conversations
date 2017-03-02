import sys
import os
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.getcwd() + "/resources")
sys.path.insert(0, os.getcwd() + "/ui")	
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from ClimateConversationsCore import Conversation, Player
from UIManager import UIManager

class ClimateConversationsApp(App):
	def build(self):
		self.load_kv("ui/ClimateConversations.kv")
		root_element = BoxLayout()
		ui = UIManager(self, root_element)
		return root_element

if __name__ == '__main__':
	Config.set("kivy", "log_dir", os.getcwd() + "/logs")
	Config.set("kivy", "log_level", "debug")
	Config.set("kivy", "log_name", "kivy_%y-%m-%d_%_.txt")
	Config.set("kivy", "log_enable", "1") 
	Config.write()

	w = ClimateConversationsApp()
	ClimateConversationsApp.run(w)