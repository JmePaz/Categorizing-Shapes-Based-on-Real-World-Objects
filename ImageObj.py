class ImageObj:
    def __init__(self, f_name, xPos, yPos, shape):
        self.f_name = f_name
        self.xPos = xPos
        self.yPos = yPos
        self.shape = shape
        self.actual_img = None
    
    def set_actual_img(self, actual_img):
        self.actual_img = actual_img