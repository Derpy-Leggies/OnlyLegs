"""
OnlyLegs - Theme Manager
"""
import os
import sys
import shutil
from datetime import datetime
import sass


class CompileTheme():
    """
    Compiles the theme into the static folder
    """
    def __init__(self, theme_name, app_path):
        """
        Initialize the theme manager
        Compiles the theme into the static folder and loads the fonts
        """

        print(f"Loading '{theme_name}' theme...")

        theme_path = os.path.join(app_path, 'themes', theme_name)
        theme_dest = os.path.join(app_path, 'static', 'theme')

        if not os.path.exists(theme_path):
            print("Theme does not exist!")
            sys.exit(1)

        self.load_sass(theme_path, theme_dest)
        self.load_fonts(theme_path, theme_dest)

        now = datetime.now()
        print(f"{now.hour}:{now.minute}:{now.second} - Done!\n")

    def load_sass(self, source_path, css_dest):
        """
        Compile the sass (or scss) file into css and save it to the static folder
        """
        if os.path.join(source_path, 'style.sass'):
            sass_path = os.path.join(source_path, 'style.sass')
        elif os.path.join(source_path, 'style.scss'):
            sass_path = os.path.join(source_path, 'style.scss')
        else:
            print("No sass file found!")
            sys.exit(1)

        with open(os.path.join(css_dest, 'style.css'), encoding='utf-8') as file:
            try:
                file.write(sass.compile(filename=sass_path,output_style='compressed'))
            except sass.CompileError as err:
                print("Failed to compile!\n", err)
                sys.exit(1)

            print("Compiled successfully!")

    def load_fonts(self, source_path, font_dest):
        """
        Copy the fonts folder to the static folder
        """
        # Append fonts to the destination path
        source_path = os.path.join(source_path, 'fonts')
        font_dest = os.path.join(font_dest, 'fonts')

        if os.path.exists(font_dest):
            print("Updating fonts...")
            try:
                shutil.rmtree(font_dest)
            except Exception as err:
                print("Failed to remove old fonts!\n", err)
                sys.exit(1)

        try:
            shutil.copytree(source_path, font_dest)
            print("Copied new fonts!")
        except Exception as err:
            print("Failed to copy fonts!\n", err)
            sys.exit(1)
