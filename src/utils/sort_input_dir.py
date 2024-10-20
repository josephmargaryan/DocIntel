import os
from datetime import datetime


def sort_images_by_time(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Define a function to extract the datetime from the filename
    def extract_datetime(filename):
        # Remove 'Skærmbillede 2024-10-20 kl. ' and '.png' from filename to extract time
        time_part = filename.replace("Skærmbillede 2024-10-20 kl. ", "").replace(
            ".png", ""
        )
        # Convert time part into a datetime object
        return datetime.strptime(time_part, "%H.%M.%S")

    # Sort files based on extracted datetime
    sorted_files = sorted(files, key=extract_datetime)

    # Print the sorted filenames
    for file in sorted_files:
        print(file)


# Example usage:
directory = "/Users/josephmargaryan/Desktop/DocIntel/input_documents"
sort_images_by_time(directory)
