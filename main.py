from imutils import contours
import imutils
import cv2
import numpy as np
from matplotlib import pyplot as plt

wrap= cv2.imread("zegarek.jpg")
#cv2.imshow('wrap',wrap)

#retval,binar = cv2.threshold(wrap , 50 , 255, cv2.THRESH_BINARY)
#cv2.imshow('binaryzacja', binar)

#resize = imutils.resize(wrap, width=500)

contrast = cv2.convertScaleAbs(wrap, alpha=1, beta=90)
cv2.imshow('kontrast', contrast)

szary = cv2.cvtColor(contrast, cv2.COLOR_RGB2GRAY)
cv2.imshow('szary', szary)

#plt.hist(szary.ravel(),256,[0,256]); plt.show()

retval, binarszary = cv2.threshold(szary, 250, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('binarszary', binarszary)

#retval, otsu = cv2.threshold(binarszary, 0, 255, cv2.THRESH_OTSU)
#cv2.imshow('otsu', otsu)

#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
#thresh = cv2.morphologyEx(otsu, cv2.MORPH_OPEN, kernel)

#erozja = cv2.erode(otsu,kernel=np.ones((5,5), np.uint8),iterations = 2)
#cv2.imshow('erozja', erozja)

dilation = cv2.dilate(binarszary, kernel=np.ones((5,5), np.uint8) , iterations = 1,)
cv2.imshow('dylatacja', dilation)

closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel=np.ones((5,5), np.uint8))
cv2.imshow('closing', closing)

retval, otsu = cv2.threshold(closing, 49, 255, cv2.THRESH_OTSU)
cv2.imshow('otsu', otsu)

#edged = cv2.Canny(otsu, 50, 200, 255)
#cv2.imshow('edged', edged)

#polaczenie = edged + erozja
#cv2.imshow('polaczenie', polaczenie)

#kros = cv2.getStructuringElement(cv2.MORPH_CROSS, (15, 15))
#img = cv2.morphologyEx(kros, cv2.MORPH_OPEN, kernel)

cv2.waitKey()











