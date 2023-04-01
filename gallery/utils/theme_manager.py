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
    THEME_SRC = os.path.join(app_path, 'themes', theme_name)
    THEME_DEST = os.path.join(app_path, 'static', 'theme')

    # If the theme doesn't exist, exit
    if not os.path.exists(THEME_SRC):
        print("Theme does not exist!")
        sys.exit(1)

    # If the destination folder doesn't exist, create it
    if not os.path.exists(THEME_DEST):
        os.makedirs(THEME_DEST)

    # Theme source file doesn't exist, exit
    if not os.path.join(THEME_SRC, 'style.sass'):
        print("No sass file found!")
        sys.exit(1)

    # Compile the theme
    with open(os.path.join(THEME_DEST, 'style.css'), encoding='utf-8', mode='w+') as file:
        try:
            file.write(sass.compile(filename=os.path.join(THEME_SRC, 'style.sass'),output_style='compressed'))
        except sass.CompileError as err:
            print("Failed to compile!\n", err)
            sys.exit(1)
        print("Compiled successfully!")
        
    # If the destination folder exists, remove it
    if os.path.exists(os.path.join(THEME_DEST, 'fonts')):
        try:
            shutil.rmtree(os.path.join(THEME_DEST, 'fonts'))
        except Exception as err:
            print("Failed to remove old fonts!\n", err)
            sys.exit(1)

    # Copy the fonts
    try:
        shutil.copytree(os.path.join(THEME_SRC, 'fonts'), os.path.join(THEME_DEST, 'fonts'))
        print("Fonts copied successfully!")
    except Exception as err:
        print("Failed to copy fonts!\n", err)
        sys.exit(1)

    print(f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second} - Done!\n")
