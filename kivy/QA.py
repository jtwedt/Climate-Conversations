from kivy.uix.boxlayout import BoxLayout

class QuestionUI(BoxLayout):
	def __init__(self, **kwargs):
		BoxLayout.__init__(self, **kwargs)

	def set_ui_reference(self, ui):
		self._ui = ui

	

class AnswerUI(BoxLayout):
	def __init__(self, **kwargs):
		BoxLayout.__init__(self, **kwargs)

	def set_ui_reference(self, ui):
		self._ui = ui