"""
OnlyLegs - Theme Manager
"""
import os
import sys
import shutil
from datetime import datetime
import sass


def compile_theme(theme_name, app_path):
    """
    Compiles the theme into the static folder
    """
    print(f"Loading '{theme_name}' theme...")

    # Set Paths
    theme_source = os.path.join(app_path, 'themes', theme_name)
    theme_destination = os.path.join(app_path, 'static', 'theme')

    # If the theme doesn't exist, exit
    if not os.path.exists(theme_source):
        print("Theme does not exist!")
        sys.exit(1)

    # If the destination folder doesn't exist, create it
    if not os.path.exists(theme_destination):
        os.makedirs(theme_destination)

    # Theme source file doesn't exist, exit
    if not os.path.join(theme_source, 'style.sass'):
        print("No sass file found!")
        sys.exit(1)

    # Compile the theme
    with open(os.path.join(theme_destination, 'style.css'),
              encoding='utf-8', mode='w+') as file:
        try:
            file.write(sass.compile(filename=os.path.join(theme_source, 'style.sass'),
                                    output_style='compressed'))
        except sass.CompileError as err:
            print("Failed to compile!\n", err)
            sys.exit(1)
        print("Compiled successfully!")

    # If the destination folder exists, remove it
    if os.path.exists(os.path.join(theme_destination, 'fonts')):
        shutil.rmtree(os.path.join(theme_destination, 'fonts'))

    # Copy the fonts
    shutil.copytree(os.path.join(theme_source, 'fonts'),
                    os.path.join(theme_destination, 'fonts'))
    print("Fonts copied successfully!")

    print(f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second} - Done!\n")
