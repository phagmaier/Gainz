
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

class CreateWorkouts(Screen):
    CSS_PATH = "create_workout.tcss"
    BINDINGS = [
        Binding(key="down", action="cursor_down", description="Move down"),
        Binding(key="up", action="cursor_up", description="Move up"),
        Binding(key="enter", action="select_lift", description="Select Lift"),
        Binding(key="escape", action="go_back", description="Back"),
    ]
    
    def __init__(self, usr_info: UsrData):
        super().__init__()
        self.usr_info: UsrData = usr_info
        self.active_index = 0
        self.current_results = []
        self.workout_lifts: list[str] = []
        self.workout_name: str = ""

    def compose(self) -> ComposeResult:
        with VerticalScroll(id="main-container"):
            yield Label("Create a New Workout", id="title")
            yield Input(placeholder="Workout Name", id="workout_name")
            
            yield Label("Add Lifts:", id="add-lifts-label")
            yield Input(placeholder="Search for a lift...", id="search")
            yield Vertical(id="results")
            
            yield Label("Current Lifts in Workout:", id="current-lifts-label")
            yield Vertical(id="workout_container")

            with Horizontal(id="button-container"):
                yield Button("Submit Workout", variant="success", id="submit")
                yield Button("Back", variant="default", id="back")
            
            yield Label("", id="status")

    def on_input_changed(self, event: Input.Changed) -> None:
        event_id = event.input.id
        if event_id == "workout_name":
            self.workout_name = event.value
        elif event_id == "search":
            self._handle_search_change(event.value)

    def _handle_search_change(self, query: str) -> None:
        """Separated search logic for clarity."""
        results_container = self.query_one("#results", Vertical)
        results_container.remove_children()
        self.current_results = []

        if not query:
            results_container.remove_class("visible")
            return

        matcher = fuzzy.Matcher(query)
        scored_lifts = [
            (matcher.match(lift), lift) 
            for lift in self.usr_info.lifts
        ]
        
        # Filter and sort in one pass
        scored_lifts = [(score, lift) for score, lift in scored_lifts if score > 0]
        scored_lifts.sort(key=lambda item: item[0], reverse=True)

        if scored_lifts:
            results_container.add_class("visible")
            for score, lift in scored_lifts[:5]:
                results_container.mount(Label(lift))
                self.current_results.append(lift)
            
            self.active_index = 0
            self._update_active_highlight()
        else:
            results_container.remove_class("visible")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "search":
            self.action_select_lift()

    def _update_active_highlight(self) -> None:
        labels = self.query("#results > Label")
        if not labels:
            return

        for label in labels:
            label.remove_class("active")
        
        self.active_index = self.active_index % len(labels)
        labels[self.active_index].add_class("active")

    def action_cursor_down(self) -> None:
        self.active_index += 1
        self._update_active_highlight()

    def action_cursor_up(self) -> None:
        self.active_index -= 1
        self._update_active_highlight()

    def action_select_lift(self) -> None:
        if not self.current_results:
            return

        selected_lift = self.current_results[self.active_index]
        
        # Prevent duplicates
        if selected_lift in self.workout_lifts:
            self.query_one("#status", Label).update(f"⚠ {selected_lift} already added")
            return
        
        self.workout_lifts.append(selected_lift)
        self._add_lift_to_display(selected_lift)
        self._clear_search()

    def _add_lift_to_display(self, lift_name: str) -> None:
        """Add a lift with a delete button."""
        # Create all widgets
        lift_container = Horizontal(classes="lift-item")
        label = Label(f"• {lift_name}", classes="lift-name")
        # Replace spaces with underscores for valid ID
        safe_id = lift_name.replace(" ", "_")
        button = Button("×", classes="delete-btn", id=f"delete-{safe_id}")
        
        # Mount container to parent, then mount children to container
        self.query_one("#workout_container").mount(lift_container)
        lift_container.mount(label, button)
        
        self.query_one("#status", Label).update(f"✓ Added {lift_name}")

    def _clear_search(self) -> None:
        """Helper to clear search state."""
        self.query_one("#search", Input).value = ""
        results_container = self.query_one("#results", Vertical)
        results_container.remove_children()
        results_container.remove_class("visible")
        self.current_results = []

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        
        if button_id and button_id.startswith("delete-"):
            # Convert ID back to lift name
            safe_name = button_id.replace("delete-", "")
            lift_name = safe_name.replace("_", " ")
            self._remove_lift(lift_name, event.button.parent)  # pyright: ignore[reportArgumentType]
        elif button_id == "submit":
            self._submit_workout()
        elif button_id == "back":
            self.action_go_back()

    def _remove_lift(self, lift_name: str, container: Horizontal) -> None:
        """Remove a lift from the workout."""
        if lift_name in self.workout_lifts:
            self.workout_lifts.remove(lift_name)
            container.remove()
            self.query_one("#status", Label).update(f"✗ Removed {lift_name}")

    def _submit_workout(self) -> None:
        """Validate and submit the workout."""
        if not self.workout_name:
            self.query_one("#status", Label).update("⚠ Please enter a workout name")
            return
        
        if not self.workout_lifts:
            self.query_one("#status", Label).update("⚠ Please add at least one lift")
            return
        
        self.usr_info.write_workout(self.workout_name, self.workout_lifts)
        self.query_one("#status", Label).update(f"✓ Workout '{self.workout_name}' created!")
        # Optionally auto-close after success:
        # self.set_timer(1.5, self.action_go_back)

    def action_go_back(self) -> None:
        self.app.pop_screen()
