import tkinter as tk
from PIL import ImageTk, Image
from Classes.FileManagement import FileManager
from Classes.ShapeBin import ShapeBin
from Classes.EventHandler import move, release
from Classes.Player import PlayerScore


class GameFrame:
    def __init__(self, parent_window, main_app):
        #main_app
        self.main_app = main_app

        #initalize frame
        self.frame = tk.Frame(parent_window)
        self.w = parent_window.winfo_width()
        self.h = parent_window.winfo_height()
        self.dataList = None
        self.bg_img = None

        #load the game
        self.__load__game()
        #position
        self.frame.pack()
    
    def __load__game(self):
        #title
        tk.Label(self.frame, text="Drag and Drop Objects to their respective shapes", font=("Arial", 18)).pack()
        score_lbl = tk.Label(self.frame, text="Points: 0",fg="green", font=("Arial", 15))
        score_lbl.pack()

        #points

        # canvas
        canvas = tk.Canvas(self.frame, width=int(self.w*50), height=(self.h*50), bg="gray")
        canvas.pack()

        #background
        self.bg_img = ImageTk.PhotoImage(Image.open("DataSets/DataTemp/Background.jpg"))

        #setting off set position
        offsetCenterX= (self.w-450)//2
        offsetCenterY= 10

        #setting background to canvas
        bg = canvas.create_image(offsetCenterX, offsetCenterY, anchor=tk.NW, image=self.bg_img)

        # creating box
        nextPosY = offsetCenterY + self.bg_img.height() + 10

        #create Shape bins
        shape_bins = list()
        shape_bin_y2 =  nextPosY + 80
        #circle
        circle_bin = ShapeBin(canvas,offsetCenterX-150, nextPosY,offsetCenterX+100, shape_bin_y2, "yellow","circle")
        #rectangle
        rect_bin = ShapeBin(canvas,circle_bin.x2+10, nextPosY, circle_bin.x2+250, shape_bin_y2, "orange", "rectangle")
        #triangle
        tria_bin = ShapeBin(canvas, rect_bin.x2+10, nextPosY, rect_bin.x2+250, shape_bin_y2, "red","triangle")

        # shape bin row position 2
        shape_bin_row2_y1 = shape_bin_y2+20
        shape_bin_row2_y2 = shape_bin_y2+20+80
        #square
        square_bin = ShapeBin(canvas,offsetCenterX-150, shape_bin_row2_y1,offsetCenterX+100, shape_bin_row2_y2, "violet","square" )

        #rectangle
        penta_bin = ShapeBin(canvas,circle_bin.x2+10, shape_bin_row2_y1, circle_bin.x2+250, shape_bin_row2_y2, "green","pentagon")
        #triangle
        others_bin = ShapeBin(canvas, rect_bin.x2+10, shape_bin_row2_y1, rect_bin.x2+250, shape_bin_row2_y2, "indigo","others")

        # add all to the shape bins lst
        shape_bins.extend([circle_bin, rect_bin, tria_bin, square_bin, penta_bin, others_bin])


        #get info about
        fManager = FileManager()
        self.dataList = fManager.get_info("DataSets/DataTemp/DataList.txt")

        #Player Score Data
        player_score = PlayerScore(score=0, total=len(self.dataList), txtLbl = score_lbl)


        #loop all image objects
        for img_fname, img_obj in self.dataList.items():
            #set offset position
            img_obj.set_offset_pos(offsetCenterX, offsetCenterY )
            # Image creation
            img_obj_tk = ImageTk.PhotoImage(Image.open(f"DataSets/DataTemp/Objs/{img_fname}"))
            new_pos = img_obj.offset_pos
            img_obj_cnvs = canvas.create_image(new_pos[0], new_pos[1], anchor=tk.CENTER, image=img_obj_tk)
            
            #setting the actual image to image_obj
            img_obj.set_instance_img(img_obj_tk, img_obj_cnvs)

            #events binding
            #drag event
            canvas.tag_bind(img_obj_cnvs ,"<B1-Motion>", move(canvas, img_obj, shape_bins))
            #drop event
            canvas.tag_bind(img_obj_cnvs, "<ButtonRelease-1>", release(canvas, img_obj, shape_bins, player_score, self.main_app))

        
    def get_instance_frame(self):
        return self.frame
