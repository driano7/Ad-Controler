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
URL=input('Enter the URL of the page to analyze: \n')
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
idiomas=['en','es','fr','pt','it']
idioma=''
bandera=0
f = open ('HTML/Prueba.html','r')
mensaje = f.read()
mensaje1=mensaje.split('"')
Numero_fotos=[]
Numero_fotos=buscarFicheros('pruebasSelenium/')

for j in range(len(Numero_fotos)-1):

    if 'lang=' in mensaje1[j]:
        if mensaje1[j+1] in idiomas:
            idioma=idiomas.index(mensaje1[j+1])

            print(' ---------------------------------------------------')
            print("          The language detected was: " + str(idiomas[idioma]))
            print(' ---------------------------------------------------')

            for i in range(len(mensaje1)):
                directorio='pruebasSelenium/'
                archivo='num'+str(i+1)+'.png'
                test=directorio+archivo
                ArchivoTXT=open('Salida'+'.txt','w')
                img=cv2.imread(r''+test)
                cad=pytesseract.image_to_string(img)
                ArchivoTXT.write(cad)
                lista=[]
                lista=pytesseract.image_to_string(img).split()

                Words = pd.read_csv('TablasCSV/'+str(idiomas[idioma])+'/Palabras_Clave.csv')
                Brands = pd.read_csv('TablasCSV/'+str(idiomas[idioma])+'/Brands.csv')
                Produc = pd.read_csv('TablasCSV/'+str(idiomas[idioma])+'/Produc.csv')

                palabras = Words['Palabra']
                plural = Words ['Plural']
                acento = Words ['Acento']
                #caracter = Words ['Caracter']
                #clave = Produc ['CLAVE']
                tipo = Produc ['Tipo']
                concepto = Produc ['Concepto']

                producto = Brands['Producto']
                submarca = Brands ['Submarca']
                marca = Brands ['Marca']
                abreviatura = Brands['Abreviatura']

                print(' ---------------------------------------------------')
                print('|                      Image '+str(i+1)+'                     |')
                print(' ---------------------------------------------------')
                #print(pytesseract.image_to_string(img))
                #print("Con respecto a la validación es lo siguiente: \n")

                if (lista !=[]):
               
                    interPalabras = set (palabras).intersection(lista)
                    interPlural = set(plural).intersection(lista)
                    interAcento = set(acento).intersection (lista)
                    #interCaracter = set(caracter).intersection(lista)

                    interProducto = set (producto).intersection(lista)
                    interSubmarca = set(submarca).intersection(lista)
                    interMarca = set(marca).intersection (lista)
                    interAbreviatura = set(abreviatura).intersection (lista)

                    #interClave = set (clave).intersection(lista)
                    interTipo = set(tipo).intersection(lista)
                    interConcepto = set(concepto).intersection (lista)
            
                    if (len(interPalabras)!=0) or (len(interPlural)!=0) or (len(interAcento)!=0) :

                        print("The repeated words in the Words table are:")
                        print ("1) -->"+ str(interPalabras))
                        print ("2) -->"+ str(interPlural))
                        print ("3) -->"+ str(interAcento))
                        #print ("4) -->"+ str(interCaracter))

                    if (len(interProducto)!=0) or (len(interSubmarca)!=0) or (len(interMarca)!=0) or (len(interAbreviatura)!=0):

                        print("The repeated words in the Brands table are:")
                        print ("1) -->"+ str(interProducto))
                        print ("2) -->"+ str(interSubmarca))
                        print ("3) -->"+ str(interMarca))
                        print ("4) -->"+ str(interAbreviatura))

                    if (len(interTipo)!=0) or (len(interConcepto)!=0):

                        print("The repeated words in the Products table are:")
                        #print ("1) -->"+ str(interClave))
                        print ("2) -->"+ str(interTipo))
                        print ("3) -->"+ str(interConcepto))

Final=time.process_time() - Inicio
print("Algorithm Employee time was: " + str(Final) + " Seconds")
print('Finish the analysis')
