#!/usr/bin/env python
# coding: utf-8

# In[2]:


import cv2
import numpy as np
from PIL import Image


# In[5]:


class ColorDescriptor:
   def __init__(self, bins):

      self.bins = bins  # we need to store the number of bins for the 3D histogram

   def describe(self, image):
      # firstly, convert the picture to the HSV color space and initialize
      # the features used to quantify the image
      image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
      features = []


      (h, w) = image.shape[:2]
      (cX, cY) = (int(w * 0.5), int(h * 0.5)) #h is the height of the image and w is width

      # divide the image into four parts (top-left,
      # top-right, bottom-right, bottom-left)
      segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
                  (0, cX, cY, h)]


      (X2, Y2) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
      elMask = np.zeros(image.shape[:2], dtype = "uint8")
      cv2.ellipse(elMask, (cX, cY), (int(X2), int(Y2)), 0, 0, 360, 255, -1)  # bulid an elliptical mask which stands for the center of the image



      for (startX,endX,startY,endY) in segments:
         # construct a mask for each corner of the image, subtracting
         # the elliptical center from it

         cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
         cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
         cornerMask = cv2.subtract(cornerMask, elMask)

         # extract a color histogram from each part, then update the
         # feature vector
         hist = self.histogram(image, cornerMask)
         features.extend(hist)

      # extract a color histogram from the elliptical region and
      # update the feature vector
      hist = self.histogram(image, elMask)
      features.extend(hist)

      # return the feature vector
      return features

   def histogram(self, image, mask):
      # extract a 3D color histogram from the masked region of the
      # image, using the supplied number of bins per channel; then
      # normalize the histogram
      hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
         [0, 180, 0, 256, 0, 256])
      hist = cv2.normalize(hist, hist).flatten()

      # return the histogram
      return hist


# In[ ]:




