import cv2
import numpy as np
from PIL import Image, ImageTk

CONST_ODSCALING = 0.36 #before 0.23
CONST_HSCALING = 0.32 #before 0.2

def get_ROI(image):
   #preprocessing
   last_row = image.shape[1]-1
   last_col = image.shape[0]-1
   image_to_process = image

   # getting upper left
   upper_left = (1,1)
   flag = False

   mid_col = int(last_col/2)
   mid_row = int(last_row/2)
   LR_three4ths_col = int(last_col/4)
   UL_three4ths_col = int(last_col * 0.75)

   for x in range(0, mid_row):
      for y in range(0, UL_three4ths_col):
         if(image_to_process[y,x] > 160):
               upper_left = (x,y)
               flag = True
               break
      if(flag):
         break

   # getting lower right X
   lower_right = (0,0)
   flag = False

   for x in range(last_row-2, mid_row, -1):
      for y in range(last_col-2, LR_three4ths_col, -1):
         if(image_to_process[y,x] > 110):
               lower_right = (x, 0)
               upper_left = (upper_left[0], y)
               flag = True
               break
      if(flag):
         break

   flag = False

   # gets the right Y for lower right
   for x in range(last_col-2, mid_col, -1):
      for y in range(last_row-2, mid_row, -1):
         if(image_to_process[x,y] > 160):
               lower_right = (lower_right[0], x)
               flag = True
               break
      
      if(flag):
         break

   x1 = upper_left[0] - 30
   x2 = lower_right[0] + 25

   y1 = upper_left[1] - 25
   y2 = lower_right[1] + 20

   ROI = image_to_process[y1:y2, x1:x2]
   
   # return img
   return ROI

# search-based heuristic segmentation
def segmentation(image) :
   # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   new_img = np.zeros(image.shape, dtype = "uint8")
   h, w = new_img.shape[:2]
   threshold = 2
   img = image
   
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
   
   # display segmented image
   cv2.imshow("Segmented Image", new_img)

   return new_img

def morphological_closing_and_opening(image) :
   img = image
   kernel = np.ones((2, 2), np.uint8)
   # morphological opening
   img = cv2.erode(img, kernel, iterations = 1)
   img = cv2.dilate(img, kernel, iterations = 1)

   # morphological closing
   img = cv2.dilate(img, kernel, iterations = 1)
   img = cv2.erode(img, kernel, iterations = 1)

   # display post processed image
   # cv2.imshow("Post Processing Image", img)

   return img


# Vertical Image Projection for Length
def vertical_image_projection(image) :
   img = image
   threshold = 40
   v_proj = np.sum(img, 1)
   v_max = np.max(v_proj)
   y = img.shape[1]
   vertical = np.zeros((v_proj.shape[0], y))
   for row in range(img.shape[0]):
      cv2.line(vertical, (0, row), (int(v_proj[row] * y / v_max), row), (255, 255, 255), 1)

   cv2.imshow("Vertical Projection", vertical)

   v_height = vertical.shape[0]
   for i in range(v_height) :
      if(int(vertical[i][threshold]) == 255) :
         y1 = i
         break

   for j in range(v_height - 1, 1, -1) :
      if(int(vertical[j][threshold]) == 255) :
         y2 = j
         break
   
   result = y2-y1
   # print(result)
   return result

# Horizontal Image Projection for OD
def horizontal_image_projection(image) :
   img = image
   threshold = 110
   h_proj = np.sum(img, 0)
   h_max = np.max(h_proj)
   x = img.shape[0]
   horizontal = np.zeros((x, h_proj.shape[0]))

   for col in range(img.shape[1]):
      cv2.line(horizontal, (col, 0), (col, int(h_proj[col] * x / h_max)), (255, 255, 255), 1)

   cv2.imshow("Horizontal Projection", horizontal)

   h_width = horizontal.shape[1]
   for i in range(h_width) :
      if(int(horizontal[threshold][i]) == 255) :
         x1 = i
         break

   for j in range(h_width - 1, 1, -1) :
      if(int(horizontal[threshold][j]) == 255) :
         x2 = j
         break

   result = x2- x1
   # print(result)
   return x2-x1

def identify_volume(length, od) :
   if(39 <= od <= 43 and length <= 60) :
      return "50mL"
   
   elif(48 <= od <= 52 and length <=75) :
      return "100mL"
   
   elif(55 <= od <= 59 and length <= 90) :
      return "150mL"
   
   elif(66 <= od <= 70 and length <= 100) :
      return "250mL"
   
   elif(75 <= od <= 79 and length <= 120) :
      return "400mL"
   
   elif(85 <= od <= 91 and length <= 135) :
      return "600mL"
   
   elif(105 <= od <= 111 and length <= 160) :
      return "1L"
   
   else :
      return "Defective"