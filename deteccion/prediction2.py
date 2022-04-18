from PIL import Image
import base64
#import torch
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime
import cv2
import os



class foodDetection:
    #constructor de la clase
    def __init__(self):
       # if versionx!=123:
       #     model=torch.hub.load('ultralytics/yolov5','yolov5s')
       #     self.model=model
        versionx=123

    #metodo que realiza la prediccion
    def predict(self,image_64,self_model):
        
        #verificamos y creamos los directorios de trabajo
        if os.name=='nt':
            base_file_path = '/tmp' 
        else:
            base_file_path = '/tmp' 
        os.makedirs(os.path.dirname(base_file_path), exist_ok=True)

        #volvemos a codificar la imagen y la guardamos su formato
        PATH_IMAGE = base_file_path+"/image_input.jpg"
        image_result = open(PATH_IMAGE,"wb")
        imagenbin=base64.b64decode(image_64)
        image_result.write(imagenbin)
        image_result.flush()
        image_result.close()

        #leemos la imagen y detectamos los objetos
        imgx = cv2.imread(PATH_IMAGE)
        results = self_model(imgx)
        image_name='image_input.jpg'
        objects_detection(image_name,base_file_path,results)

        
#------------------------------------------
#gestion del contador de detecciones
#import os

def ges_contador(ipath_base):
    
    fcontador = ipath_base+'/contador.txt'  
    if os.path.isfile(fcontador):
      fconta=open(fcontador,'r+')
      fconta.seek(0)
      ncontador=int(fconta.read())
      ncontador=ncontador+1
      #print(ncontador)
      fconta.seek(0)
      fconta.write(str(ncontador))
    else:
      ncontador=1
      fconta=open(fcontador,'w')
      fconta.write(str(ncontador))
    fconta.flush()
    fconta.close()
    return ncontador


#Función de gestion del csv
#from datetime import datetime
#import os

def ges_csv(ipath_base,ndeteccion,det_result):
  #obtenemos la fecha actual
  now = datetime.now() # current date and time
  fecha=now.strftime("%Y%m%d")
  #verficamos la existencia del csv
  #file_csv='/content/yolov5/models/data/images/datos_detection_Datos_Detection_20220328.csv' 
  file_csv=ipath_base+'/datos_detection_Datos_Detection_'+fecha+'.csv'
  if os.path.isfile(file_csv):
     fcsv=open(file_csv,'a+')
     fcsv.seek(2)
  else:
    fcsv=open(file_csv,'w')
    fcsv.write('id_detection,product,qty_detected,image_url,date_created\n')
  #analizamos los objetos obtenios
  lista_objetos=[]
  c_lista_objetos=[]

  for i in range(len(det_result)):
    objeto=det_result.loc[i,'name']
    if objeto not in lista_objetos:
      lista_objetos.append(objeto)
      c_lista_objetos.append(1)
    else:
      posicion=lista_objetos.index(objeto)
      xcant=c_lista_objetos[posicion]
      xcant=xcant+1
      c_lista_objetos[posicion]=xcant
  fecha=now.strftime("%Y-%m-%d")
  for i in range(len(lista_objetos)):  
    cadena=str(ndeteccion)+','+lista_objetos[i]+','+str(c_lista_objetos[i])+','+ipath_base+'/detection_'+str(ndeteccion)+'.jpg'+','+fecha+'\n'
    fcsv.write(cadena)    
  fcsv.flush()
  fcsv.close()
  

  #1,potato,2,https://storage.googleapis.com/kcp-bucket-01/datos_images_out/detection_1.png,2022-03-28
  

#programa de gestion de imagenes

def objects_detection(imagen,ipath_base,xresults):
  #hacemos la deteccion
  #fimg=ipath_base+'/'+imagen
  #results = model(fimg) 
  xresult=xresults.pandas().xyxy[0] 

  #verificamos que se ha realizado alguna deteccion
  if len(xresult)>0:
    ndeteccion=ges_contador(ipath_base) #contador de detecciones que llevamos
    #almacenamos la imagen en disco
    xresults.render()  # updates results.imgs with boxes and labels
    IMAGE_FILE=ipath_base+'/deteccion_'+str(ndeteccion)+'.jpg'
    plt.imsave(IMAGE_FILE,xresults.imgs[0])
    #gestionamos el csv con el regisro de lo detectado
    ges_csv(ipath_base,ndeteccion,xresult)


