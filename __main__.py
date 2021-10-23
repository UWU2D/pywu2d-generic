
import sys
import os
FILE_PATH = os.path.dirname(__file__)

sys.path.extend([os.path.join(FILE_PATH, 'drawable'), os.path.join(
    FILE_PATH, 'math'), os.path.join(FILE_PATH, 'sprite')])
print(sys.path)

if __name__ == "__main__":
    from pywu2dclient import main_loop
    import uwu2dgenericclient

    main_loop(uwu2dgenericclient.create)
