import cv2
import numpy as np
import matplotlib.pyplot as plt
 
# read image
img = cv2.imread(r"C:\Users\acer\Documents\Thesis\LateralView\Cropped_LV_1000.jpg")


# resize the image using proportion
def grayscale_resize(img) :
   h, w = img.shape[:2]
   new_h, new_w = int(h / 4), int(w / 4)
   img = cv2.resize(img, (new_w, new_h))
   # cv2.imshow("Resized Image", img)
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
   # cv2.imshow("Vertical Projection", vertical)

   return y2-y1


# Horizontal Image Projection
def horizontal_image_projection(img, threshold) :
   h_proj = np.sum(img, 0)
   h_max = np.max(h_proj)
   x = img.shape[0]
   horizontal = np.zeros((x, h_proj.shape[0]))
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
   # cv2.imshow("Horizontal Projection", horizontal)

   return x2-x1

def get_od_scaling_factor() :
   actual_measurements = np.array([109, 90, 76, 68, 56, 49, 42])
   pixel_measurements = np.array([423, 356, 331, 299, 251, 225, 176])
   scaling_factor = 0

   for i in range(0, actual_measurements.size - 1) :
      scaling_factor += actual_measurements[i] / pixel_measurements[i]

   return scaling_factor / actual_measurements[i]

def get_length_scaling_factor() :
   actual_measurements = np.array([157, 124, 109, 88, 84, 69, 54])
   pixel_measurements = np.array([541, 432, 430, 345, 319, 273, 221])
   scaling_factor = 0

   for i in range(0, actual_measurements.size - 1) :
      scaling_factor += actual_measurements[i] / pixel_measurements[i]

   return scaling_factor / actual_measurements[i]

img = grayscale_resize(img)

# show segmented image
img = segmentation(img)
cv2.imshow("Segmented Image", img)

# show image after morphological operations
img = morphological_closing_and_opening(img)
cv2.imshow("Image after Operation", img)

# printing the scaling factors
# od = get_od_scaling_factor()
# length = get_length_scaling_factor()
# print(od)
# print(length)

cv2.waitKey(0)