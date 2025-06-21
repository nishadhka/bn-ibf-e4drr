import csv
import random

from globals import LEAF_NODE_NAMES


def generate_leaf_nodes_csv(path, num_rows=25):
    """
    This method generates a csv file (synthetic dataset) that has columns
    FAR, HT, AUROC and TriggerDecision. The first three columns are
    probabilities (given in bin units) whereas TriggerDecision = 0 or 1.
    num_rows is the number of rows, not counting first line (header).

    Parameters
    ----------
    path: str
    num_rows: int

    Returns
    -------
    None

    """
    # Set random seed for reproducibility (optional)
    random.seed(42)

    # Define the data
    data = []
    for i in range(num_rows):
        row = {
            'FAR': round(random.uniform(0, 1), 6),
            'HR': round(random.uniform(0, 1), 6),
            'AUROC': round(random.uniform(0, 1), 6),
            'TriggerDecision': random.choice([0, 1])
        }
        data.append(row)

    # Write to CSV file
    with open(path, 'w', newline='') as csvfile:
        fieldnames = LEAF_NODE_NAMES
        fieldnames.append('TriggerDecision')
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data rows
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    def main():
        generate_leaf_nodes_csv("data/leaf-nodes.csv")
    main()