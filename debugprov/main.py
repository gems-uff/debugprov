from debugprov.console_interface import ConsoleInterface

# BEGIN windows only 
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
# END windows onl

def main():
      ConsoleInterface().run()

if __name__ == "__main__":
    main()
