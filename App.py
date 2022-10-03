import tkinter as tk
from tkinter import filedialog
from Classes.FileManagement import FileManager
from Game import GameFrame

class App:
    def __init__(self,title, w, h):
        self.w = w
        self.h = h
        self.window = tk.Tk()
        self.window.geometry(f"{w}x{h}")
        self.window.title(title)
        self.window.resizable(False, False)
        #load
        self.__load_app()

    def select_file(self):
        file_name = filedialog.askopenfilename()
        print("DIR", file_name)
        #move to the game sequence
        self.frame_app.destroy()
        self.frame_app = None
        self.frame_game = GameFrame(self.window, self)
        

    def __load_app(self):
        #frame
        self.frame_app = tk.Frame(self.window)
        self.frame_app.pack()

        #file
        file_btn = tk.Button(self.frame_app, text="Select an Image", command=self.select_file)
        file_btn.pack()

    def reload_app(self):
        self.__load_app()
        

    def run(self):
        self.window.mainloop()

app = App("Shapes Categorization", 775, 625)
app.run()