from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.theme import Theme
from textual.screen import Screen
from textual.widgets import Button, Label, Input, ListView, ListItem, Static, option_list
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual import fuzzy
from user import UsrData
from datetime import date
import config

class UpdateWeight(Screen):
    def __init__(self, usr_info: UsrData):
        super().__init__()
        self.usr_info = usr_info
    
    def compose(self):
        with Vertical():
            yield Label("📊 Update Your Weight")
            yield Label(f"Current: {self.usr_info.usr_weight} lbs")
            yield Input(placeholder="Enter new weight", id="new_weight", type="number")
            yield Input(placeholder=f"Enter date: {config.DATE_FORMAT} (default is today)", id="date")
            yield Button("Update", id="update")
            yield Button("Back", id="back")
            yield Label("", id="status")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "update":
            new_weight = self.query_one("#new_weight").value  # pyright: ignore[reportAttributeAccessIssue]
            date_value = self.query_one("#date").value  # pyright: ignore[reportAttributeAccessIssue]
            status_label = self.query_one("#status")
            
            if not new_weight:
                status_label.update(config.MSG_WEIGHT_REQUIRED)  # pyright: ignore[reportAttributeAccessIssue]
                return
            
            success, msg = self.usr_info.update_weight(new_weight, date_value)
            status_label.update(msg)  # pyright: ignore[reportAttributeAccessIssue]
            
            if success:
                self.query_one("#new_weight").value = ""  # pyright: ignore[reportAttributeAccessIssue]
                self.query_one("#date").value = ""  # pyright: ignore[reportAttributeAccessIssue]
                current_label = self.query_one(Label)
                current_label.update(f"Current: {self.usr_info.usr_weight} lbs")  # pyright: ignore[reportAttributeAccessIssue]

        elif event.button.id == "back":
            self.app.pop_screen()
