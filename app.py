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
from createWorkouts import CreateWorkouts
from updateWeight import UpdateWeight


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
            self.app.pop_screen()
            self.app.push_screen(MainScreen(self.usr_info))

class MainScreen(Screen):
    def __init__(self, usr_info: UsrData):
        super().__init__()
        self.usr_info = usr_info
    
    def compose(self):
        with Vertical():
            yield Label(f"Welcome, {self.usr_info.usr_name}!")
            yield Label(f"Current Weight: {self.usr_info.usr_weight} lbs")
            yield Label(f"Target Weight: {self.usr_info.usr_target} lbs")
            
            weight_diff = self.usr_info.get_weight_difference()
            if weight_diff > 0:
                yield Label(f"Goal: Lose {weight_diff:.1f} lbs")
            elif weight_diff < 0:
                yield Label(f"Goal: Gain {abs(weight_diff):.1f} lbs")
            else:
                yield Label("🎉 You're at your target weight!")
            
            #yield Button("Log Workout", id="workout")
            yield Button("Update Weight", id="update_weight")
            yield Button("Add Lift", id="add_lift")
            yield Button(label="Add Workout", id="add_workout")
            yield Label("", id="status")


    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "update_weight":
            self.app.push_screen(UpdateWeight(self.usr_info))
        elif event.button.id == "add_lift":
            status_label = self.query_one("#status")
            status_label.update("Add Lift Not implimented yet")  # pyright: ignore[reportAttributeAccessIssue]
            #self.app.push_screen()
        elif event.button.id == "add_workout":
            #status_label = self.query_one("#status")
            #status_label.update("Add Workout not implimented yet")  # pyright: ignore[reportAttributeAccessIssue]
            self.app.push_screen(CreateWorkouts(self.usr_info))






class MyApp(App):
    def __init__(self):
        super().__init__()
        self.usr_info = UsrData()

    def on_mount(self):
        self.theme = "tokyo-night"
        self.theme = "nord"
        if self.usr_info.need_login():
            self.push_screen(Login(self.usr_info))
        else:
            self.usr_info.set_starting_vals()
            self.push_screen(MainScreen(self.usr_info))


