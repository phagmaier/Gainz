from textual.app import App
from textual.theme import Theme
from textual.screen import Screen
from textual.widgets import Button, Label, Input, ListView, ListItem, Static, option_list
from textual.containers import Vertical, Horizontal
#from rapidfuzz import fuzz, process
from textual import fuzzy
from user import UsrData
from datetime import date
import config


class Login(Screen):
    def __init__(self, usr_info: UsrData):
        super().__init__()
        self.usr_info = usr_info
        self.temp_name: str = ""
        self.temp_weight: str = ""
        self.temp_target: str = ""
    
    def compose(self):
        with Vertical():
            yield Label("🏋️ Fitness Tracker Login")
            yield Input(placeholder="Enter your name here: ", id="name_input")
            yield Input(placeholder="Enter your weight here: ", id="weight_input", type="number")
            yield Input(placeholder="Enter your target weight here: ", id="target_input", type="number")
            yield Button("Submit", id="submit")
            yield Label("", id="status")

    def on_input_changed(self, event: Input.Changed):
        """Store input values temporarily"""
        input_widget = event.input
        value = event.value
        
        if input_widget.id == "name_input":
            self.temp_name = value
        elif input_widget.id == "weight_input":
            self.temp_weight = value
        elif input_widget.id == "target_input":
            self.temp_target = value

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "submit":
            status_label = self.query_one("#status")
            
            success, msg = self.usr_info.write_usr_name(self.temp_name)
            if not success:
                status_label.update(msg)  # pyright: ignore[reportAttributeAccessIssue]
                return
            
            success, msg = self.usr_info.write_usr_weight_first(self.temp_weight)
            if not success:
                status_label.update(msg)  # pyright: ignore[reportAttributeAccessIssue]
                return
            
            success, msg = self.usr_info.write_usr_target_weight(self.temp_target)
            if not success:
                status_label.update(msg)  # pyright: ignore[reportAttributeAccessIssue]
                return
            
            status_label.update(config.MSG_LOGIN_SUCCESS)  # pyright: ignore[reportAttributeAccessIssue]
            self.app.push_screen(MainScreen(self.usr_info))
