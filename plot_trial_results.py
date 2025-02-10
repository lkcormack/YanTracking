import csv
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def main():
    """
    Reads trial_metadata.csv, computes accuracy per category,
    and plots a bar chart of the results.
    """
    csv_filename = "trial_metadata.csv"
    category_counts = defaultdict(lambda: {"correct": 0, "total": 0})

    # --- 1) Read CSV and Tally Results ---
    try:
        with open(csv_filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cat = row["system_category"]
                correct_val = int(row["correct"])  # '0' or '1'
                category_counts[cat]["correct"] += correct_val
                category_counts[cat]["total"] += 1
    except FileNotFoundError:
        print(f"Error: {csv_filename} not found. Make sure it exists.")
        return

    categories = list(category_counts.keys())
    if len(categories) == 0:
        print("No data found in trial_metadata.csv. Nothing to plot.")
        return

    # --- 2) Compute Accuracy ---
    accuracies = []
    for cat in categories:
        ccount = category_counts[cat]["correct"]
        tcount = category_counts[cat]["total"]
        accuracy = (ccount / tcount) * 100 if tcount > 0 else 0
        accuracies.append(accuracy)

    # --- 3) Plot Bar Chart ---
    plt.figure(figsize=(8, 5))
    x_positions = np.arange(len(categories))
    plt.bar(x_positions, accuracies, color="skyblue")
    plt.xticks(x_positions, categories, fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylabel("Accuracy (%)", fontsize=14)
    plt.xlabel("Category", fontsize=14)
    plt.title("Accuracy per Category", fontsize=16)
    plt.ylim([0, 100])

    # Show numeric accuracy on each bar
    for i, acc in enumerate(accuracies):
        plt.text(i, acc + 1, f"{acc:.1f}%", ha="center", fontsize=12)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main() 