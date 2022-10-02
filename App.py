def move(canvas,img):
    def move_image(e):
        orig_x, orig_y = map(int,(canvas.coords(img)))
        new_x, new_y = (e.x-orig_x, e.y-orig_y)
        canvas.move(img, new_x, new_y)
    return move_image
    

def get_center(pointA , pointB):
    return pointA+(pointB-pointA)//2

import tkinter as tk
from PIL import ImageTk, Image
from FileManagement import FileManager

window = tk.Tk()
w = 900
h = 700
window.geometry(f"{w}x{h}")
window.title("Shapey: Categorizing object's shapes")

# canvas
canvas = tk.Canvas(window, width=int(w*50), height=(h*50), bg="gray")
canvas.pack()


#background 
bg_img = ImageTk.PhotoImage(Image.open("DataSets/DataTemp/Background.jpg"))
offsetCenterX= (w-bg_img.width())//2
offsetCenterY= 10

# creating box
nextPosY = offsetCenterY + bg_img.height() + 10

#create boxes
#circle
circleBox = canvas.create_rectangle(offsetCenterX-100, nextPosY,offsetCenterX+150, nextPosY+150,fill='yellow' )
center_pos_x = get_center(offsetCenterX-100, offsetCenterX+150)
center_pos_y = get_center( nextPosY, nextPosY+150)
circleText = canvas.create_text(center_pos_x,center_pos_y, text="Circle", fill="black", font=('Arial 18 bold'))
#rectangle



#Setting images
bg = canvas.create_image(offsetCenterX, offsetCenterY, anchor=tk.NW, image=bg_img)

#get info about
fManager = FileManager()
dataList = fManager.get_info("DataSets/DataTemp/DataList.txt")
#loop all image objects
img_lists = []
for img_fname, img_obj in dataList.items():
    img_obj_tk = ImageTk.PhotoImage(Image.open(f"DataSets/DataTemp/Objs/{img_fname}"))
    img_obj_cnvs = canvas.create_image(offsetCenterX+img_obj.xPos, offsetCenterY + img_obj.yPos, anchor=tk.CENTER, image=img_obj_tk)
    canvas.tag_bind(img_obj_cnvs ,"<B1-Motion>", move(canvas, img_obj_cnvs))
    
    #set
    img_obj.set_actual_img(img_obj_tk)


#looping
window.mainloop()