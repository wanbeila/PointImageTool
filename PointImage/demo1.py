from tkinter import *
root = Tk()
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
frame=Frame(root)
frame.grid(row=0, column=0, sticky=N+S+E+W)
i=1
for row_index in range(2):
    Grid.rowconfigure(frame, row_index, weight=1)
    for col_index in range(2):
        Grid.columnconfigure(frame, col_index, weight=1)
        btn = Button(frame,text="%s"%(i))
        btn.grid(row=row_index, column=col_index, sticky=N+S+E+W,padx=2,pady=2)
        i=i+1
root.mainloop()
