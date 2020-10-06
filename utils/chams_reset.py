import pymem
import pymem.process
import keyboard
import time
import re
from Offsets import *

def main():
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll

    rgba = [0, 255, 0]
    while True:

        try:
            time.sleep(0.001)
            for i in range(32):
                entity = pm.read_int(client + dwEntityList + i * 0x10)
                if entity:
                    entity_team_id = pm.read_int(entity + m_iTeamNum)
                    player = pm.read_int(client + dwLocalPlayer)
                    player_team = pm.read_int(player + m_iTeamNum)
                    if entity_team_id != player_team :
                        pm.write_int(entity + m_clrRender, (rgba[1]))
                        pm.write_int(entity + m_clrRender + 0x1, (rgba[1]))
                        pm.write_int(entity + m_clrRender + 0x2, (rgba[1]))

                else:
                	pass

        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()