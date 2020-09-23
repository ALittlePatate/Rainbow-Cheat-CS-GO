import keyboard
import ctypes
import time
from Offsets import *

rapidfire = True
def main():

        #On cherche le nom de la config actuelle
        with open("configs/path.txt") as path_txt :
            path = path_txt.readline()
            path_txt.close()

        #On ouvre la config et on en tire la variable delay_mh
        with open("configs/"+path) as config_file :
            line_nmb = 0
            for line in config_file :
                line_nmb = line_nmb + 1
                if line_nmb == 13 :
                    rapidbutton = line
                    rapidbutton = rapidbutton.replace(" ", "")
                    rapidbutton = rapidbutton.replace("\n", "")
                if line_nmb >= 14  :
                    config_file.close()
                    break

        while True:
            time.sleep(0.15)
            while rapidfire:
                time.sleep(0.01)
                if keyboard.is_pressed(rapidbutton):
                    while True :
                        ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
                        time.sleep(0.01)
                        ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
                        time.sleep(0.01)
                        if not keyboard.is_pressed(rapidbutton) :
                            break

if __name__ == '__main__':
    main()