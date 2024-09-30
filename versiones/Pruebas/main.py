import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Crear un objeto VideoCapture
# El parámetro '0' se refiere al primer dispositivo de captura (webcam). Si tienes más de una cámara, puedes cambiar este número.
cap = cv.VideoCapture(0)

# Verificar si la captura se ha inicializado correctamente
if not cap.isOpened():
   print("No se puede abrir la cámara")
   exit()

ret, frame = cap.read()
bordes = cv.Canny(frame, 100, 200)

plt.ion()
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
# l = plt.imshow(bordes, cmap='gray')

axcolor = 'lightgoldenrodyellow'
ax_umbral1 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_umbral2 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)

slider1 = Slider(ax_umbral1, 'umbral1', 0, 300, valinit=100)
slider2 = Slider(ax_umbral2, 'umbral2', 0, 300, valinit=200)

# slider1.on_changed(update)
# slider2.on_changed(update)

# Leer la captura de la cámara en un bucle
while True:
   # Capturar frame por frame
   ret, frame = cap.read()

   # Si la captura ha fallado, sal del bucle
   if not ret:
      print("No se puede recibir frame (fin de la transmisión?). Saliendo ...")
      break

   # Convertir el frame a gris (opcional)
   # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
   # bordes = cv.Canny(gray, 60, 200)
   # Mostrar el frame resultante
   # cv.imshow('frame', frame)
   # cv.imshow('frame gris', gray) # Descomentar para mostrar el frame en escala de grises
   # cv.imshow('frame canny', bordes)

   umbral1 = slider1.val 
   umbral2 = slider2.val 
   print(umbral1, umbral2)
   bordes = cv.Canny(frame, umbral1, umbral2)

#    ax.clear()
   plt.imshow(bordes, cmap='gray')
   fig.canvas.flush_events()
   plt.show()


# Liberar el objeto de captura y cerrar todas las ventanas
cap.release()
cv.destroyAllWindows()