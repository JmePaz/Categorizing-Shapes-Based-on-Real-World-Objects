def is_in_bound(point_to_check, point_range_A, point_range_B):
        return  point_range_A <= point_to_check and point_to_check <= point_range_B

#event handler for dragging
def move(canvas,img_obj, shape_bins):
    def highlight_shape_bins(orig_x, orig_y):
        #loop all through the shapes
        highlighted_color = "white"
        for shape_bin in shape_bins:
            is_inside_X = is_in_bound(orig_x, shape_bin.x, shape_bin.x2)
            is_inside_Y = is_in_bound(orig_y, shape_bin.y, shape_bin.y2)
            # if it is inside the shape bin
            if(is_inside_X and is_inside_Y):
                # highlight the shape bin
                canvas.itemconfig(shape_bin.instances_bin, fill=highlighted_color)
            else:
                canvas.itemconfig(shape_bin.instances_bin, fill=shape_bin.color)
        

    def move_img(e):
        orig_x, orig_y = map(int,(canvas.coords(img_obj.canvas_img)))
        new_x, new_y = (e.x-orig_x, e.y-orig_y)
        canvas.move(img_obj.canvas_img, new_x, new_y)
        #hightlighting the shape binns
        highlight_shape_bins(orig_x, orig_y)

    return move_img

#event handler for dropping
def release(canvas, img_obj, shape_bins):
    def reset_pos(curr_x, curr_y):
        orig_offset_pos = img_obj.offset_pos
        new_x, new_y = (orig_offset_pos[0]-curr_x, orig_offset_pos[1]-curr_y)
        canvas.move(img_obj.canvas_img, new_x, new_y)
        
    def success_sequence():
        canvas.delete(img_obj.canvas_img)
        # score is up

    def validate_bins(curr_x, curr_y):
        for shape_bin in shape_bins:
            is_inside_X = is_in_bound(curr_x, shape_bin.x, shape_bin.x2)
            is_inside_Y = is_in_bound(curr_y, shape_bin.y, shape_bin.y2)
            # if it is inside the shape bin
            if(is_inside_X and is_inside_Y):
                # if the answer is right
                if(img_obj.shape == shape_bin.shape_category):
                    print("right answer")
                    success_sequence()
                else:
                    print("wrong answer")
                    reset_pos(curr_x, curr_y)

                #get back through the shape color
                canvas.itemconfig(shape_bin.instances_bin, fill=shape_bin.color)
                
    def release_img(e):
        curr_x, curr_y = map(int, canvas.coords(img_obj.canvas_img))
        #loop all through 
        validate_bins(curr_x, curr_y)
        

    return release_img

import tkinter as tk
from PIL import ImageTk, Image
from FileManagement import FileManager
from ShapeBin import ShapeBin


window = tk.Tk()
w = 900
h = 650
window.geometry(f"{w}x{h}")
window.title("Shapey: Categorizing object's shapes")

#title
tk.Label(window, text="Drag and Drop Objects to their respective shapes", font=("Arial", 18)).pack()
tk.Label(window, text="Points: 0").pack()
#points

# canvas
canvas = tk.Canvas(window, width=int(w*50), height=(h*50), bg="gray")
canvas.pack()

#background 
bg_img = ImageTk.PhotoImage(Image.open("DataSets/DataTemp/Background.jpg"))
offsetCenterX= (w-bg_img.width())//2
offsetCenterY= 10

# creating box
nextPosY = offsetCenterY + bg_img.height() + 10

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

#Setting images 
bg = canvas.create_image(offsetCenterX, offsetCenterY, anchor=tk.NW, image=bg_img)

#get info about
fManager = FileManager()
dataList = fManager.get_info("DataSets/DataTemp/DataList.txt")

#loop all image objects
for img_fname, img_obj in dataList.items():
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
    canvas.tag_bind(img_obj_cnvs, "<ButtonRelease-1>", release(canvas, img_obj, shape_bins))


#looping
window.mainloop()