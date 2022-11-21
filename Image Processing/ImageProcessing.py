import cv2
import numpy as np
import matplotlib.pyplot as plt
 
# Read image
img = cv2.imread(r"C:\Users\acer\Documents\Thesis\LateralView\Cropped_LV_100.jpg")
# show image
# cv2.imshow("Image", image)
# cv2.waitKey(0)
 
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
# h, w = image.shape[:2]
# new_h, new_w = int(h / 4), int(w / 4)
# img = cv2.resize(image, (new_w, new_h))
# cv2.imshow("Image", img)
# cv2.waitKey(0)

# Extracting ROI automatically
h, w = img.shape[:2]
new_h, new_w = int(h / 4), int(w / 4)
img = cv2.resize(img, (new_w, new_h))
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
_, img = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

v_proj = np.sum(img, 1)
v_max = np.max(v_proj)
y = img.shape[1]
vertical = np.zeros((v_proj.shape[0], y))
for row in range(img.shape[0]):
   cv2.line(vertical, (0, row), (int(v_proj[row] * y / v_max), row), (255, 255, 255), 1)

cv2.imshow("Vertical Projection", vertical)

h_proj = np.sum(img, 0)
h_max = np.max(h_proj)
x = img.shape[0]
horizontal = np.zeros((x, h_proj.shape[0]))
for col in range(img.shape[1]):
   cv2.line(horizontal, (col, 0), (col, int(h_proj[col] * x / h_max)), (255, 255, 255), 1)

cv2.imshow("Horizontal Projection", horizontal)
cv2.imshow("Image", img)

# segmentation
# gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# _, img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
# # cv2.imshow("Image", img)
# # cv2.waitKey(0)

# # morphological operations
# kernel = np.ones((5,5),np.uint8)
# img = cv2.erode(img, kernel, iterations = 1)
# img = cv2.dilate(img, kernel, iterations = 1)
# cv2.imshow("Image", img)
# cv2.waitKey(0)

cv2.waitKey(0)