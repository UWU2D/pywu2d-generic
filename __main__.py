import sys
import os
FILE_PATH = os.path.dirname(__file__)

sys.path.extend([os.path.join(FILE_PATH, 'drawable'), os.path.join(
    FILE_PATH, 'math'), os.path.join(FILE_PATH, 'sprite')])

if __name__ == "__main__":
    from pywu2dclient import main_loop
    from client import create

    main_loop(create)
