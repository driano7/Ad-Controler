import pandas as pd 
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests
import time
import os
import sys
import cv2
import re
from PIL import Image
import pytesseract 
from os import remove


def buscarFicheros(directorio):
    ficheros=[]
    for base,dirs,files in os.walk(directorio):
        ficheros.append(files)
    return files


# Obtención código fuente html 
URL=input('Ingresa la dirección URL del sitio a analizar: \n')
Inicio=time.process_time()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
req = requests.get(URL,headers=headers)
bs = BeautifulSoup(req.content,features='lxml')
Archivo1=open('HTML/Prueba'+'.html','w')
Archivo1.write(str(bs))
Archivo1.close()

#'geckoFirefox/'
driver = webdriver.Firefox()
driver.get(URL)
driver.maximize_window()
time.sleep(0.5)
iter=1
while True:
        scrollHeight = driver.execute_script("return document.documentElement.scrollHeight")
        Height=600*iter
        time.sleep(0.5)
        driver.save_screenshot("pruebasSelenium/num"+str(iter)+".png")
        driver.execute_script("window.scrollTo(0, " + str(Height) + ");")

        if Height > scrollHeight:
            break
        
        iter+=1

driver.close()


#Parseo del código para obtener las imágenes
bandera=0
Numero_fotos=[]
Numero_fotos=buscarFicheros('pruebasSelenium/')

for j in range(len(Numero_fotos)-1):

    directorio='pruebasSelenium/'
    archivo='num'+str(j+1)+'.png'
    test=directorio+archivo
    ArchivoTXT=open('Salida'+'.txt','w')
    img=cv2.imread(r''+test)
    cad=pytesseract.image_to_string(img)
    ArchivoTXT.write(cad)
    lista=[]
    lista=pytesseract.image_to_string(img).split()

    Words = pd.read_csv('Trending.csv')
    virus = Words['COVID']
    sociales = Words ['Movimientos']

    print(' ---------------------------------------------------')
    print('|                     Imagen '+str(j+1)+'                     |')
    print(' ---------------------------------------------------')

    if (lista !=[]):

        interVirus = set (virus).intersection(lista)
        interSociales = set(sociales).intersection(lista)
            
        if (len(interVirus)!=0) or (len(interSociales)!=0) :

            print("Las repeticiones del algoritmo son:")
            print ("1)COVID -->"+ str(interVirus))
            print ("2)SOCIAL -->"+ str(interSociales))

            k=lista.index(str(interVirus)[2:len(str(interVirus))-2])

            print("\n\nExpresiones del tema: ")

            if(k>0):
                antes=[]
                times=0
                while(k-times>=0 and times<5):
                    antes.append(lista[k-times])
                    times+=1

                antes.reverse()
                despues=[]
                times=0
                while(times<5 and (k+times)<=(len(lista)-1)):
                    despues.append(lista[k+times])
                    times+=1

            print("\n\nANTES palabra clave: ")

            for i in range(len(antes)):
                print(antes[i])

            print("\n\nDESPUES palabra clave:")

            for i in range(len(despues)):
                print(despues[i])

Final=time.process_time() - Inicio
print("Algorithm Employee time was: " + str(Final) + " Seconds")
print('Finish the analysis')
