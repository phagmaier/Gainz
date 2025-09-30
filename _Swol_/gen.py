import random
from pathlib import Path

lifts_dir = Path("Lifts")
workouts_dir = Path("Workouts")

lifts = ["bench press", "bicep curls", "squats", "deadlifts", "lunges", "lateral raises", "skull crushers"]
workouts = ["Workout 1", "Workout 2", "Workout 3", "Workout 4"]

sample_size = 3

def gen_lifts():
    lifts_dir.mkdir(parents=True, exist_ok=True)
    for lift in lifts:
        lift = lift + ".txt"
        fName = lifts_dir / lift
        fName.touch()

def gen_workout():
    workouts_dir.mkdir(parents=True, exist_ok=True)

    for workout in workouts:
        ran_lifts = random.sample(lifts, sample_size)
        ran_lifts = "\n".join(ran_lifts).strip()
        workout = workout + ".txt"
        f_name = workouts_dir / workout
        with open(f_name, 'w') as f:
            f.write(ran_lifts)

def main():
    gen_lifts()
    gen_workout()

if __name__ == "__main__":
    main()


