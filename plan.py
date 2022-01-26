import tkinter
from tkinter import *
from stib import arret


print(arret(1755))

root = Tk()

Canvas = Canvas(root, width=900, height=900)

Canvas.pack()

plan = PhotoImage(file= "map.png")

placerImage = Canvas.create_image(836,817,anchor=SE, image=plan)

#13EN-83B
label1 = tkinter.Label(master=Canvas, text = arret(1746))
label1.place(x=175, y=520)

#14UZ
label2 = tkinter.Label(master=Canvas, text = arret(1755))
label2.place(x=150, y=300)

#14GdN-83VM
label3 = tkinter.Label(master=Canvas, text = arret(1768))
label3.place(x=450,y=450)

label4 = tkinter.Label(master=Canvas, text = arret(1711))
label4.place(x=300,y=100)

label5 = tkinter.Label(master=Canvas, text = arret(1680))
label5.place(x=0,y=0)

mainloop()
