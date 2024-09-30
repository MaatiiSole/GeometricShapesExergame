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

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
l = ax.imshow(bordes, cmap='gray')
axcolor = 'lightgoldenrodyellow'
ax_umbral1 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_umbral2 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
slider1 = Slider(ax_umbral1, 'umbral1', 0, 300, valinit=100)
slider2 = Slider(ax_umbral2, 'umbral2', 0, 300, valinit=200)

# Leer la captura de la cámara en un bucle
while True:
   # Capturar frame por frame
   ret, frame = cap.read()

   # Si la captura ha fallado, sal del bucle
   if not ret:
      print("No se puede recibir frame (fin de la transmisión?). Saliendo ...")
      break

   umbral1 = slider1.val 
   umbral2 = slider2.val 
   # print(umbral1, umbral2)
   bordes = cv.Canny(frame, umbral1, umbral2)
   l.set_data(bordes)
   plt.draw()
   plt.pause(0.01)

   # Salir del bucle al presionar 'q'
   if cv.waitKey(1) == ord('q'):
      break

# Liberar el objeto de captura y cerrar todas las ventanas
cap.release()
cv.destroyAllWindows()
