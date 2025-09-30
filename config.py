from pathlib import Path

DB_DIR = "_Swol_"
USR_DIR = "Usr"
WORKOUTS_DIR = "Workouts"
LIFTS_DIR = "Lifts"

NAME_FILE = "name.txt"
WEIGHT_FILE = "weight.txt"
GOAL_FILE = "goal.txt"

DATE_FORMAT = "%m-%d-%Y"

MIN_WEIGHT = 1.0
MAX_WEIGHT = 1000.0

MSG_NAME_REQUIRED = "⌠Please enter your name"
MSG_WEIGHT_REQUIRED = "⌠Please enter a valid weight"
MSG_TARGET_REQUIRED = "⌠Please enter a valid target weight"
MSG_LOGIN_SUCCESS = "✅ Login successful!"
MSG_WEIGHT_UPDATED = "✅ Weight updated!"
MSG_DUPLICATE_DATE = "⚠️ Weight already logged for this date"
MSG_INVALID_DATE = "⌠Please enter a valid date (MM-DD-YYYY)"
MSG_INVALID_WEIGHT = f"⌠Weight must be between {MIN_WEIGHT} and {MAX_WEIGHT} lbs"
MSG_WORKOUT_LOGGED = "✅ Logged: {exercise} for {duration} minutes!"
MSG_WORKOUT_INCOMPLETE = "⌠Please fill in both fields"
