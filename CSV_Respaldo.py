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

# Obtención código fuente html 
URL=input('Ingrese el URL de la pagina a analizar: \n')
Inicio=time.process_time()
request=requests.get(URL)
bs=BeautifulSoup(request.text,'lxml')
Archivo1=open('HTML/Prueba'+'.html','w')
Archivo2=open('HTML/Salida'+'.html','w')
Archivo1.write(str(bs))
Archivo1.close()


WordsSpanish = pd.read_csv("TablasCSV/Palabras_Clave_Es.csv")
Brands = pd.read_csv("TablasCSV/Brands.csv")
ProducSpanish = pd.read_csv("TablasCSV/Produc_Es.csv")

palabras = WordsSpanish['Palabra']
plural = WordsSpanish ['Plural']
acento = WordsSpanish ['Acento']
caracter = WordsSpanish ['Caracter']

clave = ProducSpanish['CLAVE']
tipo = ProducSpanish['Tipo']
concepto = ProducSpanish['Concepto']

producto = Brands['Producto']
submarca = Brands ['Submarca']
marca = Brands ['Marca']
abreviatura = Brands['Abreviatura']



numPalabras = palabras.iloc [0:len(palabras)-1]
numPlural = plural.iloc [0:len(plural)-1]
numAcento = acento.iloc [0:len(acento)-1]
numCaracteres = caracter.iloc [0:len(caracter)-1]

numClaves = clave.iloc [0:len(clave)-1]
numTipo = tipo.iloc [0:len(tipo)-1]
numConcepto = concepto.iloc [0:len(concepto)-1]

numProductos = producto.iloc [0:len(producto)-1]
numSubMarcas = submarca.iloc [0:len(submarca)-1]
numMarcas = marca.iloc [0:len(marca)-1]
numAbreviaturas = abreviatura.iloc [0:len(abreviatura)-1]

def buscarFicheros(directorio):
    ficheros=[]
    for base,dirs,files in os.walk(directorio):
        ficheros.append(files)
    return files


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

for i in range(len(mensaje1)):
    if 'lang=' in mensaje1[i]:
        if mensaje1[i+1] in idiomas:
            idioma=idiomas.index(mensaje1[i+1])
            print(idiomas[idioma])

    if ('https' or 'http') in mensaje1[i].split(':'):
        bandera=0
        if ('jpg' or 'png' or 'jpeg') in mensaje1[i].split('.'):

            Match=0;
            k=k+1
            receive = requests.get(mensaje1[i])
            lista_url.append(mensaje1[i])
            with open(r''+str(dir_downloads+'num'+str(i)+'.png'),'wb') as f:
                f.write(receive.content)

            print(' ---------------------------------------------------')
            print('|                 Screenshot '+str(k)+'                     |')
            print(' ---------------------------------------------------')

            directorio='pruebasBS4/'
            archivo='num'+str(i)+'.png'
            test=directorio+archivo
            img=cv2.imread(r''+test)
            cad=pytesseract.image_to_string(img)

            lista=[]
            lista=pytesseract.image_to_string(img).split()
            print(lista)

            for j in range(len(lista)-1):
                directorio='pruebasBS4/'
                archivo='num'+str(i)+'.png'
                test=directorio+archivo
                Archivo1=open('Salida'+'.txt','w')
                img=cv2.imread(r''+test)
                cad=pytesseract.image_to_string(img)
                Archivo1.write(cad)

                #print(pytesseract.image_to_string(img))

                print(' ---------------------------------------------------')
                print('|                 Screenshot '+str(i)+'                     |')
                print(' ---------------------------------------------------')

            if (lista !=[]):
            
                interPalabras = set (palabras).intersection(lista)
                interPlural = set(plural).intersection(lista)
                interAcento = set(acento).intersection (lista)
                interCaracter = set(caracter).intersection(lista)
            
                print("Las palabras repetidas de la tabla de Palabras son:")
                print ("1) -->"+ str(interPalabras))
                print ("2) -->"+ str(interPlural))
                print ("3) -->"+ str(interAcento))
                print ("4) -->"+ str(interCaracter))



                print("Las palabras repetidas de la tabla de Marcas son:")
                interProducto = set (producto).intersection(lista)
                interSubmarca = set(submarca).intersection(lista)
                interMarca = set(marca).intersection (lista)
                interAbreviatura = set(abreviatura).intersection (lista)
                print ("1) -->"+ str(interProducto))
                print ("2) -->"+ str(interSubmarca))
                print ("3) -->"+ str(interMarca))
                print ("4) -->"+ str(interAbreviatura))



                interClave = set (clave).intersection(lista)
                interTipo = set(tipo).intersection(lista)
                interConcepto = set(concepto).intersection (lista)
                print("Las palabras repetidas de la tabla de Productos son:")
                print ("1) -->"+ str(interClave))
                print ("2) -->"+ str(interTipo))
                print ("3) -->"+ str(interConcepto))
        
            else:
                print("La lista de Pytesseract esta vacía")
