import cv2
class ShapeDetector:
  @classmethod
  def detect(cls, c, debugName=""):
    #initialize the shape name and appro
    shape = None
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.0090*peri, True)
    approx_len = len(approx)

    if approx_len==3:
      shape = "triangle"

    elif approx_len == 4:
      (x, y, w, h) = cv2.boundingRect(approx)
      ratio = min(w,h)/max(w,h)
      if ratio >= 0.94:
        shape = "square"
      else:
        shape = "rectangle"

    elif approx_len == 5:
      shape = "pentagon"

    elif 6 <= approx_len and approx_len <= 14:
      shape = "others" 

    elif approx_len >= 15:
      shape = "circle"
    
    return shape