import datetime
now = datetime.datetime.now()

import sys
import shutil
import os
import sass


class compile():
    def __init__(self, theme, dir):
        print(f"Loading '{theme}' theme...")

        theme_path = os.path.join(dir, 'themes', theme)
        font_path = os.path.join(dir, 'themes', theme, 'fonts')
        dest = os.path.join(dir, 'static', 'theme')

        # print(f"Theme path: {theme_path}")

        if os.path.exists(theme_path):
            if os.path.exists(os.path.join(theme_path, 'style.scss')):
                theme_path = os.path.join(theme_path, 'style.scss')
            elif os.path.exists(os.path.join(theme_path, 'style.sass')):
                theme_path = os.path.join(theme_path, 'style.sass')
            else:
                print("Theme does not contain a style file!")
                sys.exit(1)

            self.sass = sass

            self.loadTheme(theme_path, dest)
            self.loadFonts(font_path, dest)
        else:
            print("No theme found!")
            sys.exit(1)

        print(f"{now.hour}:{now.minute}:{now.second} - Done!\n")

    def loadTheme(self, theme, dest):
        with open(os.path.join(dest, 'style.css'), 'w') as f:
            try:
                f.write(
                    self.sass.compile(filename=theme,
                                      output_style='compressed'))
                print("Compiled successfully!")
            except self.sass.CompileError as e:
                print("Failed to compile!\n", e)
                sys.exit(1)

    def loadFonts(self, source, dest):
        dest = os.path.join(dest, 'fonts')

        if os.path.exists(dest):
            print("Updating fonts...")
            try:
                shutil.rmtree(dest)
            except Exception as e:
                print("Failed to remove old fonts!\n", e)
                sys.exit(1)

        try:
            shutil.copytree(source, dest)
            # print("Copied fonts to:", dest)
            print("Copied new fonts!")
        except Exception as e:
            print("Failed to copy fonts!\n", e)
            sys.exit(1)