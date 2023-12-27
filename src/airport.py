import numpy as np
import math

Airport_list = [{'name' : 'RJTT', 'position' : [35.553333, 139.781111]},
                {'name' : 'RJAA', 'position' : [35.763889, 140.391667]},
                {'name' : 'RJFF', 'position' : [33.584444, 130.451667]},
                {'name' : 'RJCC', 'position' : [42.775, 141.692222]},
                {'name' : 'ROAH', 'position' : [26.195833, 127.645833]},
                {'name' : 'RJOO', 'position' : [34.785278, 135.438056]},
                {'name' : 'RJBB', 'position' : [34.427222, 135.243889]},
                {'name' : 'RJNN', 'position' : [34.858333, 136.805278]},
                {'name' : 'RJFK', 'position' : [31.8, 130.721667]},
                {'name' : 'RJBE', 'position' : [34.633333, 135.226389]},
                {'name' : 'RJFT', 'position' : [32.837222, 130.855]},
                {'name' : 'RJSS', 'position' : [38.136944, 140.9225]},
                {'name' : 'RJFM', 'position' : [31.877222, 131.448611]},
                {'name' : 'RJFU', 'position' : [32.916944, 129.913611]},
                {'name' : 'ISG', 'position' : [24.344722, 124.186944]},
                {'name' : 'RJOM', 'position' : [33.827222, 132.699722]},
                {'name' : 'RJOA', 'position' : [34.436111, 132.919444]},
                {'name' : 'ROMY', 'position' : [24.782778, 125.295]},
                {'name' : 'RJFO', 'position' : [33.476111, 131.739722]},
                {'name' : 'RJCH', 'position' : [41.77, 140.821944]},
                {'name' : 'RJOT', 'position' : [34.214167, 134.015556]},
                {'name' : 'RKSS', 'position' : [37.565792, 126.800743]},
                {'name' : 'RJSI', 'position' : [37.467151, 126.433356]},
                {'name' : 'RCTP', 'position' : [25.077017, 121.233515]},
                {'name' : 'RJSA', 'position' : [40.735394, 140.689597]},
                {'name' : 'RJFR', 'position' : [33.842907, 131.035532]},
                {'name' : 'EDDF', 'position' : [50.037812, 8.562920]}]

#-------------------------距離を返す関数----------------------------------


def Qtedist( lata, lona, latb, lonb):
# Output distance (NM) between input lat lon data

    lata = lata/180*np.pi
    lona = lona/180*np.pi
    latb = latb/180*np.pi
    lonb = lonb/180*np.pi

    TWOPI = math.pi * 2
    ELLIPS = 4.4814724e-5
    REQTOR = 3443.9184665

    londif = lonb-lona

    # unit vectors beacon a and b
    #----------------------------
    xa = math.cos(lata)
    za = math.sin(lata)
    xb = math.cos(latb)*math.cos(londif)
    yb = math.cos(latb)*math.sin(londif)
    zb = math.sin(latb)
    zave = 0.5*(za + zb)
    rprime = REQTOR / math.sqrt(1.0 - ELLIPS * zave * zave)

    # distance over earth
    #---------------------
    sangl2= math.sqrt((xb - xa)*(xb - xa)+yb * yb+(zb - za)*(zb - za))*0.5
    angle = 2.0 * math.asin(min(1.0, max(-1.0, sangl2)))
    dist = angle * rprime

    # true bearing from a to b
    #--------------------------
    cosqte = (xa * zb - xb * za)
    sinqte = yb

    if (sinqte*sinqte + cosqte*cosqte) > 0:
        qte = math.atan2(sinqte, cosqte)
    else:
        qte = 0.0

    if qte < 0:
        qte = qte + TWOPI

    return dist