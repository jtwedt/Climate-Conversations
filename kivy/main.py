from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import re
# from kivy.adapters.listadapter import ListAdapter
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


class IntInput(TextInput):
	def insert_text(self, input_string, from_undo=False):
		int_re = re.compile("[0-9]*")
		print "Calling insert_text, will probably break"
		# int_string = self.int_re.sub("", input_string)
		ints = re.findall(int_re, input_string)
		if len(ints) > 0:
			int_string = ints[0]
		print int_string
		return super(IntInput, self).insert_text(int_string, from_undo=from_undo)


class YearSelectorButton(ListItemButton):
	def register_press(self):
		print "Clicked: year", self.text
	pass


class IntroUI(GridLayout):
	def __init__(self, **kwargs):
		GridLayout.__init__(self, **kwargs)

	def set_ui_reference(self, ui):
		self._ui = ui

	def begin_game(self):
		print "Clicked: begin game button"
		self._ui.swap_widget("AddPlayersUI")
		pass

	def about_game(self):
		print "Clicked: about game button"
		self._ui.swap_widget("AboutGameUI")
		pass

class AboutGameUI(BoxLayout):
	def __init__(self, **kwargs):
		BoxLayout.__init__(self, **kwargs)

	def set_ui_reference(self, ui):
		self._ui = ui

	# def display_game_info(self):
		# pass

	def back_to_intro(self):
		print "Clicked: back to intro button"
		self._ui.swap_widget("IntroUI")
 
class AddPlayersUI(BoxLayout):
	def __init__(self, **kwargs):
		BoxLayout.__init__(self, **kwargs)
		self.players = []			
		self.selected_year = None
		self.next_screen_button_enabled = False

		#dropdown = DropDown()
		#for index in range(0,20):
	#		btn = Button(text="%d" %index, size_hint_y=None, height="50dp")
#			btn.bind(on_release=lambda btn: dropdown.select(btn.text))#
			# dropdown.add_widget(btn)
		#self.add_widget(dropdown)
		print "Beginning widget walk:"
		for widget in self.walk():
			print ("{} -> {}").format(widget, widget.id)
		print "End of widget walk."

	def set_ui_reference(self, ui):
		self._ui = ui

	def back_to_intro(self):
		print "Clicked: back to intro button"
		self._ui.swap_widget("IntroUI")

	def next_screen(self, button):
		print "Clicked: next screen button"
		self._ui.swap_widget("GameSettingsUI")

	def enable_next_screen_button(self):
		if not self.next_screen_button_enabled:
			print "Enabled: next screen button"
			self.next_screen_button.text = "Next"
			self.next_screen_button.bind(on_release=self.next_screen)
			self.next_screen_button_enabled = True

	def add_player(self):
		player_name = self.player_name_input.text
		if not player_name : return
		try:
			player_birthyear = self.player_year_input.adapter.selection[0].text
		except:
			player_birthyear = ""
			return
		print player_name, player_birthyear

		if player_name and player_birthyear:
			self.players.append((player_name, player_birthyear))
			print self.players
			self.enable_next_screen_button()
		player_display = ["%s, %s" % x for x in self.players]
		self.player_info_display.item_strings = player_display
		self.player_name_input.text = "Another sample player"
		if self.player_year_input.adapter.selection:
			# self.player_year_input.adapter.set_data_item_selection(player_birthyear, False)
			# self.player_year_input.adapter.selection.is_selected = False
			# self.player_year_input.adapter.data.remove(player_birthyear)
			self.player_year_input.adapter.delete_cache()
			self.player_year_input._trigger_reset_populate()

class GameSettingsUI(GridLayout):
	def __init__(self, **kwargs):
		GridLayout.__init__(self, **kwargs)
		size = Window.size

	def set_ui_reference(self, ui):
		self._ui = ui	

	def next_screen(self):
		print "Clicked: next screen"
		pass
		# get settings from the page
		
		#if self.next_screen_button is None:
			
		#	self.next_screen_button.bind(on_press=app.root.begin_game(players))

    ## Deleting an item from a list:
    # if self.player_year_input.adapter.selection:
		# self.player_year_input.adapter.data.remove(player_birthyear)
		# self.player_year_input._trigger_reset_populate()


	# def test_add(self):
	# 	print "Clicked: add player"
	# 	player_name = self.player_name_input.text
	# 	if player_name != "":
	# 		self.players.append(player_name)
	# 	print "Players added so far:", self.players
	# 	display_string = self.players
	# 	self.player_info_display.item_strings = display_string

	# 	print self.player_birthyear_input.adapter.selection[0].text
	# 	# self.player_birthyear_input.adapter.data

class ClimateConversationsApp(App):
	def build(self):
		root_element = BoxLayout()
		ui = UIManager(root_element)
		return root_element
	pass

if __name__ == '__main__':
	w = ClimateConversationsApp()
	ClimateConversationsApp.run(w)

	#"1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992"