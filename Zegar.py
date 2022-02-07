from imutils import contours
from time import sleep
import imutils
import cv2
import numpy as np

DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 0, 1): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9,
}

zegar = cv2.imread('zegarek.jpg')
output = zegar

contrast = cv2.convertScaleAbs(zegar, alpha=1, beta=90)
cv2.imshow('kontrast', contrast)

szary = cv2.cvtColor(contrast, cv2.COLOR_RGB2GRAY)
cv2.imshow('szary', szary)

retval, binarszary = cv2.threshold(szary, 250, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('binarszary', binarszary)

dilation = cv2.dilate(binarszary, kernel=np.ones((5,5), np.uint8) , iterations = 1,)
cv2.imshow('dylatacja', dilation)

closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel=np.ones((5,5), np.uint8))
cv2.imshow('closing', closing)

retval, otsu = cv2.threshold(closing, 49, 255, cv2.THRESH_OTSU)
cv2.imshow('otsu', otsu)

erozja = cv2.erode(otsu,kernel=np.ones((5,5), np.uint8),iterations = 2)
cv2.imshow('erozja', erozja)


kontr = cv2.findContours(erozja.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
kontr = imutils.grab_contours(kontr)


zlicz = []

for c in kontr:
	(x, y, w, h) = cv2.boundingRect(c)

	if w >= 5 and (h >= 50 and h <= 350):
		zlicz.append(c)

zlicz = contours.sort_contours(zlicz, method="left-to-right")[0]
digits = []



for c in zlicz:
	(x, y, w, h) = cv2.boundingRect(c)
	print(x, y, w, h)
	cal = w/h
	if (cal <0.3):
		digit = 1
	else:

		roi = erozja[y:y + h, x:x + w]

		(roiH, roiW) = roi.shape
		(dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
		dHC = int(roiH * 0.05)

		segments = [
			((0, 0), (w, dH)),
			((0, 0), (dW, h // 2)),
			((w - dW, 0), (w, h // 2)),
			((0, (h // 2) - dHC) , (w, (h // 2) + dHC)),
			((0, h // 2), (dW, h)),
			((w - dW, h // 2), (w, h)),
			((0, h - dH), (w, h))
		]
		on = [0] * len(segments)

		for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
			xC=xB-xA
			yC=yB-yA

			#print('xA',xA,'xB', xB, 'xC', xC)
			#print('yA', yA, 'yB', yB, 'yC', yC)
			#print('xC/yC', xC/yC)

			if (xC / yC<0.2):
				digit = 1
			else:
				segkraw = roi[yA:yB, xA:xB]
				total = cv2.countNonZero(segkraw)
				area = (xB - xA) * (yB - yA)

				if area > 0.0:
					if total / float(area) > 0.4:
						on[i]= 1
				else:
					on[i]=0


		digit = DIGITS_LOOKUP[tuple(on)]
		digits.append(digit)
	cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
	cv2.putText(output, str(digit), (x - 10, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

cv2.imshow("Output", output)
cv2.waitKey(0)

sleep (5)