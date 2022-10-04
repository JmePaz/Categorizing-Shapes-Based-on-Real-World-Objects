import tkinter.messagebox as tkM
from Classes.FileManagement import FileManager

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
        #hightlighting the shape bins
        highlight_shape_bins(orig_x, orig_y)

    return move_img

#event handler for dropping
def release(canvas, img_obj, shape_bins, player_score, main_app):
    def reset_pos(curr_x, curr_y):
        orig_offset_pos = img_obj.offset_pos
        new_x, new_y = (orig_offset_pos[0]-curr_x, orig_offset_pos[1]-curr_y)
        canvas.move(img_obj.canvas_img, new_x, new_y)
        
    def success_sequence():
        #delete the object img
        canvas.delete(img_obj.canvas_img)
        # score is up
        player_score.gain_points()
        # validate if it has full score
        if(player_score.is_full_score()):
            tkM.showinfo("Congratulations!", "You have solved it!")


    def validate_bins(curr_x, curr_y):
        for shape_bin in shape_bins:
            is_inside_X = is_in_bound(curr_x, shape_bin.x, shape_bin.x2)
            is_inside_Y = is_in_bound(curr_y, shape_bin.y, shape_bin.y2)
            # if it is inside the shape bin
            if(is_inside_X and is_inside_Y):
                # if the answer is right
                if(img_obj.shape == shape_bin.shape_category):
                    is_finished = success_sequence()
                else:
                    #else if its wrong
                    reset_pos(curr_x, curr_y)
                    break

                #get back through the shape color
                if(not player_score.is_full_score()):
                    canvas.itemconfig(shape_bin.instances_bin, fill=shape_bin.color)
                
           
    def is_out_canvas(curr_x, curr_y):
        canvas_w = canvas.winfo_width()
        canvas_h = canvas.winfo_height()
        canvas_x = canvas.winfo_rootx()
        canvas_y = canvas.winfo_rooty()
        return not (is_in_bound(curr_x, canvas_x, canvas_x + canvas_w) and is_in_bound(curr_y, canvas_y, canvas_y + canvas_h) )


    def release_img(e):
        curr_x, curr_y = map(int, canvas.coords(img_obj.canvas_img))
        #check 
        if(is_out_canvas(curr_x, curr_y)):
            reset_pos(curr_x, curr_y)
        #loop all through shape bins
        validate_bins(curr_x, curr_y)   
        # if the game is finished
        if(player_score.is_full_score()):
            # clear all temp files
            FileManager.remove_allfiles("DataSets/DataTemp")
            # back to main app
            main_app.frame_game.frame.destroy()
            main_app.frame_game = None
            main_app.reload_app()
            return

    return release_img


