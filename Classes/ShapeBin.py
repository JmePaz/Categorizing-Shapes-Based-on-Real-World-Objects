class ShapeBin:
    def __init__(self, parent_canvas,x,y, x2, y2, color, shape_category=None):
        self.parent_canvas = parent_canvas
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.width = x2-x
        self.height = y2-y
        self.color = color
        self.shape_category = shape_category

        #create a shape
        self.instances_bin = self.__create_shape_box()
        self.create_lbl_text(self.shape_category, "black")
    
    def __create_shape_box(self):
        return self.parent_canvas.create_rectangle(self.x,self.y,self.x+self.width,self.y+self.height,fill=self.color)

    def create_lbl_text(self, txtLbl, color):
        center_pos_x = self.get_center(self.x, self.x+self.width)
        center_pos_y = self.get_center(self.y,self.y+self.height)
        self.parent_canvas.create_text(center_pos_x,center_pos_y, text=txtLbl, fill=color, font=('Arial 18 bold'))
    
    def get_center(self,pointA , pointB):
        return pointA+(pointB-pointA)//2
    
    