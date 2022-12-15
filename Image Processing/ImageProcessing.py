from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk

import cv2
import numpy as np
import matplotlib.pyplot as plt
 
def to_grayscale(img) :
   img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

   return img


# search-based heuristic segmentation
def segmentation(img) :
   new_img = np.zeros(img.shape, dtype = "uint8")
   h, w = img.shape[:2]
   threshold = 0.8

   # for left and right direction, i is for row and j for column
   # left to right
   for i in range(2, h - 1) :
      for j in range(2, w - 1) :
         if(abs((int(img[i, j]) - int(img[i, j - 1])) / 2) > threshold * abs((int(img[i, j -1]) - int(img[i, j - 2]) / 2))) :
            new_img[i, j] = 255
            new_img[i - 1, j] = 255
            new_img[i + 1, j] = 255
            new_img[i, j - 1] = 255
            new_img[i, j + 1] = 255
            break

   # right to left
   for i in range(2, h - 1) :
      for j in range(w - 2, 2, -1) :
         if(abs((int(img[i, j]) - int(img[i, j - 1])) / 2) > threshold * abs((int(img[i, j -1]) - int(img[i, j - 2]) / 2))) :
            new_img[i, j] = 255
            new_img[i - 1, j] = 255
            new_img[i + 1, j] = 255
            new_img[i, j - 1] = 255
            new_img[i, j + 1] = 255
            break

   # for top and bottom direction, i is for column and j is for row
   # top to bottom
   for i in range(2, w - 1) :
      for j in range(h - 2, 2, -1) :
         if(abs((int(img[j, i]) - int(img[j - 1, i])) / 2) > threshold * abs((int(img[j - 1, i]) - int(img[j - 2, i]) / 2))) :
            new_img[j, i] = 255
            new_img[j - 1, i] = 255
            new_img[j + 1, i] = 255
            new_img[j, i - 1] = 255
            new_img[j, i + 1] = 255
            break

   # bottom to toi
   for i in range(2, w - 1) :
      for j in range(2, h - 1) :
         if(abs((int(img[j, i]) - int(img[j - 1, i])) / 2) > threshold * abs((int(img[j - 1, i]) - int(img[j - 2, i]) / 2))) :
            new_img[j, i] = 255
            new_img[j - 1, i] = 255
            new_img[j + 1, i] = 255
            new_img[j, i - 1] = 255
            new_img[j, i + 1] = 255
            break

   return new_img


def morphological_closing_and_opening(img) :
   kernel = np.ones((2,2), np.uint8)
   # morphological opening
   img = cv2.erode(img, kernel, iterations = 1)
   img = cv2.dilate(img, kernel, iterations = 1)

   # morphological closing
   img = cv2.dilate(img, kernel, iterations = 1)
   img = cv2.erode(img, kernel, iterations = 1)

   return img


# Vertical Image Projection
def vertical_image_projection(img, threshold) :
   v_proj = np.sum(img, 1)
   v_max = np.max(v_proj)
   y2 = 0
   y1 = 0
   y = img.shape[1]
   vertical = np.zeros((v_proj.shape[0], y))
   for row in range(img.shape[0]):
      cv2.line(vertical, (0, row), (int(v_proj[row] * y / v_max), row), (255, 255, 255), 1)

   v_height = vertical.shape[0]
   for i in range(v_height) :
      if(int(vertical[i][threshold]) == 255) :
         y1 = i
         break

   for j in range(v_height - 1, 1, -1) :
      if(int(vertical[j][threshold]) == 255) :
         y2 = j
         break

   print("Height of the object :", y2-y1)

   return y2-y1


# Horizontal Image Projection
def horizontal_image_projection(img, threshold) :
   h_proj = np.sum(img, 0)
   h_max = np.max(h_proj)
   x = img.shape[0]
   horizontal = np.zeros((x, h_proj.shape[0]))

   x2 = 0
   x1 = 0
   for col in range(img.shape[1]):
      cv2.line(horizontal, (col, 0), (col, int(h_proj[col] * x / h_max)), (255, 255, 255), 1)

   h_width = horizontal.shape[1]
   for i in range(h_width) :
      if(int(horizontal[threshold][i]) == 255) :
         x1 = i
         break

   for j in range(h_width - 1, 1, -1) :
      if(int(horizontal[threshold][j]) == 255) :
         x2 = j
         break

   print("Width of the object :", x2-x1)

   return x2-x1

def get_od_scaling_factor() :
   actual_measurements = np.array([109, 90, 76, 68, 56, 49, 42])
   pixel_measurements = np.array([423, 356, 331, 299, 251, 225, 176])
   scaling_factor = 0
   i=0

   for i in range(0, actual_measurements.size - 1) :
      scaling_factor += actual_measurements[i] / pixel_measurements[i]

   return scaling_factor / actual_measurements[i]

def get_length_scaling_factor() :
   actual_measurements = np.array([157, 124, 109, 88, 84, 69, 54])
   pixel_measurements = np.array([541, 432, 430, 345, 319, 273, 221])
   scaling_factor = 0
   i=0
   for i in range(0, actual_measurements.size - 1) :
      scaling_factor += actual_measurements[i] / pixel_measurements[i]

   return scaling_factor / actual_measurements[i]

def processImage(img):
    from PIL import Image, ImageTk
    global windows
    global image
    global PIL_img
    global canvas
    global processed_label
    global label

    # process image here
    img = ImageTk.getimage(image)
    w, h = img.size

    # convert Image to np array
    processed_img = np.asarray(img)
    processed_img = to_grayscale(processed_img)

    # segmented image
    processed_img = segmentation(processed_img)
   
    # image after morphological operations
    processed_img = morphological_closing_and_opening(processed_img)
    

    # convert np array to PIL image to display
    temp_img = Image.fromarray(processed_img)
    PIL_img = ImageTk.PhotoImage(temp_img)


    # getting the height and diameter
    pixel_height = vertical_image_projection(processed_img, 50)
    h_scalar_factor = get_length_scaling_factor()
    height = round(pixel_height * h_scalar_factor, 2)
    f_height = int(height * 10)

    pixel_diameter = horizontal_image_projection(processed_img, 50)
    d_scalar_factor = get_od_scaling_factor()
    diameter = round(pixel_diameter * d_scalar_factor, 2)
    f_diameter = int(diameter*10)

    # display image
    processed_label.destroy()
    processed_label = Label(windows,text="Processed Image", font=('Ariel', 22, 'bold'))
    processed_label.place(x=(w+(w/2)+100), y=7)

    label = Label(windows, image = PIL_img, width=w, height=h)
    label.place(x=(w+220),y=50)

    btnOpenImage = Button(windows, text="Open file", width=12, command=openDialog)
    txt_height =  str(f_height) + " mm"
    txt_diameter =  str(f_diameter) + " mm"
    # actual_h = "Actual Height: " + str(245)
    # actual_d = "Actual Diameter: " + str(245)

    canvas.delete("all") 
    canvas = Canvas(windows, height=600, width=450)
    canvas.place(x=w-30, y=h+80)
    canvas.create_rectangle(5, 5, 350, 150, outline='black')
    canvas.create_text(170,20, text="Report", font=('Ariel', 18, 'bold'))

    canvas.create_text(56, 60, text="Height: ", font=('Ariel', 14 ))
    canvas.create_text(123, 60, text=txt_height, font=('Ariel', 14 ))
    canvas.create_text(65, 80, text="Diameter: ", font=('Ariel', 14 ))
    canvas.create_text(143, 80, text=txt_diameter, font=('Ariel', 14 ))
   

def openDialog():
    from PIL import Image, ImageTk
    global windows
    global image
    global btnOpenImage
    global btnProcessImage
    global captured_label
    global processed_label
    global label
    address = filedialog.askopenfilename(initialdir="/Users/Rd/dev/thesis/Images/", title="Select file", 
    filetypes= (("Images", ("*.jpg", "*.png", "*.bmp")), ("All Items", "*.*")))

    img = Image.open(address)
    w, h = img.size
    new_w, new_h = int(w/4), int(h/4)
    img = img.resize((new_w, new_h))
    image = ImageTk.PhotoImage(img)

    canvas.delete("all")
    captured_label.destroy()
    label.destroy()
    processed_label.destroy()

    captured_label = Label(windows,text="Captured Image", font=('Ariel', 22, 'bold'))
    captured_label.place(x=((new_w/2)+40), y=7)
  
    label = Label(windows, image = image, width=(w/4), height=(h/4))
    label.place(x=150,y=50)

    btnProcessImage.config(state = NORMAL)
    btnProcessImage = Button(windows, text="Process Image", width=12, command=lambda: processImage(image), state=NORMAL)
    btnOpenImage = Button(windows, text="Open file", width=12, command=openDialog)
   

 # creating a  main window for the application
windows = Tk()
windows.title("Automatic Dimension Measurement of Griffin Beakers")
windows.geometry("900x1300")

# initializing elements inside the windows
captured_label = Label(windows,text="Captured Image", font=('Ariel', 22, 'bold'), fg='white')
processed_label = Label(windows,text="Processed Image", font=('Ariel', 22, 'bold'), fg='white')
canvas = Canvas(windows, height=600, width=450)
# label = Label(windows)

btnOpenImage = Button(windows, text="Open file", width=12, command=openDialog)
btnOpenImage.place(x=40,y=90)

btnProcessImage = Button(windows, text="Process Image", width=12, command=lambda: processImage(image), state=DISABLED)
btnProcessImage.place(x=40,y=130)


windows.mainloop()
