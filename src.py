import numpy as np
import cv2
from PIL import Image
import math

# pix = im.load()
# pix[x,y] = value
# print(pix[x,y])

im_gray = cv2.imread('testimg.png', 0)
width = int(im_gray[0].size)
height = int(im_gray.size/width)

(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 127
im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

thickness = 0
x = int(width/2)
y = 0
trab = 0

def startPoint():
    global thickness, x, y
    _ = 0
    quit = False
    aux = 0
    x = int(width/2)
    while _ < height:
        while im_bw[_][x] == 0:
            thickness = thickness + 1
            aux = aux + _
            _ = _ + 1
            if im_bw[_][x] == 255:
                quit = True
                break
        if quit:
            y = int(math.ceil(aux/thickness))
            return x
            break
        _ = _ + 1

def nextPoint(x, y, prev_x, prev_y):
    global thickness, trab
    aux_x = 0
    aux_y = 0
    pix = 0
    distance = int(thickness*2)
    matbuff_x = []
    matbuff_y = []
    matbuff_x.append(0)
    matbuff_y.append(0)
    line = 0
    stopper = True
    for _ in range(360):
        aux_x = int(math.ceil(math.sin(_/56)*distance+x))
        aux_y = int(math.ceil(math.cos(_/56)*distance+y))
        print(aux_x, aux_y)
        # im_bw[aux_y][aux_x] = 255
        if im_bw[aux_y][aux_x] == 255:
            print("white")
            if stopper:
                if pix != 0:
                    matbuff_x[line] = matbuff_x[line]/pix
                    matbuff_y[line] = matbuff_y[line]/pix
                stopper = False
                matbuff_x.append(0)
                matbuff_y.append(0)
                line = line + 1
                pix = 0
        else:
            print("black")
            stopper = True
            matbuff_x[line] = aux_x+matbuff_x[line]
            matbuff_y[line] = aux_y+matbuff_y[line]
            pix = pix + 1

    if pix != 0:
        matbuff_x[line] = matbuff_x[line]/pix
        print(matbuff_x[line])
        matbuff_y[line] = matbuff_y[line]/pix

    if matbuff_y[0] != 0 and matbuff_x[0] != 0:
        matbuff_y[0] = (matbuff_y[0]+matbuff_y[len(matbuff_y)-1])/2
        matbuff_x[0] = (matbuff_x[0]+matbuff_x[len(matbuff_x)-1])/2
    else:
        matbuff_x[0] = matbuff_x[len(matbuff_x)-2]
        matbuff_y[0] = matbuff_y[len(matbuff_y)-2]

    print(line)
    for _ in range(line-2):
        aux_x = int(matbuff_x[_])
        aux_y = int(matbuff_y[_])
        im_bw[aux_y][int(aux_x)] = 150
        if not (aux_x in range(prev_x-2, prev_x+2) and aux_y != range(prev_y-2, prev_y+2)) and line>2:
            nextPoint(aux_x, aux_y, x, y)
            trab = trab + 1
        print(matbuff_y[_], matbuff_x[_])


startPoint()
nextPoint(x, y, 0, 0)
cv2.imshow('bw_image.png', im_bw)
cv2.waitKey(0)
cv2.destroyAllWindows()
