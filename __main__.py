import sys
import os
FILE_PATH = os.path.dirname(__file__)

sys.path.extend([os.path.join(FILE_PATH, 'core'), os.path.join(
    FILE_PATH, 'public'), os.path.join(FILE_PATH, 'uwu2dgeneric')])


CLIENT_TICK_RATE = 60

if __name__ == '__main__':
    from core.gameloop import main_loop
    from uwu2dgeneric.servicefactory import ServiceFactory

    main_loop(ServiceFactory(), CLIENT_TICK_RATE)
