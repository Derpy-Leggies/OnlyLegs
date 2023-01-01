import sys
import os

class Sassy():
    def __init__(self, theme):
        try:
            import sass
        except ImportError:
            print("Error: sass not found")
            sys.exit(1)
        
        path_to_sass = os.path.join('./usr', 'themes', theme, 'style.scss')
        
        if os.path.exists(path_to_sass):
            print("Sass found at: " + path_to_sass)
            self.sass = sass
            self.loadTheme(path_to_sass)
        else:
            print("Error: theme not found")
            sys.exit(1)
    
    def loadTheme (self, theme):
        with open('static/css/style.css', 'w') as f:
            try:
                f.write(self.sass.compile(filename=theme, output_style='compressed'))
                print("Sass compiled successfully to: " + f.name)
            except self.sass.CompileError as e:
                print("Error: sass compilation failed:\n", e)