from threading import Thread
from Offsets import *
import win32api
import pymem
import keyboard
import ctypes
from math import atan2, sqrt, pi, asin, isnan
import time
 
Aim = False
aimbone = 8
bone = 8
 
 
def checkindex():
    localplayer = pm.read_int(client + dwLocalPlayer)
    for y in range(64):
        if pm.read_int(client + dwEntityList + y * 0x10):
            entity = pm.read_int(client + dwEntityList + y * 0x10)
            if localplayer == entity and y:
                return y
 
def nanchecker(first, second):
    if isnan(first) or isnan(second):
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
 
 
def Magnitude(vec_x, vec_y, vec_z):
    return sqrt(vec_x * vec_x + vec_y * vec_y + vec_z * vec_z)
 
 
def Subtract(src_x, src_y, src_z, dst_x, dst_y, dst_z):
    diff_x = src_x - dst_x
    diff_y = src_y - dst_y
    diff_z = src_z - dst_z
    return (diff_x, diff_y, diff_z)
 
 
def Distance(src_x, src_y, src_z, dst_x, dst_y, dst_z):
    diff_x, diff_y, diff_z = Subtract(src_x, src_y, src_z, dst_x, dst_y, dst_z)
    src_x += diff_x / smooth
    src_y += diff_y / smooth
    return Magnitude(diff_x, diff_y, diff_z)
 
 
def calcangle(src_x, src_y, src_z, dst_x, dst_y, dst_z):
    x = -atan2(dst_x - src_x, dst_y - src_y) / pi * 180.0 + 180.0
    y = asin((dst_z - src_z) / Distance(src_x, src_y, src_z, dst_x, dst_y, dst_z)) * 180.0 / pi
    return x, y
 
 
def GetBestTarget(local):
    while True:
        olddist = 1.7976931348623157e+308
        newdist = None
        target = None
        if local :
            localplayer_team = pm.read_int(local + m_iTeamNum)
            for x in range(1):
                entity_id = pm.read_int(local + m_iCrosshairId)
                entity = pm.read_int(client + dwEntityList + (entity_id - 1) * 0x10)
                if pm.read_int(client + dwEntityList + x * 0x10):
                    spotted = pm.read_int(entity + m_bSpottedByMask)
                    index = checkindex()
                    entity_health = pm.read_int(entity + m_iHealth)
                    entity_team = pm.read_int(entity + m_iTeamNum)
                    if localplayer_team != entity_team and entity_health > 0 :# and spotted == 1 << index:
                        entity_bones = pm.read_int(entity + m_dwBoneMatrix)
                        localpos_x = pm.read_float(local + m_vecOrigin)
                        localpos_y = pm.read_float(local + m_vecOrigin + 4)
                        localpos_z = pm.read_float(local + m_vecOrigin + 8)
 
                        localpos_x_angles = pm.read_float(enginepointer + dwClientState_ViewAngles)
                        localpos_y_angles = pm.read_float(enginepointer + dwClientState_ViewAngles + 0x4)
                        localpos_z_angles = pm.read_float(enginepointer + dwClientState_ViewAngles + 0x8)
 
                        entitypos_x = pm.read_float(entity_bones + 0x30 * bone + 0xC)
                        entitypos_y = pm.read_float(entity_bones + 0x30 * bone + 0x1C)
                        entitypos_z = pm.read_float(entity_bones + 0x30 * bone + 0x2C) + 64
 
                        X, Y = calcangle(entitypos_x, entitypos_y, entitypos_z, localpos_x, localpos_y, localpos_z)
                        newdist = Distance(localpos_x_angles, localpos_y_angles, localpos_z_angles, entitypos_x,
                                           entitypos_y, entitypos_z)
                        olddist = newdist
                        target = entity
            if target:
                return target
 
def main():
    try :
        pm = pymem.Pymem("csgo.exe")
        global pm
    except :
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Could not find the csgo.exe process !', 'Error', 16)
        return
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
    enginepointer = pm.read_int(engine + dwClientState)
    key_ai = " "
    smooth_ai = 0
    fov_ai = " "
    global client
    global engine
    global enginepointer

    #On cherche le nom de la config actuelle
    with open("configs/path.txt") as path_txt :
        path = path_txt.readline()
        path_txt.close()

    #On ouvre la config et on en tire les variables smooth, fov et key_a
    with open("configs/"+path) as config_file :
        line_nmb = 1
        for line in config_file :
            if line_nmb == 5 :
                key_ai = line
            if line_nmb == 6 :
                smooth_ai = line
            if line_nmb == 7 :
                fov_ai = line
            if line_nmb >= 8 :
                config_file.close()
                break
            line_nmb = line_nmb + 1

    key_ai = key_ai[0:-1] #On sort le retour à la ligne après le nom de la touche
    key_ai = key_ai.replace(" ", "")  #On sort les espaces
    trigger_key = key_ai
    smooth_ai = float(smooth_ai) #On converti smooth_ai en integer
    smooth = smooth_ai
    fov_ai = fov_ai[0:-1] #On sort le retour à la ligne après le nom de la touche
    fov_ai = float(fov_ai) #On converti fov_ai en integer
    aimfov = fov_ai
    global aimfov
    global smooth
    global trigger_key
    while True:
        if not keyboard.is_pressed(trigger_key):
            time.sleep(0.1)
            tours = 0
        while keyboard.is_pressed(trigger_key) :
            aimlocalplayer = pm.read_int(client + dwLocalPlayer)
            aimflag = pm.read_int(aimlocalplayer + m_fFlags)
            aimteam = pm.read_int(aimlocalplayer + m_iTeamNum)
            enginepointer = pm.read_int(engine + dwClientState)
 
            for y in range(1):
                if pm.read_int(client + dwEntityList + y * 0x10):
                    aimplayer = GetBestTarget(aimlocalplayer)
                    aimplayerbone = pm.read_int(aimplayer + m_dwBoneMatrix)
                    gungameimmunity = pm.read_int(aimplayer + m_bGunGameImmunity)
                    aimplayerteam = pm.read_int(aimplayer + m_iTeamNum)
                    aimplayerhealth = pm.read_int(aimplayer + m_iHealth)
                    if aimplayerteam != aimteam and aimplayerhealth > 0 and gungameimmunity != 1:
                        localpos1 = pm.read_float(aimlocalplayer + m_vecOrigin)
                        localpos2 = pm.read_float(aimlocalplayer + m_vecOrigin + 4)
                        if aimflag == 263:
                            localpos3 = pm.read_float(aimlocalplayer + m_vecOrigin + 8) + 45
                        elif aimflag == 257:
                            localpos3 = pm.read_float(aimlocalplayer + m_vecOrigin + 8) + 62
                        elif aimflag == 256:
                            localpos3 = pm.read_float(aimlocalplayer + m_vecOrigin + 8) + 64
                        enemypos1 = pm.read_float(aimplayerbone + 0x30 * bone + 0xC)
                        enemypos2 = pm.read_float(aimplayerbone + 0x30 * bone + 0x1C)
                        enemypos3 = pm.read_float(aimplayerbone + 0x30 * bone + 0x2C)
 
                        targetline1 = enemypos1 - localpos1
                        targetline2 = enemypos2 - localpos2
                        targetline3 = enemypos3 - localpos3
 
                        viewanglex = pm.read_float(enginepointer + dwClientState_ViewAngles)
                        viewangley = pm.read_float(enginepointer + dwClientState_ViewAngles + 0x4)
 
                        if targetline2 == 0 and targetline1 == 0:
                            yaw = 0
                            if targetline3 > 0:
                                pitch = 270
                            else:
                                pitch = 90
                        else:
                            yaw = (atan2(targetline2, targetline1) * 180 / pi)
                            if yaw < 0:
                                yaw += 360
                            hypo = sqrt(
                                (targetline1 * targetline1) + (targetline2 * targetline2) + (targetline3 * targetline3))
                            pitch = (atan2(-targetline3, hypo) * 180 / pi)
 
                            if pitch < 0:
                                pitch += 360
 
                        pitch, yaw = normalizeAngles(pitch, yaw)
                        if checkangles(pitch, yaw):
 
                            distance_x, distance_y = calc_distance(viewanglex, viewangley, pitch, yaw)
 
                            if distance_x < aimfov and distance_y < aimfov:
 
                                if nanchecker(pitch, yaw):
                                    if tours > 2 :
                                        time.sleep(0.2)
                                    if keyboard.is_pressed(trigger_key) :
                                        pm.write_float(enginepointer + dwClientState_ViewAngles, pitch)
                                        pm.write_float(enginepointer + dwClientState_ViewAngles + 0x4, yaw)
                                        tours = tours + 1

if __name__ == '__main__':
    main()
