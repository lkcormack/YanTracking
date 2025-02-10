import numpy as np
from psychopy import visual, core, event
import random
import csv
import matplotlib.pyplot as plt

# === Experiment Setup ===
# Open a full-screen window for the experiment
win = visual.Window(size=(1920, 1080), fullscr=True, color="black", units="pix")

# Settings
max_trials = 5       # Fixed number of trials
isi_duration = 0.5   # Inter-stimulus interval in seconds
mouse_tracking_time = 2.5  # Track mouse for 2.5 seconds

# === Load Dataset from CSV ===
def load_dataset(csv_filename):
    """
    Load dataset from 'word_dataset.csv'.
    The file must have columns: initial_word, similar, unrelated, gibberish
    Each row is one initial_word with comma-separated options for each category.
    """
    dataset = {}
    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            initial_word = row["initial_word"].strip()
            dataset[initial_word] = {
                "similar": [word.strip() for word in row["similar"].split(",")],
                "unrelated": [word.strip() for word in row["unrelated"].split(",")],
                "gibberish": [word.strip() for word in row["gibberish"].split(",")],
            }
    return dataset

# Load our dictionary of words from the CSV
dataset = load_dataset("word_dataset.csv")

def show_instructions():
    """
    Display instructions to the participant and wait for any key press to continue.
    In this variant, we use the mouse movement to indicate "similar" or "unrelated":
      - Move mouse right if you think it is "similar"
      - Move mouse left if you think it is "unrelated"
    The system does not check correctness; we only record the mouse path.
    """
    instructions_text = (
        "In this experiment, you will see pairs of words.\n\n"
        "1) You will see the first word in yellow for 1 second.\n"
        "2) Then, after a brief pause, you will see the second word in green.\n\n"
        "You have 2.5 seconds to move the mouse:\n"
        "    • Move RIGHT if you think the words are similar.\n"
        "    • Move LEFT if you think they're unrelated.\n"
        "    (We aren't checking correctness — just recording your mouse movement.)\n\n"
        "Press any key to begin."
    )

    instructions = visual.TextStim(
        win,
        text=instructions_text,
        color="white",
        height=30,
        wrapWidth=800
    )
    instructions.draw()
    win.flip()
    event.waitKeys()

def run_trial(initial_word, trial_data, mouse_records):
    """
    Present two words per trial:
      (1) Show the first word (yellow) for 1 second (no user response needed).
      (2) Inter-stimulus interval (blank) for isi_duration seconds.
      (3) Show second word (green) and track mouse for 2.5 seconds.
    We do NOT determine correctness or user response. We simply store the data.
    """
    # Randomly pick a category for the second word
    category = random.choice(["similar", "unrelated", "gibberish"])
    second_word = random.choice(dataset[initial_word][category])

    # === First Word ===
    first_word_stim = visual.TextStim(win, text=initial_word, color="yellow", height=50)
    first_word_stim.draw()
    win.flip()
    core.wait(1.0)  # Show first word for 1 second

    # === ISI ===
    win.color = "black"
    win.flip()
    core.wait(isi_duration)

    # === Second Word ===
    second_word_stim = visual.TextStim(win, text=second_word, color="green", height=50)
    second_word_stim.draw()
    win.flip()

    # Track mouse for the given time, but no user key response
    mouse = event.Mouse(visible=False, win=win)
    mouse.setPos([0, 0])  # Optionally re-center the mouse

    mouse_positions = []
    mouse_times = []
    clock = core.Clock()
    clock.reset()

    # For 2.5 seconds, record mouse position each frame
    while clock.getTime() < mouse_tracking_time:
        current_time = clock.getTime()
        second_word_stim.draw()
        win.flip()

        # Store mouse position
        pos = mouse.getPos()
        mouse_positions.append(pos)
        mouse_times.append(current_time)

        core.wait(0.01)  # small delay

    # === Save summary (trial_data) ===
    # We no longer store user_response or correctness. Use placeholders if desired.
    trial_data.append({
        "initial_word": initial_word,
        "second_word": second_word,
        "system_category": category,
        "user_response": "N/A",   # placeholder
        "correct": "N/A",         # placeholder
        "reaction_time": "N/A",   # placeholder
    })

    # === Save mouse record (mouse_records) ===
    mouse_records.append({
        "initial_word": initial_word,
        "second_word": second_word,
        "system_category": category,
        "mouse_positions": mouse_positions,  # list of (x, y)
        "mouse_times": mouse_times           # list of float times
    })

def plot_mouse_trajectories(mouse_data):
    """
    Plot y-direction mouse trajectories colored by category.
    """
    colors = {"similar": "blue", "unrelated": "red", "gibberish": "green"}

    plt.figure()
    for trial in mouse_data:
        positions = trial["mouse_positions"]
        category = trial["system_category"]
        y_data = [pos[1] for pos in positions]

        color = colors.get(category, "gray")
        plt.plot(y_data, color=color, alpha=0.7, label=category)

    plt.xlabel("Sample index")
    plt.ylabel("Mouse Y-position")
    plt.title("Mouse Trajectories (Y-direction)")
    handles, labels = plt.gca().get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    plt.legend(unique_labels.values(), unique_labels.keys())
    
    plt.ion()  # Interactive mode so it doesn't block
    plt.show()
    plt.pause(0.1)

def main():
    try:
        show_instructions()

        trial_data = []
        mouse_data = []

        # Pick some random words for the session
        all_words = list(dataset.keys())
        session_words = random.sample(all_words, min(max_trials, len(all_words)))

        for word in session_words:
            run_trial(word, trial_data, mouse_data)

        # --- Save Trial Metadata to CSV ---
        # We'll keep the same columns as before, but it's mostly placeholders now.
        with open('trial_metadata.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                "initial_word", "second_word", "system_category",
                "user_response", "correct", "reaction_time"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(trial_data)

        # --- Save Mouse Data to a NumPy File ---
        np.save('mouse_data.npy', mouse_data, allow_pickle=True)

        # --- Summary in Console ---
        print("\n--- EXPERIMENT SUMMARY ---")
        print(f"Total Trials: {len(trial_data)}")
        print("No correctness check. Mouse data recorded for each trial.")

    except Exception as exc:
        print(f"An error occurred: {exc}")
    finally:
        # Close the PsychoPy window
        if 'win' in locals() and win:
            win.close()
        core.quit()
        event.Mouse(visible=True)

    # Plot the mouse data
    plot_mouse_trajectories(mouse_data)

if __name__ == "__main__":
    main()
