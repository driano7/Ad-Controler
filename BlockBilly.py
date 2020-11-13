import os
import sys
import cv2
import re
from PIL import Image
import pytesseract 
from os import remove
import mysql.connector
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

def buscarFicheros(directorio):
    ficheros=[]
    for base,dirs,files in os.walk(directorio):
        ficheros.append(files)
    return files

#Coneccion  BASE DE DTOS 
conn = mysql.connector.connect(host='MacBook-Air-de-Pinon.local',
user=os.environ.get('DB_USER'),password=os.environ.get('DB_PASS'),db='Datos_Publicidad')

# Obtención código fuente html 
URL=input('Ingrese el URL de la pagina a analizar: \n')
Inicio=time.process_time()
request=requests.get(URL)
bs=BeautifulSoup(request.text,'lxml')
Archivo1=open('/Users/billypinon2/Documents/Servicio/Version2/prueba'+'.html','w')
Archivo2=open('/Users/billypinon2/Documents/Servicio/Version2/salida'+'.html','w')
Archivo1.write(str(bs))
Archivo1.close()

#Parseo del código para obtener las imágenes
lista_url=[]
idiomas=['en','es','fr']
idioma=''
bandera=0
f = open ('/Users/billypinon2/Documents/Servicio/Version2/prueba.html','r')
mensaje = f.read()
mensaje1=mensaje.split('"')
dir_downloads = '/Users/billypinon2/Documents/Servicio/pruebas/'
imagen_local = 'num.png'
k=0
Match=0

for i in range(len(mensaje1)):
	if 'lang=' in mensaje1[i]:
		if mensaje1[i+1] in idiomas:
			idioma=idiomas.index(mensaje1[i+1])

	if 'path' in mensaje1[i]:
		print('siiii')
		mensaje1[i]=''
		if mensaje1[i+1]==':':
			mensaje1[i+1]=''

	if ('jpg' or 'png' or 'jpeg') in mensaje1[i].split('.'):
		if ('https') not in mensaje1[i].split(':'):
			print (mensaje1[i])
			Match=1

	if ('https' or 'http') in mensaje1[i].split(':'):
		bandera=0
		if 'meta' in mensaje1[i-1]:
			bandera=1
		if (bandera==0) and ('jpg' or 'png' or 'jpeg') in mensaje1[i].split('.'):

			Match=0;
			k=k+1
			receive = requests.get(mensaje1[i])
			lista_url.append(mensaje1[i])
			with open(r''+str(dir_downloads+imagen_local),'wb') as f:
				f.write(receive.content)

			print(' ---------------------------------------------------')
			print('|                 Screenshot '+str(k)+'                     |')
			print(' ---------------------------------------------------')

			directorio='/Users/billypinon2/Documents/Servicio/pruebas/'
			archivo='num.png'
			test=directorio+archivo
			img=cv2.imread(r''+test)
			cad=pytesseract.image_to_string(img)

			lista=[]
			lista=pytesseract.image_to_string(img).upper().replace('$',' $ ').replace('%',' % ').replace('"','').replace('\\','').replace('&','').replace('´','').replace('\’','').split(' ')

			for j in range(len(lista)):
	               
				#Busqueda en tabla Marcas_Prodcutos (PRODUCTO,SUBMARCA,MARCA,Abreviatura)
				Find_1=pd.read_sql_query('select mp.MARCA from Marcas_Productos as mp where mp.PRODUCTO = "'+lista[j]+'" or mp.SUBMARCA = "'+lista[j]+'" or mp.MARCA = "'+lista[j]+'" or mp.Abreviatura = "'+lista[j]+'";',conn)
				if len(Find_1)!=0:
					val = Find_1['MARCA'].values[0]
					texto='Word : "'+lista[j]+'" related to the brand: "'+str(val)+'"'
					Match=1

				#Busqueda en tabla palabras_clave (Palabra,Plural,Acento,Caracter)
				Find_1=pd.read_sql_query('select Palabra from palabras_clave as pc where pc.Palabra = "'+lista[j]+'" or pc.Plural = "'+lista[j]+'" or pc.Acento = "'+lista[j]+'" or pc.Caracter = "'+lista[j]+'";',conn)
				if len(Find_1)!=0:
					if lista[j]=='$':
						lista[j]=lista[j]+lista[j+1]
					val = Find_1['Palabra'].values[0]
					Match=1

				#Busqueda en tabla Productos_Varios (CLAVE,Tipo,Concepto)
				Find_1=pd.read_sql_query('select * from Productos_Varios as pv where pv.Tipo = "'+lista[j]+'" or pv.Concepto = "'+lista[j]+'";',conn)
				if len(Find_1)!=0:
					val2=Find_1['Tipo'].values[0]
					val3=Find_1['Concepto'].values[0]
					Match=1

			if Match==1:
				Archivo2.write('http://panorama-minero.com/wp-content/uploads/2018/01/fondo-blanco.png"')
			else:
				Archivo2.write(mensaje1[i]+'"')
			f.close()
			#remove(test)
		else:
			Archivo2.write(mensaje1[i]+'"')
	else:
		if Match==1:
			Archivo2.write('http://panorama-minero.com/wp-content/uploads/2018/01/fondo-blanco.png"')
		if i==len(mensaje1)-1:
			Archivo2.write(mensaje1[i]+'"')
		else:
			if i==0:
				Archivo2.write(mensaje1[i]+'"')
			else:
				Archivo2.write(mensaje1[i]+'"')

Archivo2.close()
Final=time.process_time() - Inicio
print(Final)






