import cv2
class ShapeDetector:
  def __init__(self):
    pass
  def detect(self, c):
    #initialize the shape name and appro
    shape = "unindentified"
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.03*peri, True)

    if(len(approx)==3) :
      shape = "triangle"
    elif len(approx) == 4:
      (x, y, w, h) = cv2.boundingRect(approx)
      ar = w/float(h)
      shape = "square" if 0.95 <= ar and ar<= 1.05 else "rectangle"
    elif len(approx) == 5:
      shape = "pentagon"
    else:
      shape = "circle"
    
    return shape