class ImageObj:
    def __init__(self, f_name, xPos, yPos, shape):
        self.f_name = f_name
        self.orig_x = xPos
        self.orig_y = yPos
        self.shape = shape
        self.offset_pos = (self.orig_x, self.orig_y)
        self.actual_img = None
        self.canvas_img = None
    
    def set_instance_img(self, actual_img, canvas_img):
        self.actual_img = actual_img
        self.canvas_img = canvas_img

    def set_offset_pos(self, off_set_x, off_set_y):
        self.offset_pos = (self.orig_x+off_set_x, self.orig_y+off_set_y)