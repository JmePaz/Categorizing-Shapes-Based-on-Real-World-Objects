def move(canvas,img):
    def move_image(e):
        orig_x, orig_y = map(int,(canvas.coords(img)))
        new_x, new_y = (e.x-orig_x, e.y-orig_y)
        canvas.move(img, new_x, new_y)
    return move_image
    

import tkinter as tk
from PIL import ImageTk, Image
from FileManagement import FileManager

window = tk.Tk()
w = 905
h = 700
window.geometry(f"{w}x{h}")
window.title("Shapey: Categorizing object's shapes")

# canvas
canvas = tk.Canvas(window, width=w, height=h, bg="white")
canvas.pack()
#background 
bg_img = ImageTk.PhotoImage(Image.open("DataSets/DataTemp/Background.jpg"))
print(bg_img.width(),bg_img.height())
bg = canvas.create_image(0,0, anchor=tk.NW, image=bg_img)

#get info about
fManager = FileManager()
dataList = fManager.get_info("DataSets/DataTemp/DataList.txt")
#loop all image objects
img_lists = []
for img_fname, img_obj in dataList.items():
    img_obj_tk = ImageTk.PhotoImage(Image.open(f"DataSets/DataTemp/Objs/{img_fname}"))
    img_obj_cnvs = canvas.create_image(img_obj.xPos, img_obj.yPos, anchor=tk.CENTER, image=img_obj_tk)
    canvas.tag_bind(img_obj_cnvs ,"<B1-Motion>", move(canvas, img_obj_cnvs))
    
    #set
    img_obj.set_actual_img(img_obj_tk)

#looping
window.mainloop()