import keyboard
import pymem
import pymem.process
import time
import ctypes
from Offsets import *
from win32gui import GetWindowText, GetForegroundWindow

def main():
    try :
        pm = pymem.Pymem("csgo.exe")
    except :
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
        return
    
    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On ouvre la config et on en tire les variables delay_tg et key_tg
    with open("configs/"+path) as config_file :
        line_nmb = 1
        for line in config_file :
            if line_nmb == 2 :
                delay_tg = line
            if line_nmb == 3 :
                key_tg = line
            if line_nmb >= 4 :
                config_file.close()
                break
            line_nmb = line_nmb + 1
    
    key_tg = key_tg.replace(" ", "")
    key_tg = key_tg.replace("\n", "")
    delay_tg = delay_tg.replace(" ", "")
    delay_tg = delay_tg.replace("\n", "")
    delay_tg = float(delay_tg) #On converti delay_tg en integer
    trigger_key = key_tg  #On met la variable trigger_key = key_tg pour que la touche soit celle de la config

    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    while True:
        if not keyboard.is_pressed(trigger_key):
            time.sleep(0.1)

        if not GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive":
            continue

        if keyboard.is_pressed(trigger_key):
            player = pm.read_int(client + dwLocalPlayer)
            entity_id = pm.read_int(player + m_iCrosshairId)
            entity = pm.read_int(client + dwEntityList + (entity_id - 1) * 0x10)

            entity_team = pm.read_int(entity + m_iTeamNum)
            player_team = pm.read_int(player + m_iTeamNum)

            if entity_id > 0 and entity_id <= 64 and player_team != entity_team:
                time.sleep(delay_tg)
                pm.write_int(client + dwForceAttack, 6)

            time.sleep(0.006)


if __name__ == '__main__':
    main()