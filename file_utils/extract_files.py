from pathlib import Path
import os


def lift_subfiles(path):
    # Get the list of files in the directory
    root = Path(path)
    # Loop through the files
    for element in root.iterdir():
        # Check if the file is a directory
        if element.is_dir():
            for subelement in element.iterdir():
                move(destination=root, source=subelement)
            # Remove the directory
            os.rmdir(element)


def move(destination, source):
    # Move the file to the parent directory
    if os.path.isfile(destination / source.name):
        source = source.rename(source.with_name(source.stem + '_' + source.suffix))
        move(destination, source)
    elif os.path.exists(destination / source.name) and os.path.isdir(destination / source.name):
        # This means there is a folder with the same name in the destination
        # folder, so we need to move the subfiles inside the existing folder
        for subelement in source.iterdir():
            move(destination / source.name, subelement)
        # Remove the directory
        os.rmdir(source)
    else:
        source.rename(destination / source.name)
