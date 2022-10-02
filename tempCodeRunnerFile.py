bg_img = ImageTk.PhotoImage(Image.open("DataSets/DataTemp/Background.jpg"))
print(bg_img.width(),bg_img.height())
bg = canvas.create_image(0,0, anchor=tk.NW, image=bg_img)