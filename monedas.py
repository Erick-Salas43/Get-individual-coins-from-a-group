#Python 3.7.3 de RoboDK 
#opencv-python 4.2.0.32 || pip install opencv-python 

#Documentacion de opencv 4.2
#https://docs.opencv.org/4.2.0/d2/d96/tutorial_py_table_of_contents_imgproc.html
#Abrir camara, guardar video, leer video
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html


# Realizar un algoritmo de reconocimiento de placa
# para estacionamiento  

# Erick Salas 02 abril 2020

# Metodo de watershed
# https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html
# Metodo de detector de bordes Canny y filtro gauss
# https://programarfacil.com/blog/vision-artificial/detector-de-bordes-canny-opencv/

# Metodo detector de circulos
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html
# Documentacion de parametros funcion de circulos
# https://docs.opencv.org/2.4/modules/imgproc/doc/feature_detection.html

# Conversion de pixeles a mm
# https://www.pixelto.net/px-to-mm-converter
# dpi is the pixel density or dots per inch.
# 96 dpi means there are 96 pixels per inch.  =1 in = 96 px
# 1 inch is equal to 25.4 millimeters.         1 in = 25.4 mm   .:. 25.4 mm = 96 px .:. 25.4 mm / 96 px

# Información acerca de diametro de las monedas de acuerdo a Banxico
# https://www.banxico.org.mx/billetes-y-monedas/disenos-actuales-circulacion-.html
# Moneda   Radio  Familia
# $0.05 = 7.75 mm  (Familia C)
# $0.10 = 7 mm     (Familia D)
# $0.20 = 7.65 mm  (Familia D)
# $0.50 = 11 mm    (Familia B) Dodecagonal || https://www.banxico.org.mx/billetes-y-monedas/monedas-centavos-circulacion-.html
# $0.50 = 8.5 mm   (Familia D)
# $1 	= 10.5 mm  (Familia C)
# $2 	= 11.5 mm  (Familia C)
# $5    = 12.75 mm (Familia C)
# $10   = 14 mm    (Familia C)
# $20   = 16 mm    (Familia C)




# Escalar la fotografia, Metodo para obtener diametros originales
# https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
# Foto fifty tiene 13.5mm para $0.50 -> 8.5 mm deberia de tener, tiene una diferencia de 5mm
# si 	100% es 8.5  mm  
# then    x  es 5    mm 58.82
# Metodo que ubique una moneda por su numero y que en base a eso
# Haga el redimensionamiento

# Recortar img de acuerdo a coordenadas proporcionadas
# https://stackoverflow.com/questions/50696090/cropping-an-image-in-using-opencv-function-for-python 


# Primer metodo se basa en identificacion del valor de la moneda
# de acuerdo a su tamaño
# El segundo metodo se basa en identificacion del numero impreso en la moneda
# evidentemente el primer metodo es funcional en cualquier caso, por el hecho
# que no necesita que las monedas esten de "cara"
import numpy as np
import cv2

ax = 11
aplicar_escala,escala= 0 , 60  #0:NO 1:SI
valor_inicial = 120

formato = str(ax)+'.jpg'
img = cv2.imread(formato) #Abre la imagen en la variable img.
img2 = cv2.imread(formato)

if aplicar_escala == 1:

	width = int(img.shape[1]*escala/100)
	height = int(img.shape[0]*escala/100) 
	img = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)

	esc = 100+escala*2
	width1 = int(img.shape[1]*esc/100)
	height1 = int(img.shape[0]*esc/100) 
	img2 = cv2.resize(img2, (width1, height1), interpolation = cv2.INTER_AREA) 


gaussiano = cv2.GaussianBlur(img,(7, 7), 0) #Aplica filtro gauss a la imagen para suaviazarlo
gray = cv2.cvtColor(gaussiano,cv2.COLOR_BGR2GRAY) #Lo pasa de RGB a escala de grises

def nothing(x):
    pass
#
cv2.namedWindow('Configuracion')
cv2.resizeWindow('Configuracion', 400, 50)
cv2.createTrackbar('diam', 'Configuracion',valor_inicial,300,nothing)



#100,40

def circulos(parametro1):
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=parametro1,param2=parametro1-20,minRadius=0,maxRadius=0)
	circles = np.uint16(np.around(circles))
	for pt in circles[0, :]:
		x, y, r = pt[0], pt[1], pt[2]
		cv2.circle(img,(x, y), r,(0, 255, 0),2)
	return parametro1, circles

pq = 0
while (True):
	par1 = cv2.getTrackbarPos('diam', 'Configuracion')
	kj,datos = circulos(par1)
	cv2.imshow("arn", img)
	if cv2.waitKey(1) & 0xFF == ord('s'):
		cv2.destroyAllWindows()
		break

eleccion = input("¿Desea guardar? y/n: ")
if (eleccion != 'y'):
		print("Vuelva pronto")
elif (eleccion == 'y'):
	diam = kj
	circles = datos
	pq = 0
	for pt in circles[0, :]: 
		x, y, r = pt[0], pt[1],pt[2]
		if aplicar_escala == 1:
			xaux = int(x*escala*2/100)
			yaux = int(y*escala*2/100)
			raux = int(r*escala*2/100)
			x = x+xaux
			y = y+yaux
			r = r+raux
			d = r*2
		xa = x-r-8
		ya = y-r-8
		d = 2*r
		h = d+ya+16
		k = d+xa+16
		df = img2[ya:h, xa:k]
		pq = pq + 1
		apu = str(ax)+'a'+str(pq)+'.jpg'
		print(apu)
		cv2.imwrite(apu,df)
cv2.waitKey(0)

