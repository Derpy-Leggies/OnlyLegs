import time
import sys
import os

class Sassy():
    def __init__(self, theme):
        print("### OnlyLegs Theme Manager ###")
        
        try:
            import sass
        except ImportError:
            print("Could not find libsass!")
            print("Exiting...")
            sys.exit(1)
        
        path_to_sass = os.path.join('usr', 'themes', theme, 'style.scss')
        
        if os.path.exists(path_to_sass):
            print(f"Theme '{theme}' found at:", path_to_sass)
            self.sass = sass
            self.loadTheme(path_to_sass)
        else:
            print("No theme found!")
            print("Exiting...")
            sys.exit(1)
    
    def loadTheme (self, theme):
        with open('static/css/style.css', 'w') as f:
            try:
                f.write(self.sass.compile(filename=theme, output_style='compressed'))
                print("Compiled successfully to:", f.name)#
                print("Finished\n")
            except self.sass.CompileError as e:
                print("Failed to compile! Full error:\n", e)
                print("Exiting...")
                sys.exit(1)