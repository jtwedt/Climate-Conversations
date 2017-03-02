from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
# from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.logger import Logger
# from kivy.adapters.listadapter import ListAdapter
from kivy.config import Config
import os
from GameSetup import AddPlayersUI, GameSettingsUI
from QA import QuestionUI, AnswerUI


class UIManager():
	_widget_tracker = {}
	_root_widget = None

	def __init__(self, root_widget):
		self._root_widget = root_widget
		self._widget_tracker["IntroUI"] = IntroUI(rows=3)
		self._widget_tracker["IntroUI"].set_ui_reference(self)
		self._widget_tracker["AboutGameUI"] = AboutGameUI()
		self._widget_tracker["AboutGameUI"].set_ui_reference(self)
		self._widget_tracker["AddPlayersUI"] = AddPlayersUI()
		self._widget_tracker["AddPlayersUI"].set_ui_reference(self)
		self._widget_tracker["GameSettingsUI"] = GameSettingsUI(rows=9,cols=1)
		self._widget_tracker["GameSettingsUI"].set_ui_reference(self)

		# Probably need to load these on the fly, not here
		self._widget_tracker["QuestionUI"] = QuestionUI()
		self._widget_tracker["QuestionUI"].set_ui_reference(self)
		self._widget_tracker["AnswerUI"] = AnswerUI()
		self._widget_tracker["AnswerUI"].set_ui_reference(self)

		self.swap_widget("IntroUI")

	def swap_widget(self, widget_name):
		self._root_widget.clear_widgets()
		self._root_widget.add_widget(self._widget_tracker[widget_name])


class IntroUI(GridLayout):
	def __init__(self, **kwargs):
		GridLayout.__init__(self, **kwargs)

	def set_ui_reference(self, ui):
		self._ui = ui

	def begin_game(self):
		Logger.debug("IntroUI: Clicked begin game button")
		self._ui.swap_widget("AddPlayersUI")
		pass

	def about_game(self):
		Logger.debug("IntroUI: Clicked about game button")
		self._ui.swap_widget("AboutGameUI")
		pass


class AboutGameUI(BoxLayout):
	def __init__(self, **kwargs):
		BoxLayout.__init__(self, **kwargs)

	def set_ui_reference(self, ui):
		self._ui = ui

	def back_to_intro(self):
		Logger.debug("AboutGameUI: Clicked back to intro button")
		self._ui.swap_widget("IntroUI")


class ClimateConversationsApp(App):
	def build(self):
		root_element = BoxLayout()
		ui = UIManager(root_element)
		return root_element

if __name__ == '__main__':
	Config.set("kivy", "log_dir", os.getcwd() + "/logs")
	Config.set("kivy", "log_level", "debug")
	Config.set("kivy", "log_name", "kivy_%y-%m-%d_%_.txt")
	Config.set("kivy", "log_enable", "1") 
	Config.write()
	w = ClimateConversationsApp()
	ClimateConversationsApp.run(w)