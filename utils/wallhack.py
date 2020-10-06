import pymem
import pymem.process
import time
import ctypes
import warnings
warnings.simplefilter("ignore")
from Offsets import *

def main():
    try :
        pm = pymem.Pymem("csgo.exe")
    except :
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
        return

    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        glow_manager = pm.read_int(client + dwGlowObjectManager)

        for i in range(1, 32):  # Entities 1-32 are reserved for players.
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                player = pm.read_int(client + dwLocalPlayer)
                player_team = pm.read_int(player + m_iTeamNum)
                entity_hp = pm.read_int(entity + m_iHealth)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if entity_hp == 100 :
                    r = 0
                    g = 1
                    b = 0
                if entity_hp < 100 :
                    if entity_hp > 75:
                        r = 0.30
                        g = 1
                        b = 0
                    if entity_hp < 75:
                        r = 0.70
                        g = 0.30
                        b = 0
                    if entity_hp < 50 :
                        r = 1
                        g = 0.1
                        b = 0
                    if entity_hp < 25 :
                        r = 1
                        g = 0
                        b = 0
                    if entity_hp == 1 :
                        r = 1
                        g = 1
                        b = 1

                if entity_team_id != player_team:  # Terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(r))   # R 
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(g))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(b))   # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

                elif entity_team_id != player_team:  # Counter-terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(r))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(g))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(b))   # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

if __name__ == '__main__':
    main()