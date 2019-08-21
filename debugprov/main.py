from debugprov.console_interface import ConsoleInterface
from debugprov.now_interface import NowInterface
from debugprov.application_controller import ApplicationController
import traceback

def main():
      try:
            app = ApplicationController()
            app.run()
      except:
            traceback.print_exc()      

if __name__ == "__main__":
    main()
