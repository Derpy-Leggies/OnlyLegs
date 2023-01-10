import datetime
now = datetime.datetime.now()
import sys
import shutil
import os
import sass

class compile():
    def __init__(self, theme):
        print(f"Loading '{theme}' theme...")
        
        theme_path = os.path.join('./user', 'themes', theme, 'style.scss')
        font_path = os.path.join('./user', 'themes', theme, 'fonts')
        
        print(f"Theme path: {theme_path}")
        
        if os.path.exists(theme_path):
            self.sass = sass
            
            self.loadTheme(theme_path)
            self.loadFonts(font_path)
        else:
            print("No theme found!")
            sys.exit(1)
        
        print(f"{now.hour}:{now.minute}:{now.second} - Done!\n")
    
    def loadTheme (self, theme):
        with open('static/theme/style.css', 'w') as f:
            try:
                f.write(self.sass.compile(filename=theme, output_style='compressed'))
                print("Compiled successfully to:", f.name)
            except self.sass.CompileError as e:
                print("Failed to compile!\n", e)
                sys.exit(1)
    
    def loadFonts (self, font_path):
        dest = os.path.join('./static', 'theme', 'fonts')
        
        if os.path.exists(dest):
            print("Removing old fonts...")
            try:
                shutil.rmtree(dest)
            except Exception as e:
                print("Failed to remove old fonts!\n", e)
                sys.exit(1)
        
        try:
            shutil.copytree(font_path, dest)
            print("Copied fonts to:", dest)
        except Exception as e:
            print("Failed to copy fonts!\n", e)
            sys.exit(1)