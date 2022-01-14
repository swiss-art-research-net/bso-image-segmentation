
import cv2
import numpy as np

from matplotlib import pyplot as plt
from IPython.display import display

class BSOImageCropping:
    
    showImages = False
    extension = 50
    
    METHOD_TRHESH = 0
    METHOD_CANNY = 1

    SELECT_SQUAREST = 0
    SELECT_LARGEST = 1
    
    def __init__(self, showImages=False):
        self.showImages = showImages
        
    def applyMorphologyClose(self, image):
        # Applie a Kernel that "smears" the image horizontally
        # and slightly downwards. Can help in some instances to
        # close gaps between shapes, e.g. text
        padding = 15
        kernel = np.ones((2,10), np.uint8)
        if image[image.shape[0]-padding][padding] > 127:
            return cv2.morphologyEx(255-image.copy(), cv2.MORPH_CLOSE, kernel)
        else:
            return cv2.morphologyEx(image.copy(), cv2.MORPH_CLOSE, kernel)
    
    def blurImage(self, image, amount=5):
        return cv2.blur(image.copy(), (amount, amount))
    
    def cannyImage(self, image):
        return cv2.Canny(image.copy(), 10, 120)
    
    def displayImage(self, image):
        plt.figure()
        plt.imshow(image)
        
    def erodeImage(self, image, iterations=5):
        kernel = np.ones((5,5),np.uint8)
        return cv2.erode(image.copy(), kernel, iterations)
        
    def extendImage(self, image):
        return cv2.copyMakeBorder(image.copy(), self.extension, self.extension, self.extension, self.extension, cv2.BORDER_REPLICATE)
    
    def makeBW(self, image):
        return cv2.cvtColor(image.copy(), cv2.COLOR_RGB2GRAY)
        
    def thresholdImage(self, image, invertImage=None):   
        padding = 5
        if invertImage == None:
            if image[image.shape[0]-padding][image.shape[1]-padding] > 127:
                thresholdMethod = cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU
            else:
                thresholdMethod = cv2.THRESH_BINARY+cv2.THRESH_OTSU
        elif invertImage == True:
            thresholdMethod = cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU
        else:
            thresholdMethod = cv2.THRESH_BINARY+cv2.THRESH_OTSU
        
        ret, thresh = cv2.threshold(image,0,255,thresholdMethod)   
        return thresh
    
    def cropImage(self, image, invertImage=None, preprocessMethod=METHOD_TRHESH, selectMethod=SELECT_SQUAREST):
        # Extend image to improve recognition of (document) edges that
        # are close to the image edge
        extendedImage = self.extendImage(image)
        
        # Convert image to Black and White
        grayImage = self.makeBW(extendedImage)
        
        # Smear or blur image to remove detail and close gaps
        morphImage = self.applyMorphologyClose(grayImage)
        #blurImage = self.blurImage(morphImage)
        
        # Binarise image
        if preprocessMethod == self.METHOD_CANNY:
            thresh = self.cannyImage(morphImage)
        else:
            thresh = self.thresholdImage(morphImage, invertImage)
        
        # Detect contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # (for debugging) Draw contours on image
        contourImage = np.zeros(extendedImage.shape)
        cv2.drawContours(contourImage, contours, -1, (0,255,0), 3)
            
        # Retrieve the areas of the contours and select n largest
        areas = [cv2.contourArea(c) for c in contours]
        indicesOfLargestContours = [areas.index(x) for x in sorted(areas, reverse=True)[:2]]
        
        # Pick contour based on selection method, either the largest contour detected
        # or the one which is closest in ratio to a square. The ratio method can be useful
        # to discard a colour calibration bar which might be detected
        if selectMethod == self.SELECT_SQUAREST:
            ratios = []
            for i in indicesOfLargestContours:
                x,y,w,h = cv2.boundingRect(contours[i])
                ratios.append(max(w,h)/min(w,h))
            indexToPick = np.argmin(ratios)
        elif selectMethod == self.SELECT_LARGEST:
            indexToPick = 0
        
        # (for debugging) Draw detected contours
        drawThickness = 8
        
        rectangleImage = extendedImage.copy()
        for i in indicesOfLargestContours:
            x,y,w,h = cv2.boundingRect(contours[i])
            cv2.rectangle(rectangleImage, (x, y) , (x + w, y + h), (0,255,0) ,drawThickness)
        
        # Retrieve coordinates of selected contour
        chosenX, chosenY, chosenW, chosenH = cv2.boundingRect(contours[indicesOfLargestContours[indexToPick]])
        
        x0 = chosenX
        x1 = chosenX + chosenW
        y0 = chosenY
        y1 = chosenY + chosenH
        
        # Remove border that has been added in the first step
        x0 = max(0, chosenX - self.extension)
        y0 = max(0, chosenY - self.extension)
        x1 = min(x0 + chosenW, image.shape[1])
        y1 = min(y0 + chosenH, image.shape[0])
        
        # (for debugging) Draw rectangle of selected region
        cv2.rectangle(rectangleImage, (chosenX, chosenY), (chosenX + chosenW, chosenY + chosenH), (255,0,0), drawThickness)

        croppedImage = image.copy()[y0:y1, x0:x1]
        
        if self.showImages:
            self.displayImage(image)
            #self.displayImage(morphImage)
            self.displayImage(thresh)
            self.displayImage(contourImage)
            self.displayImage(rectangleImage)
            self.displayImage(croppedImage)
            
        return x0, y0, x1-x0, y1-y0