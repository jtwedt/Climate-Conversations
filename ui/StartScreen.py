from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.logger import Logger

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