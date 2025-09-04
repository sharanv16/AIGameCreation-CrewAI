#!/usr/bin/env python
import sys
import warnings
import os
import time
import json
import litellm
from datetime import datetime

sys.path.append(os.path.abspath("./"))

os.environ["OPENAI_API_KEY"] = "API_KEY"

from src.game_version_v1.crew.GameVersionV1 import GameVersionV1

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

PROGRESS_FILE = "game_outputs/progress.json"

def save_progress(task_name):
    progress = {"last_task": task_name}
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"last_task": None}

def run():
    inputs = {
        "template_path": "GameTemplate.html",
        "platform": "mobile + desktop",
        "difficulty": "intermediate",
        "player_features": ["torchlight", "dynamic maze", "hidden keys"]
    }

    with open(inputs["template_path"], "r") as file:
        template_content = file.read()

    inputs["html_template"] = template_content

    try:
        crew_obj = GameVersionV1().crew()

        output_dir = "game_outputs"
        os.makedirs(output_dir, exist_ok=True)

        progress = load_progress()
        print(f"Resuming from last task: {progress['last_task']}")

        # Retry logic for kickoff
        while True:
            try:
                result = crew_obj.kickoff(inputs=inputs)
                break  # Exit the loop if successful
            except litellm.RateLimitError as e:
                retry_time = 30  # Default retry time in seconds
                if hasattr(e, "message") and "Please try again in" in str(e):
                    try:
                        retry_time = float(str(e).split("Please try again in")[1].split("s")[0].strip())
                    except ValueError:
                        pass
                print(f"Rate limit reached. Retrying in {retry_time} seconds...")
                time.sleep(retry_time)

        # Write task outputs to files
        for task in crew_obj.tasks:
            task_output = task.output
            task_name = task.name.replace(" ", "_").lower()
            filename = f"{task_name}_output.txt"
            file_path = os.path.join(output_dir, filename)

            # Check if the task was already completed
            if progress["last_task"] and task_name <= progress["last_task"]:
                print(f"Skipping already completed task: {task_name}")
                continue

            # Append task output to the file
            with open(file_path, "a") as f:
                f.write(str(task_output or "No output.") + "\n")

            # Save progress after each task
            save_progress(task_name)

        # Append the final result to a file
        with open("game_outputs/crew_output.txt", "a") as f:
            f.write(str(result) + "\n")
        print("Output appended to 'game_outputs/crew_output.txt'")

    except Exception as e:
        raise Exception(f"❌ Error running crew: {e}")

if __name__ == "__main__":
    run()
