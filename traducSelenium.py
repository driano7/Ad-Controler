from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import sys
import cv2
import re
from PIL import Image
import pytesseract 
from os import remove
from langdetect import detect
from scipy import stats

"""
driver = webdriver.Firefox('geckoFirefox/')
#driver.get('https://www5.usp.br/')   #-->Página en Portugues 
driver.get('https://careers.twitter.com/en/university.html')     #--> Página en Ingles
driver.maximize_window()
time.sleep(0.5)
iter=1
while True:
        scrollHeight = driver.execute_script("return document.documentElement.scrollHeight")
        Height=600*iter
        time.sleep(0.5)
        driver.save_screenshot("pruebas/num"+str(iter)+".png")
        driver.execute_script("window.scrollTo(0, " + str(Height) + ");")

        if Height > scrollHeight:
            break
        
        iter+=1

driver.close()
"""

def buscarFicheros(directorio):
    ficheros=[]
    for base,dirs,files in os.walk(directorio):
        ficheros.append(files)
    return files


Numero_fotos=[]
Numero_fotos=buscarFicheros('pruebas/')


for i in range(len(Numero_fotos)-1):
    directorio='pruebas/'
    archivo='num'+str(i+1)+'.png'
    test=directorio+archivo
    Archivo1=open('Salida'+'.txt','w')
    img=cv2.imread(r''+test)
    cad=pytesseract.image_to_string(img)
    Archivo1.write(cad)

    print(pytesseract.image_to_string(img))

    print(' ---------------------------------------------------')
    print('|                 Screenshot '+str(i)+'                     |')
    print(' ---------------------------------------------------')

    lista=[]
    lista=pytesseract.image_to_string(img).split()
    print(lista)
    if (lista !=[]):
        try:
            idiomas = []
            leng = ""
            leng += detect(lista[i])
            print("El idioma detectado fue: " + leng)
            idiomas.append([leng])

            for k in range(len(idiomas)):
                idiomas[k].append([leng])   

                for j in range(len(idiomas)):
                    print("Los idiomas que estan en el arreglo son: ")
                    print(idiomas[j])
        except:
            language = "error"
            print("\n Ya no hay que imprimir en los lenguajes ")
    else:
        print("La lista de Pytesseract esta vacía")
    
        """print("Veces que se Encontro el Idioma Inglés: "+ str(idiomas.count(en)))
        print("Veces que se Encontro el Idioma Portugués: "+ str(idiomas.count(pt)))
        print("Veces que se Encontro el Idioma Italiano: "+ str(idiomas.count(it)))
        print("Veces que se Encontro el Idioma Francés: "+ str(idiomas.count(fr)))
        print("Veces que se Encontro el Idioma Español: "+ str(idiomas.count(es)))"""
        #print(stats.mode(idiomas))
            
