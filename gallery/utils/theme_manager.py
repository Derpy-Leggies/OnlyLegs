"""
OnlyLegs - Theme Manager
"""
import os
import sys
import shutil
from datetime import datetime
import sass
import json


def compile_theme(theme_name, app_path):
    """
    Compiles the theme into the static folder
    """
    print(f"Loading '{theme_name}' theme...")

    # Set Paths
    theme_source = os.path.join(app_path, 'themes', theme_name)
    theme_target = os.path.join(app_path, 'static', 'theme')

    # If the theme doesn't exist, exit
    if not os.path.exists(theme_source):
        print("Theme does not exist!")
        sys.exit(1)

    # If the destination folder doesn't exist, create it
    if not os.path.exists(theme_target):
        os.makedirs(theme_target)

    # Theme source file doesn't exist, exit
    if not os.path.join(theme_source, 'style.sass'):
        print("No sass file found!")
        sys.exit(1)

    # Check if the theme has a manifest.json file
    if os.path.exists(os.path.join(theme_source, 'manifest.json')):
        source_info = json.load(open(os.path.join(theme_source, 'manifest.json'), encoding='utf-8', mode='r'))
    else:
        print("Theme lacks a manifest.json file, exiting as its required!")
        sys.exit(1)

    # Check if the theme is upto date
    if os.path.exists(os.path.join(theme_target, 'manifest.json')):
        target_info = json.load(open(os.path.join(theme_target, 'manifest.json'), encoding='utf-8', mode='r'))
    
        if source_info['version'] == target_info['version'] and source_info['name'] == target_info['name']:
            print("Theme is up to date!")
            return

    # Compile the theme
    with open(os.path.join(theme_target, 'style.css'),
              encoding='utf-8', mode='w+') as file:
        try:
            file.write(sass.compile(filename=os.path.join(theme_source, 'style.sass'),
                                    output_style='compressed'))
        except sass.CompileError as err:
            print("Failed to compile!\n", err)
            sys.exit(1)
        print("Compiled successfully!")

    # If the destination folder exists, remove it
    if os.path.exists(os.path.join(theme_target, 'fonts')):
        shutil.rmtree(os.path.join(theme_target, 'fonts'))

    # Copy the fonts
    shutil.copytree(os.path.join(theme_source, 'fonts'),
                    os.path.join(theme_target, 'fonts'))
    print("Fonts copied successfully!")
    
    # Copy the manifest
    shutil.copyfile(os.path.join(theme_source, 'manifest.json'),
                    os.path.join(theme_target, 'manifest.json'))
    print("Manifest copied successfully!")

    print(f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second} - Done!\n")
