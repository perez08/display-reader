#!/usr/bin/python3.5

from PIL import Image
import pytesseract
import argparse
import numpy as np
import cv2
import os

def ver(imgA):
    cv2.imshow("Imagen", imgA)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def recortar(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
    ver(gray)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(blur,50, 150)
    ver(edges)
    img, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Para determinar el contorno de la pantalla, se escoge el area mas grande y se recorta la imagen con respecto a esos
    # puntos

    xmin = 255
    xmax = 0
    ymin = 255
    ymax = 0

    for element in contours:
        for c in element:
            if c[0][0] < xmin:
                xmin = c[0][0]
            if c[0][0] > xmax:
                xmax = c[0][0]
            if c[0][1] < ymin:
                ymin = c[0][1]
            if c[0][1] > ymax:
                ymax = c[0][1]

    xmin += 50
    xmax -= 20
    ymin += 5
    ymax -= 55

    display = blur[ymin:ymax, xmin:xmax]
    return display

def procesar(img):
    
    thres = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 5))
    thres = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 13))
    thres = cv2.morphologyEx(thres, cv2.MORPH_OPEN, kernel)
    ver(thres)
    img, cnts, hierarchy = cv2.findContours(thres,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    img = cv2.drawContours(thres, cnts, -1, (255,0,0), 3)
    img, cnts, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    tam = thres.shape
    digits = []

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if h < tam[0]-1:
            digits.append(c)

    final = cv2.drawContours(img, digits, -1, (0,255,0), 19)
    ver(final)
    return final

def splitNum(img):
    
    img, cnts, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    digits = []
    tam = img.shape

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        
        if (h < tam[0]-1) and h > 120:
            digits.append((x, c))

    # Ordenar los digitos segun su coordenada x de izquierda a derecha
    digits = sorted(digits, key=lambda x: int(x[0]))

    return digits

def getNum(final, digits):
    
    i = 1
    lectura = ""

    for element in digits:
        (x, y, w, h) = cv2.boundingRect(element[1])
        digit = final[y:y+h, x:x+w]
        name = "temp/" + str(i) + ".png"
        i += 1

        tam = digit.shape
        newTam = (tam[0]+10, tam[1]+10)
        img1 = np.ones(newTam)
        img1 = 255*img1
        j = 4
        k = 4

        for j in range(0, tam[0]):
            for k in range(0, tam[1]):
                img1[j+5][k+5] = digit[j][k]

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        digit = cv2.morphologyEx(img1, cv2.MORPH_CLOSE, kernel)

        cv2.imwrite(name, digit)
        num = pytesseract.image_to_string(Image.open(name), lang='letsgodigital', config='-psm 10 -c tessedit_char_whitelist=0123456789')

        if num == "8" or num=="":
            num1 = pytesseract.image_to_string(Image.open(name), lang='eng', config='-psm 10 -c tessedit_char_whitelist=0123456789')
            if num1 == "0":
                num = num1

        os.remove(name)

        lectura += num

    return lectura

def obtenerDato(path):

    img = cv2.imread(path)

    display = recortar(img)

    final = procesar(display)

    digits = splitNum(final)
   
    lectura = getNum(final, digits)

    print(lectura)
    return(lectura)

def main():

    datos = []

    lectura = obtenerDato("Lecturas/Lectura1.jpeg")
    datos.append(int(lectura))

    lectura = obtenerDato("Lecturas/Lectura2.jpg")
    datos.append(int(lectura))

if __name__ == '__main__':
    main()