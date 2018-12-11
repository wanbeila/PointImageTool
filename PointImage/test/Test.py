from points.moved_points import *

count = 0


# 为了解决这个bug，除了创建canvas之外，直接将canvas交给moved_points来管理
def mouse_pressed(event):
    global count
    # print(event.widget)
    if count >= 3:
        canvas.unbind('<ButtonPress-1>')
    mp = MovingPoint(canvas=canvas, label=str(count), radius=10, x_pos=event.x, y_pos=event.y)
    count = count + 1


window = Tk()
window.geometry('600x800')

test_frame = Frame(window, width=400, height=400, bg='black')
test_frame.place(x=100, y=100, anchor=CENTER)

canvas = Canvas(master=test_frame, width=400, height=400, bg='gray')
canvas.grid(row=0, column=0, sticky=NSEW)

canvas.bind('<ButtonPress-1>', mouse_pressed)

window.mainloop()
