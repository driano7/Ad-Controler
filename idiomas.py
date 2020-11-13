import pandas as pd 
import numpy as np
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
URL=input('Ingrese el URL de la pagina a analizar: \n')
Inicio=time.process_time()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
req = requests.get(URL,headers=headers)
# Comprobamos que la petición nos devuelve un Status Code = 200
status_code = req.status_code
if status_code == 200:
    bs = BeautifulSoup(req.content,features='lxml')
Archivo1=open('HTML/Prueba'+'.html','w')
Archivo2=open('HTML/Prueba'+'.html','w')
Archivo1.write(str(bs))
Archivo1.close()



#Parseo del código para obtener las imágenes
lista_url=[]
idiomas=['en','es','fr','pt','it']
idioma=''
bandera=0
f = open ('HTML/Prueba.html','r')
mensaje = f.read()
mensaje1=mensaje.split('"')
dir_downloads = 'pruebasBS4/'
k=0
Match=0

if '<amp-ad' in mensaje:
    mensaje2=mensaje.split('<amp-ad')
    for i in range(len(mensaje2)):
        if '</amp-ad>' in mensaje2[i]:
            cierre=mensaje2[i].split('</amp-ad>')
            Archivo2.write(str(cierre[len(cierre)-1]))
        else:
            Archivo2.write(str(mensaje2[i]))

Archivo2.close()


for i in range(len(mensaje1)):
    if 'google' in mensaje1[i]:
        Match=1
    if 'lang=' in mensaje1[i]:
        if mensaje1[i+1] in idiomas:
            idioma=idiomas.index(mensaje1[i+1])

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

            #print(palabras)

            print(' ---------------------------------------------------')
            print("El idioma detectado fue: " + str(idiomas[idioma]))
            print(' ---------------------------------------------------')

    if ('jpg' or 'png' or 'jpeg') in mensaje1[i].split('.'):
        if ('https') not in mensaje1[i].split(':'):
            print (mensaje1[i])

    if ('https' or 'http') in mensaje1[i].split(':'):
        bandera=0
        if 'meta' in mensaje1[i-1]:
            bandera=1
        if (bandera==0) and ('jpg' or 'png' or 'jpeg' or 'svg') in mensaje1[i].split('.'):

            Match=0;
            k=k+1
            receive = requests.get(mensaje1[i])
            lista_url.append(mensaje1[i])
            with open(r''+str(dir_downloads+'num'+str(k)+'.png'),'wb') as f:
                f.write(receive.content)

            print(' ---------------------------------------------------')
            print('|                 Imagen '+str(k)+'                     |')
            print(' ---------------------------------------------------')

            if Match == 0:

                archivo='num'+str(k)+'.png'
                test=dir_downloads+archivo
                img=cv2.imread(r''+test)
                cad=pytesseract.image_to_string(img)

                lista=[]
                lista=pytesseract.image_to_string(img).split()

                if (lista !=[]):
           
                    #interPalabras = set (palabras).intersection(lista)
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

                        print("Las palabras repetidas de la tabla de Palabras son:")
                        print ("1) -->"+ str(interPalabras))
                        print ("2) -->"+ str(interPlural))
                        print ("3) -->"+ str(interAcento))
                        #print ("4) -->"+ str(interCaracter))

                    if (len(interProducto)!=0) or (len(interSubmarca)!=0) or (len(interMarca)!=0) or (len(interAbreviatura)!=0):

                        print("Las palabras repetidas de la tabla de Marcas son:")
                        print ("1) -->"+ str(interProducto))
                        print ("2) -->"+ str(interSubmarca))
                        print ("3) -->"+ str(interMarca))
                        print ("4) -->"+ str(interAbreviatura))

                    if (len(interTipo)!=0) or (len(interConcepto)!=0):

                        print("Las palabras repetidas de la tabla de Productos son:")
                        print ("1) -->"+ str(interClave))
                        print ("2) -->"+ str(interTipo))
                        print ("3) -->"+ str(interConcepto))

Final=time.process_time() - Inicio
print("El tiempo Empleado del algoritmo fue: " + str(Final) + " Segundos")
print('Termino el analisis')
