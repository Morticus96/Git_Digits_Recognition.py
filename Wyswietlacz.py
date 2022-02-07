from imutils import contours
import imutils
import cv2
import numpy as np

CYFRY = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9,
}


wrap= cv2.imread("wrap.jpg")
cv2.imshow('wrap',wrap)
output= wrap

szary = cv2.cvtColor(wrap, cv2.COLOR_RGB2GRAY)
cv2.imshow('szary', szary)

retval, binarszary = cv2.threshold(szary, 50, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('binarszary', binarszary)

closing = cv2.morphologyEx(binarszary, cv2.MORPH_CLOSE, kernel=np.ones((5,5), np.uint8))
cv2.imshow('closing', closing)


kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
thresh = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
cv2.imshow('post process', thresh)

kontr = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
kontr = imutils.grab_contours(kontr)

zlicz = []


for c in kontr:
	(x, y, w, h) = cv2.boundingRect(c)

	if w >= 30 and (h >= 50 and h <= 70):
		zlicz.append(c)

zlicz = contours.sort_contours(zlicz,method="left-to-right")[0]
digits = []

for c in zlicz:
	(x, y, w, h) = cv2.boundingRect(c)

	print(x, y, w, h)
	cal = (w / h)

	if (cal < 0.3):
		digit = 1
	else:

		roi = thresh[y:y + h, x:x + w]


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
			segkraw = roi[yA:yB, xA:xB]
			total = cv2.countNonZero(segkraw)
			area = (xB - xA) * (yB - yA)

			if total / float(area) > 0.5:
				on[i]= 1


		digit = CYFRY[tuple(on)]
		digits.append(digit)
		cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)
		cv2.putText(output, str(digit), (x - 10, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

cv2.imshow("Input", wrap)
cv2.imshow("Output", output)
cv2.waitKey(0)