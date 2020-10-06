import pymem
import time
import keyboard
import ctypes
from math import *
from Offsets import *

baim = False

def main():

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On ouvre la config et on en tire la variable abkey
    with open("configs/"+path) as config_file :
        line_nmb = 0
        for line in config_file :
            line_nmb = line_nmb + 1
            if line_nmb == 17 :
                abkey = line
                abkey = abkey.replace(" ", "")
                abkey = abkey.replace("\n", "")
            if line_nmb >= 18 :
                config_file.close()
                break

    aimfov = 15
    oldpunchx = 0.0
    oldpunchy = 0.0

    try :
        pm = pymem.Pymem("csgo.exe")
    except :
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
        return

    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
   
    while True:
                        
        target = None
        olddistx = 111111111111
        olddisty = 111111111111
        #MANAGER
        if client and engine and pm:
            try:
                player = pm.read_int(client + dwLocalPlayer)
                engine_pointer = pm.read_int(engine + dwClientState)
                glow_manager = pm.read_int(client + dwGlowObjectManager) 
                crosshairID = pm.read_int(player + m_iCrosshairId) 
                getcrosshairTarget = pm.read_int(client + dwEntityList + (crosshairID - 1) * 0x10)
                immunitygunganme = pm.read_int(getcrosshairTarget + m_bGunGameImmunity)
                localTeam = pm.read_int(player + m_iTeamNum)
                crosshairTeam = pm.read_int(getcrosshairTarget + m_iTeamNum)
            except:
                continue

        #GlowESP
        for i in range(1,32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                try:
                    entity_glow = pm.read_int(entity + m_iGlowIndex)
                    entity_team_id = pm.read_int(entity + m_iTeamNum)
                    entity_isdefusing = pm.read_int(entity + m_bIsDefusing)
                    entity_hp = pm.read_int(entity + m_iHealth)
                    entity_dormant = pm.read_int(entity + m_bDormant)
                except:
                    continue

                if localTeam != entity_team_id and entity_hp > 0:
                    entity_bones = pm.read_int(entity + m_dwBoneMatrix)
                    localpos_x_angles = pm.read_float(engine_pointer + dwClientState_ViewAngles)
                    localpos_y_angles = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                    localpos1 = pm.read_float(player + m_vecOrigin)
                    localpos2 = pm.read_float(player + m_vecOrigin + 4)
                    localpos_z_angles = pm.read_float(player + m_vecViewOffset + 0x8)
                    localpos3 = pm.read_float(player + m_vecOrigin + 8) + localpos_z_angles
                    if baim:
                        try:
                            entitypos_x = pm.read_float(entity_bones + 0x30 * 5 + 0xC)
                            entitypos_y = pm.read_float(entity_bones + 0x30 * 5 + 0x1C)
                            entitypos_z = pm.read_float(entity_bones + 0x30 * 5 + 0x2C)
                        except:
                            continue
                    else:
                        try:
                            entitypos_x = pm.read_float(entity_bones + 0x30 * 8 + 0xC)
                            entitypos_y = pm.read_float(entity_bones + 0x30 * 8 + 0x1C)
                            entitypos_z = pm.read_float(entity_bones + 0x30 * 8 + 0x2C)
                        except:
                            continue
                    try :
                        X, Y = calcangle(localpos1, localpos2, localpos3, entitypos_x, entitypos_y, entitypos_z)
                    except :
                        pass
                    newdist_x, newdist_y = calc_distance(localpos_x_angles, localpos_y_angles, X, Y)
                    if newdist_x < olddistx and newdist_y < olddisty and newdist_x <= aimfov and newdist_y <= aimfov:
                        olddistx, olddisty = newdist_x, newdist_y
                        target, target_hp, target_dormant = entity, entity_hp, entity_dormant
                        target_x, target_y, target_z = entitypos_x, entitypos_y, entitypos_z
                if keyboard.is_pressed(abkey) and player:
                    if target and target_hp > 0 and not target_dormant:
                        x, y = calcangle(localpos1, localpos2, localpos3, target_x, target_y, target_z)
                        normalize_x, normalize_y = normalizeAngles(x, y)
                        
                        if True :
                            pm.write_uchar(engine + dwbSendPackets, 0)
                            Commands = pm.read_int(client + dwInput + 0xF4)
                            VerifedCommands = pm.read_int(client + dwInput + 0xF8)
                            Desired = pm.read_int(engine_pointer + clientstate_last_outgoing_command) + 2
                            OldUser = Commands + ((Desired - 1) % 150) * 100
                            VerifedOldUser = VerifedCommands + ((Desired - 1) % 150) * 0x68
                            m_buttons = pm.read_int(OldUser + 0x30)
                            Net_Channel = pm.read_uint(engine_pointer + clientstate_net_channel)
                            if pm.read_int(Net_Channel + 0x18) >= Desired:
                                pm.write_float(OldUser + 0x0C, normalize_x)
                                pm.write_float(OldUser + 0x10, normalize_y)
                                pm.write_int(OldUser + 0x30, m_buttons | (1 << 0))
                                pm.write_float(VerifedOldUser + 0x0C, normalize_x)
                                pm.write_float(VerifedOldUser + 0x10, normalize_y)
                                pm.write_int(VerifedOldUser + 0x30, m_buttons | (1 << 0))
                                pm.write_uchar(engine + dwbSendPackets, 1)
                            else :
                                pm.write_uchar(engine + dwbSendPackets, 1)
                        else:
                            pm.write_float(engine_pointer + dwClientState_ViewAngles, normalize_x)
                            pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, normalize_y)
                        
                            time.sleep(0.2)

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

def calc_distance(current_x, current_y, new_x, new_y):
    distancex = new_x - current_x
    if distancex < -89:
        distancex += 360
    elif distancex > 89:
        distancex -= 360
    if distancex < 0.0:
        distancex = -distancex
 
    distancey = new_y - current_y
    if distancey < -180:
        distancey += 360
    elif distancey > 180:
        distancey -= 360
    if distancey < 0.0:
        distancey = -distancey
    return distancex, distancey

def calcangle(localpos1, localpos2, localpos3, enemypos1, enemypos2, enemypos3):
    try:
        delta_x = localpos1 - enemypos1
        delta_y = localpos2 - enemypos2
        delta_z = localpos3 - enemypos3
        hyp = sqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z)
        x = atan(delta_z / hyp) * 180 / pi
        y = atan(delta_y / delta_x) * 180 / pi
        if delta_x >= 0.0:
            y += 180.0
        return x, y
    except Exception as e:
        print(e)
        pass
    
if __name__ == "__main__":
    main()
