from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListItemButton
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.logger import Logger
import re


class AddPlayersUI(BoxLayout):
	def __init__(self, **kwargs):
		BoxLayout.__init__(self, **kwargs)
		self.players = []			
		self.selected_year = None
		self.next_screen_button_enabled = False

		print "Beginning widget walk:"
		for widget in self.walk():
			print ("{} -> {}").format(widget, widget.id)
		print "End of widget walk."

	def set_ui_reference(self, ui):
		self._ui = ui

	def back_to_intro(self):
		Logger.debug("AddPlayersUI: Clicked back to intro button")
		self._ui.swap_widget("IntroUI")

	def next_screen(self, button):
		Logger.debug("AddPlayersUI: Clicked next screen button")
		self._ui.swap_widget("GameSettingsUI")

	def enable_next_screen_button(self):
		if not self.next_screen_button_enabled:
			Logger.debug("AddPlayersUI: Enabled next screen button")
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
		Logger.info("AddPlayersUI: Player input: %s, %s" % (player_name, player_birthyear))

		if player_name and player_birthyear:
			self.players.append((player_name, player_birthyear))
			debug_str = "; ".join([x[0] + " " + str(x[1]) for x in self.players])
			Logger.info("AddPlayersUI: Players so far: %s" % debug_str)
			self.enable_next_screen_button()
		player_display = ["%s, %s" % x for x in self.players]
		self.player_info_display.item_strings = player_display
		self.player_name_input.text = "Another sample player"
		if self.player_year_input.adapter.selection:
			# TODO fix -- stopped resetting completely
			# self.player_year_input.adapter.set_data_item_selection(player_birthyear, False)
			# self.player_year_input.adapter.selection.is_selected = False
			# self.player_year_input.adapter.data.remove(player_birthyear)
			self.player_year_input.adapter.delete_cache()
			self.player_year_input._trigger_reset_populate()


class YearSelectorButton(ListItemButton):
	def register_press(self):
		Logger.debug("YearSelector: Clicked year %s" % self.text)
	pass


class IntInput(TextInput):
	def insert_text(self, input_string, from_undo=False):
		int_re = re.compile("[0-9]*")
		ints = re.findall(int_re, input_string)
		if len(ints) > 0:
			int_string = ints[0]
		else:
			Logger.debug("IntInput: Disallowed character %s" % input_string)
		return super(IntInput, self).insert_text(int_string, from_undo=from_undo)


class GameSettingsUI(GridLayout):
	def __init__(self, **kwargs):
		GridLayout.__init__(self, **kwargs)
		size = Window.size

	def set_ui_reference(self, ui):
		self._ui = ui	

	def next_screen(self):
		Logger.debug("GameSettingsUI: Clicked next screen button")
		pass