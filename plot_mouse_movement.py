import numpy as np
import matplotlib.pyplot as plt
import math

def main():
    """
    Loads mouse_data.npy and plots each trial's mouse trajectory in 2D (X vs Y).
    Creates subplots (one per trial).
    """
    npy_filename = "mouse_data.npy"

    try:
        mouse_data = np.load(npy_filename, allow_pickle=True)
    except FileNotFoundError:
        print(f"Error: {npy_filename} not found. Make sure it exists.")
        return
    
    if len(mouse_data) == 0:
        print("No mouse data available to plot.")
        return

    total_trials = len(mouse_data)
    # Figure out a suitable grid (e.g., up to 3 columns)
    ncols = min(total_trials, 3)
    nrows = math.ceil(total_trials / ncols)
    
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(5*ncols, 5*nrows))
    if nrows == 1 and ncols == 1:
        # If there's only one trial, axes is not a 2D array
        axes = [[axes]]

    # Convert axes to 2D array for easier indexing
    ax_array = np.atleast_2d(axes)

    # Colors for categories
    colors = {"similar": "blue", "unrelated": "red", "gibberish": "green"}

    for idx, trial_record in enumerate(mouse_data):
        row = idx // ncols
        col = idx % ncols
        
        trial_ax = ax_array[row, col]

        # Safely retrieve values from the dictionary
        initial_word = trial_record.get("initial_word", "unknown_first")
        second_word = trial_record.get("second_word", "unknown_second")
        category = trial_record.get("system_category", "unknown_category")
        user_response = trial_record.get("user_response", "N/A")
        positions = trial_record.get("mouse_positions", [])

        xs = [pos[0] for pos in positions]
        ys = [pos[1] for pos in positions]

        color = colors.get(category, "gray")

        trial_ax.plot(xs, ys, color=color, marker="o", markersize=2, linewidth=1)
        trial_ax.set_title(f"Trial {idx+1}\n"
                           f"{initial_word} → {second_word}\n"
                           f"Category: {category} / Response: {user_response}")
        trial_ax.set_xlabel("X position")
        trial_ax.set_ylabel("Y position")
        trial_ax.grid(True)

    # Adjust layout so subplots don't overlap
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
