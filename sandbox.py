from tkinter import *
from tkinter import ttk

root = Tk()
root.title('My Title')
root.geometry("500x400")

#Create a main frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)
# create a canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
#add a scroll bar to the canvas
my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)
#configure the canvas to have a scroll bar
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

#create another frame inside the canvas
second_frame = Frame(my_canvas)
#add the new frame to a window in the canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")


for thing in range(100):
    Button(second_frame, text=f'Button {thing} Yo').grid(row=thing, column=0)

root.mainloop()
