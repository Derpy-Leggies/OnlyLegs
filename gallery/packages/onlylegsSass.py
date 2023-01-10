import datetime
now = datetime.datetime.now()
import sys
import shutil
import os

class Sassy():
    def __init__(self, theme):
        print("### OnlyLegs Theme Manager ###")
        print(f"{now.hour}:{now.minute}:{now.second} - Loading theme...")
        
        try:
            import sass
        except ImportError:
            print("Could not find libsass!")
            sys.exit(1)
        
        theme_path = os.path.join('usr', 'themes', theme, 'style.scss')
        
        if os.path.exists(theme_path):
            print(f"Theme '{theme}' found at:", theme_path)
            self.sass = sass
            self.loadTheme(theme_path)
        else:
            print("No theme found!")
            sys.exit(1)
            
        font_path = os.path.join('usr', 'themes', theme, 'fonts')
        
        if os.path.exists(font_path):
            print("Fonts found at:", font_path)
            self.loadFonts(font_path)
        else:
            print("No fonts found!")
        
        print(f"{now.hour}:{now.minute}:{now.second} - Done!\n")
    
    def loadTheme (self, theme):
        with open('static/theme/style.css', 'w') as f:
            try:
                f.write(self.sass.compile(filename=theme, output_style='compressed'))
                print("Compiled successfully to:", f.name)
            except self.sass.CompileError as e:
                print("Failed to compile!\nFull error:", e)
                sys.exit(1)
    
    def loadFonts (self, font_path):
        dest = os.path.join('static', 'theme', 'fonts')
        
        if os.path.exists(dest):
            print("Removing old fonts...")
            try:
                shutil.rmtree(dest)
                print("Removed old fonts!")
            except Exception as e:
                print("Failed to remove old fonts!\nFull error:", e)
                sys.exit(1)
        
        try:
            shutil.copytree(font_path, dest)
            print("Copied fonts to:", dest)
        except Exception as e:
            print("Failed to copy fonts!\nFull error:", e)
            sys.exit(1)