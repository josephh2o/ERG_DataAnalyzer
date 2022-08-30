import tkinter as tk
from PIL import Image, ImageTk
        
root = tk.Tk()
root.configure(bg = "white")
canvas = tk.Canvas(root, width = 640, height = 360, bd = 0, highlightthickness = 0, borderwidth = 0)
canvas.grid(columnspan = 3)
canvas.configure(bg = "white")    

logo = Image.open("resources/logo.png")
logo = ImageTk.PhotoImage(logo)
logoLabel = tk.Label(image = logo)
logoLabel.image = logo
logoLabel.grid(column = 1, row = 0)

instructions = tk.Label(root, text = "Select CSV files to read", font = "helvetica")
instructions.grid(columnspan = 3, column = 0, row = 1)

browseText = tk.StringVar()
browseText.set("Browse")
browseButton = tk.Button(root, textvariable = browseText)
browseButton.grid(column = 1, row = 2)

widgets = [root, canvas, logoLabel, instructions, browseButton]
for wid in widgets:
    wid.configure(bg = "white")

root.mainloop()