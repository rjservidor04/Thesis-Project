import cv2
import numpy as np
import matplotlib.pyplot as plt
 
# Read image
img = cv2.imread(r"C:\Users\acer\Documents\Thesis\LateralView\Cropped_LV_100.jpg")

# show loaded image
# cv2.imshow("Loaded Image", image)
 
# # Manual Selection of ROI
# r = cv2.selectROI("select the area", image)
# cropped_image = image[int(r[1]):int(r[1]+r[3]),
#                       int(r[0]):int(r[0]+r[2])]
# cv2.imshow("Cropped image", cropped_image)
# cv2.waitKey(0)

# #resize the image with specified size
# img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# img = cv2.resize(img, (256, 256))
# cv2.imshow("Image", img)
# cv2.waitKey(0)

# resize the image using proportion
h, w = img.shape[:2]
new_h, new_w = int(h / 4), int(w / 4)
img = cv2.resize(img, (new_w, new_h))
cv2.imshow("Resized Image", img)
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# Image Projection
# h, w = img.shape[:2]
# new_h, new_w = int(h / 4), int(w / 4)
# img = cv2.resize(img, (new_w, new_h))
# gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# _, img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Vertical Image Projection
# v_proj = np.sum(img, 1)
# v_max = np.max(v_proj)
# y = img.shape[1]
# vertical = np.zeros((v_proj.shape[0], y))
# for row in range(img.shape[0]):
#    cv2.line(vertical, (0, row), (int(v_proj[row] * y / v_max), row), (255, 255, 255), 1)
# cv2.imshow("Vertical Projection", vertical)

# Horizontal Image Projection
# h_proj = np.sum(img, 0)
# h_max = np.max(h_proj)
# x = img.shape[0]
# horizontal = np.zeros((x, h_proj.shape[0]))
# for col in range(img.shape[1]):
#    cv2.line(horizontal, (col, 0), (col, int(h_proj[col] * x / h_max)), (255, 255, 255), 1)
# cv2.imshow("Horizontal Projection", horizontal)
# cv2.imshow("Image", img)

# threshold segmentation
# gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
# # cv2.imshow("Image", img)

# search-based heuristic segmentation
def segment() :
   new_img = np.zeros(img.shape, dtype = "uint8")
   h, w = img.shape[:2]
   threshold = 0.8

   # for left and right direction, i is for row and j for column
   # left to right
   for i in range(2, h) :
      for j in range(2, w) :
         if(abs((int(img[i, j]) - int(img[i, j - 1])) / 2) > threshold * abs((int(img[i, j -1]) - int(img[i, j - 2]) / 2))) :
            new_img[i, j] = 255
            new_img[i - 1, j] = 255
            new_img[i + 1, j] = 255
            new_img[i, j - 1] = 255
            new_img[i, j + 1] = 255
            break

   # right to left
   for i in range(2, h) :
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
      for j in range(2, h) :
         if(abs((int(img[j, i]) - int(img[j - 1, i])) / 2) > threshold * abs((int(img[j - 1, i]) - int(img[j - 2, i]) / 2))) :
            new_img[j, i] = 255
            new_img[j - 1, i] = 255
            new_img[j + 1, i] = 255
            new_img[j, i - 1] = 255
            new_img[j, i + 1] = 255
            break

   return new_img

new_img = segment()
cv2.imshow("Segmented Image", new_img)
img = new_img

# morphological operations
kernel = np.ones((2,2   ),np.uint8)

# morphological closing
img = cv2.dilate(img, kernel, iterations = 1)
img = cv2.erode(img, kernel, iterations = 1)

# morphological opening
img = cv2.erode(img, kernel, iterations = 1)
img = cv2.dilate(img, kernel, iterations = 1)

cv2.imshow("Image after Operation", img)

# Vertical Image Projection
v_proj = np.sum(img, 1)
v_max = np.max(v_proj)
y = img.shape[1]
vertical = np.zeros((v_proj.shape[0], y))
for row in range(img.shape[0]):
   cv2.line(vertical, (0, row), (int(v_proj[row] * y / v_max), row), (255, 255, 255), 1)
cv2.imshow("Vertical Projection", vertical)

# Horizontal Image Projection
h_proj = np.sum(img, 0)
h_max = np.max(h_proj)
x = img.shape[0]
horizontal = np.zeros((x, h_proj.shape[0]))
for col in range(img.shape[1]):
   cv2.line(horizontal, (col, 0), (col, int(h_proj[col] * x / h_max)), (255, 255, 255), 1)
cv2.imshow("Horizontal Projection", horizontal)

cv2.waitKey(0)