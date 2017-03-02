
from StartScreen import IntroUI, AboutGameUI
from GameSetup import AddPlayersUI, GameSettingsUI
from QA import QuestionUI, AnswerUI

class UIManager():
	_widget_tracker = {}
	_root_widget = None

	def __init__(self, app_ref, root_widget):
		self.app_ref = app_ref

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