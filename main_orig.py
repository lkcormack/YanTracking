import csv
from psychopy import visual, core, event, data
import random

# === Experiment Setup ===
# Open a full-screen window for the experiment
win = visual.Window(size=(1920, 1080), fullscr=True, color="black", units="pix")

# Settings
max_trials = 2  # Fixed number of trials

# === Load Dataset from CSV ===
def load_dataset(csv_filename):
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

# Load the dataset from a CSV file
dataset = load_dataset("word_dataset.csv")

def show_instructions():
    instructions = visual.TextStim(
        win, 
        text="In this experiment, you will see pairs of words.\n\n" +
             "For each pair, decide if the second word is:\n\n" +
             "1: Similar to the first word\n" +
             "2: Unrelated to the first word\n" +
             "3: Not a real word (Gibberish)\n\n" +
             "Press any key to begin.",
        color="white",
        height=30,
        wrapWidth=800
    )
    instructions.draw()
    win.flip()
    event.waitKeys()  # Wait for any key press
    
    # Brief pause before starting trials
    win.flip()
    core.wait(1) # pause for 1 second
   
def run_trial(initial_word, trial_data):
    # Reset and pause before starting new trial
    win.color = "black"
    win.flip()
    core.wait(1)  # 1 second pause between trials
    
    # Randomly choose category first (similar, unrelated, or gibberish)
    category = random.choice(["similar", "unrelated", "gibberish"])
    # Then choose a word from that category
    second_word = random.choice(dataset[initial_word][category])
    
    # Create text stimuli
    label = visual.TextStim(win, text="First word:", color="white", height=30, pos=(0, 100))
    word_stim = visual.TextStim(win, text=initial_word, color="white", height=50)
    
    # Show first word
    label.draw()
    word_stim.draw()
    win.flip()
    core.wait(2)  # Show for 2 seconds

    # Fade out first word
    for opacity in range(100, -1, -5):
        label.opacity = opacity/100
        word_stim.opacity = opacity/100
        label.draw()
        word_stim.draw()
        win.flip()
        core.wait(0.016)

    # Brief pause with blank screen
    win.flip()
    core.wait(0.3)

    # Reset opacity for second word
    label.opacity = 1.0
    word_stim.opacity = 1.0
    
    # Update text for second word
    label.text = "Second word:"
    word_stim.text = second_word
    
    # Show second word
    label.draw()
    word_stim.draw()
    win.flip()

    # Start timer and wait for user response
    timer = core.Clock()
    keys = event.waitKeys(
        keyList=["1", "2", "3", "escape"], timeStamped=timer
    )

    if keys:
        key, reaction_time = keys[0]
        if key == "escape":  # Allow user to quit experiment
            win.close()
            core.quit()
        if key == "1":
            user_response = "similar"
        elif key == "2":
            user_response = "unrelated"
        elif key == "3":
            user_response = "gibberish"
        else:
            user_response = "unknown"

    # Record trial data
    trial_data.append({
        "initial_word": initial_word,
        "second_word": second_word,
        "system_category": category,
        "user_response": user_response,
        "reaction_time": reaction_time,
    })

    # Fade out second word
    for opacity in range(100, -1, -5):
        label.opacity = opacity/100
        word_stim.opacity = opacity/100
        label.draw()
        word_stim.draw()
        win.flip()
        core.wait(0.016)

    # Additional pause before next trial
    win.flip()
    core.wait(0.5)

used_words = set()  # Track which initial words have been used

def main():
    # Show instructions at the start
    show_instructions()
    
    # Define experiment parameters
    trial_data = []
    
    # Create a list of all available words from the dataset
    all_words = list(dataset.keys())
    
    # Ensure we have enough words for the trials
    if len(all_words) < max_trials:
        print(f"Warning: Only {len(all_words)} words available for {max_trials} trials")
        current_max_trials = len(all_words)  # Create new variable instead of modifying global
    else:
        current_max_trials = max_trials
    
    # Randomly select words for this session
    session_words = random.sample(all_words, current_max_trials)
    
    # Loop through trials
    for trial in range(current_max_trials):
        initial_word = session_words[trial]
        run_trial(initial_word, trial_data)

    try:
        # Save data to CSV
        csv_filename = 'word_verification_results.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['initial_word', 'second_word', 'system_category', 
                         'user_response', 'reaction_time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in trial_data:
                writer.writerow(record)
        print(f"Results saved to {csv_filename}")

    except Exception as e:
        print(f"Error saving data: {str(e)}")
        event.waitKeys()

    # Close window
    win.close()
    core.quit()

if __name__ == "__main__":
    main()