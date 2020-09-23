import pymem
import pymem.process
import time
import math
import keyboard
from os import _exit
from Offsets import *
import ctypes
import keyboard
import re

rcsonoff = True


def normalizeAngles(viewAngleX, viewAngleY):
    if viewAngleX > 89:
        viewAngleX -= 360
    if viewAngleX < -89:
        viewAngleX += 360
    if viewAngleY > 180:
        viewAngleY -= 360
    if viewAngleY < -180:
        viewAngleY += 360
    return viewAngleX, viewAngleY


def checkangles(x, y):
    if x > 89:
        return False
    elif x < -89:
        return False
    elif y > 360:
        return False
    elif y < -360:
        return False
    else:
        return True


def nanchecker(first, second):
    if math.isnan(first) or math.isnan(second):
        return False
    else:
        return True


def main():
    try :
        pm = pymem.Pymem("csgo.exe")
    except :
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
        return

    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On ouvre la config et on en tire la variable RCSPerfectPercent
    with open("configs/"+path) as config_file :
        line_nmb = 1
        for line in config_file :
            if line_nmb == 15 :
                RCSPerfectPercent = line
            if line_nmb >= 16 :
                config_file.close()
                break
            line_nmb = line_nmb + 1
    
    RCSPerfectPercent = RCSPerfectPercent.replace("\n", "")
    RCSPerfectPercent = RCSPerfectPercent.replace(" ", "")
    RCSPerfectPercent = float(RCSPerfectPercent)


    global amount
    oldpunchx = 0.0
    oldpunchy = 0.0
    while True:
        time.sleep(0.01)
        if rcsonoff:
            rcslocalplayer = pm.read_int(client + dwLocalPlayer)
            rcsengine = pm.read_int(engine + dwClientState)
            if pm.read_int(rcslocalplayer + m_iShotsFired) > 2:
                rcs_x = pm.read_float(rcsengine + dwClientState_ViewAngles)
                rcs_y = pm.read_float(rcsengine + dwClientState_ViewAngles + 0x4)
                punchx = pm.read_float(rcslocalplayer + m_aimPunchAngle)
                punchy = pm.read_float(rcslocalplayer + m_aimPunchAngle + 0x4)
                newrcsx = rcs_x - (punchx - oldpunchx) * (RCSPerfectPercent * 0.02)
                newrcsy = rcs_y - (punchy - oldpunchy) * (RCSPerfectPercent * 0.02)
                newrcs, newrcy = normalizeAngles(newrcsx, newrcsy)
                oldpunchx = punchx
                oldpunchy = punchy
                if nanchecker(newrcsx, newrcsy) and checkangles(newrcsx, newrcsy):
                    pm.write_float(rcsengine + dwClientState_ViewAngles, newrcsx)
                    pm.write_float(rcsengine + dwClientState_ViewAngles + 0x4, newrcsy)
            else:
                oldpunchx = 0.0
                oldpunchy = 0.0
                newrcsx = 0.0
                newrcsy = 0.0
            if keyboard.is_pressed('delete'):
                _exit(0)


if __name__ == '__main__':
    main()
