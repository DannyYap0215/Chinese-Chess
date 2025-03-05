import pygame as py  
import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()
root.title("中国象棋")
root.configure(bg="black")  

image = Image.open("images/mapWithWood.png")  
root_width, root_height = image.size  

root.geometry(f"{root_width + 100}x{root_height + 100}")
root.resizable(False,False)

map_image = ImageTk.PhotoImage(image)

map_panel = tk.Label(root, image=map_image, bg="black")
map_panel.place(relx=0.5, rely=0.5, anchor="center")  

root.mainloop()
