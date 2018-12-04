import os
from queue import Queue
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

"""
目前完成了，从指定的文件夹中读取图片，并且显示图片，在程序运行过程中对图片进行标点操作
每次需要标记4个点，保存到对应的图片文件的同路径下的同名txt文件中，txt文件包括有图片完整路径，点的横纵坐标
在程序运行过程中，每次完成标记的图片会从列表中软移除

之后需要完善：在程序运行时加载当前路径下的同名标记文件txt，并且将其中的点渲染到图片上显示
"""

# 当前选中的文件名
from Point import Point

SELECTED_FILE_NAME = ''
# 当前选中的文件夹名，也即保存txt文件路径
SELECTED_FOLDER = ''
# 当前选中的文件夹中的所有支持图像
CURRENT_IMAGE_LIST = []
# 当前显示的文件的索引，默认为-1，如果选中的为文件夹，则开始也为-1
CURRENT_IMAGE_INDEX = -1
# 选中的文件夹中所包含的所有文件数量
SELECTED_IMAGE_NUMBERS = 0
# 支持文件格式
FILE_TYPE = [('JPG', '.jpg'), ('JPEG', '.jpeg'), ('PNG', '.png')]
# 默认文件路径
DEFAULT_DIR = '/'
# 中部canvas
mid_canvas = None
# 中部布局绘制举行的canvas
rec_canvas = None
# 指示当前canvas中是否存在图片
CANVAS_HAS_IMAGE = False
# 指示标点按钮是否触发并完成任务
IS_POINT_EVENT_DONE = True
# 待保存的坐标点队列，4组坐标点
save_points = Queue(maxsize=4)
# 一张图片上的最大点数4
MAX_POINT_NUMBER_IN_IMAGE = 4
# 当前添加到图片上的点个数
CURRENT_POINT_NUMBER_IN_IMAGE = 0
# 指示是否已经执行了保存操作
HAS_SAVED = True
# 在定点画出圆形的半径大小
CIRCLE_RADIUS = 2
# 图片输入后，长宽的显示比例
DOUBLE_IMAGE_WIDTH = 1.0
DOUBLE_IMAGE_HEIGHT = 1.0
# 图像resize的最大宽度
MAX_RESIZE_WIDTH = 640
# 当前画布中的图像显示大小，用于清空画布
CURRENT_IMAGE_SIZE_IN_CANVAS = [MAX_RESIZE_WIDTH, -1]
# 是否按住了CTRL键
IS_CTRL_PRESSED = False
# 图像缩放指数
IMAGE_RESIZE_RATIO = 10


# 关于图像的自适应缩放(本程序将以宽为优先级更高的条件，根据初始化的程序主窗口的canvas的宽为800/10 * 8=640)
# 因此将以640作为图像的初显示宽度，如果图像本身过小则不予处理
# 可以指定重置大小的宽度
def auto_resize_image(image, **kw):
    global DOUBLE_IMAGE_WIDTH, DOUBLE_IMAGE_HEIGHT, CURRENT_IMAGE_SIZE_IN_CANVAS
    # 首先获得图像的原始长宽比例
    raw_width, raw_height = image.width, image.height
    print(kw)
    if kw:
        # 此时判断为手动缩放操作
        resize_width = kw['width']
    else:
        resize_width = MAX_RESIZE_WIDTH

    # 此时判断为初始输入的操作
    if raw_width <= resize_width:
        CURRENT_IMAGE_SIZE_IN_CANVAS = [raw_width, raw_height]
        return image
    else:
        re_width = resize_width
        raw_ratio = raw_height / raw_width
        # 根据原始比例得到新的长
        re_height = int(resize_width * raw_ratio)
        re_image = image.resize((re_width, re_height))
        DOUBLE_IMAGE_WIDTH = raw_width / resize_width
        DOUBLE_IMAGE_HEIGHT = raw_height / re_height
        CURRENT_IMAGE_SIZE_IN_CANVAS[0] = re_width
        CURRENT_IMAGE_SIZE_IN_CANVAS[1] = re_height
        return re_image


# 判断条件，如果当前已经在图像上标过点且未执行保存操作则弹出对话框
def check_save():
    global SELECTED_IMAGE_NUMBERS, CURRENT_IMAGE_INDEX, CURRENT_POINT_NUMBER_IN_IMAGE, HAS_SAVED
    if CURRENT_POINT_NUMBER_IN_IMAGE > 0 and not HAS_SAVED:
        # 如果当前有没有保存的任务
        need_save = messagebox.askyesno('tip', message='是否保存当前图片的点集？')
        if need_save:
            return _on_save()
        HAS_SAVED = True
    return True


# 在图片切换后，需要进行重置的参数
def reset_params():
    global CURRENT_POINT_NUMBER_IN_IMAGE, \
        save_points, \
        DOUBLE_IMAGE_WIDTH, \
        DOUBLE_IMAGE_HEIGHT, mid_canvas, CURRENT_IMAGE_SIZE_IN_CANVAS
    CURRENT_POINT_NUMBER_IN_IMAGE = 0
    DOUBLE_IMAGE_HEIGHT = 1.0
    DOUBLE_IMAGE_WIDTH = 1.0
    mid_canvas.delete('all')
    save_points.queue.clear()


# 切换下一张图片
def _next_image():
    global CURRENT_IMAGE_INDEX
    if check_save():
        if CURRENT_IMAGE_INDEX < SELECTED_IMAGE_NUMBERS:
            CURRENT_IMAGE_INDEX = CURRENT_IMAGE_INDEX + 1
        reset_params()
        show_image_in_canvas()


def _former_image():
    global CURRENT_IMAGE_INDEX
    if check_save():
        if CURRENT_IMAGE_INDEX > 0:
            CURRENT_IMAGE_INDEX = CURRENT_IMAGE_INDEX - 1
        reset_params()
        show_image_in_canvas()


def resize_image(image):
    global DOUBLE_IMAGE_WIDTH, DOUBLE_IMAGE_HEIGHT
    DOUBLE_IMAGE_WIDTH = image.width / 400
    DOUBLE_IMAGE_HEIGHT = image.height / 400
    print(image.width, image.height, DOUBLE_IMAGE_HEIGHT, DOUBLE_IMAGE_WIDTH)
    n_image = image.resize((400, 400))
    return n_image


def show_image_in_canvas(**kw):
    global SELECTED_IMAGE_NUMBERS, SELECTED_FILE_NAME, CURRENT_IMAGE_INDEX, CURRENT_IMAGE_LIST
    global mid_canvas
    if len(CURRENT_IMAGE_LIST) > 0:
        # 如果能够显示的图片列表不为空
        SELECTED_FILE_NAME = CURRENT_IMAGE_LIST[CURRENT_IMAGE_INDEX]
        if SELECTED_FILE_NAME is not '':
            # if CANVAS_HAS_IMAGE:
            #     mid_canvas.clearRect()
            img = Image.open(SELECTED_FILE_NAME)
            # img = resize_image(img)
            img = auto_resize_image(img, **kw)
            image = ImageTk.PhotoImage(img)
            img_width = image.width()
            img_height = image.height()
            if isinstance(mid_canvas, Canvas):
                mid_canvas.create_image(img_width / 2, img_height / 2, image=image, tag='image')
                mid_canvas.config(
                    scrollregion=(0, 0, img_width, img_height)
                )
                # mid_canvas.create_line((0, 0, 100, 200))
            CURRENT_IMAGE_LIST.append(image)
            print('当前显示%d张图片，共有%d张' % (CURRENT_IMAGE_INDEX + 1, SELECTED_IMAGE_NUMBERS))


# 选中文件，并且使用canvas画出图片
def _select_file():
    global SELECTED_IMAGE_NUMBERS, SELECTED_FILE_NAME, CURRENT_IMAGE_INDEX, CURRENT_IMAGE_LIST
    filename = filedialog.askopenfilename(title='选择文件',
                                          initialdir=(os.path.expanduser(DEFAULT_DIR)),
                                          filetypes=FILE_TYPE)
    SELECTED_FILE_NAME = filename
    CURRENT_IMAGE_INDEX = 0
    SELECTED_IMAGE_NUMBERS = SELECTED_IMAGE_NUMBERS + 1
    CURRENT_IMAGE_LIST.insert(0, SELECTED_FILE_NAME)
    show_image_in_canvas()


# 遍历文件夹
# bug：过多文件，list会无响应
def list_image_from_folder(folder):
    global SELECTED_IMAGE_NUMBERS, SELECTED_FILE_NAME, CURRENT_IMAGE_INDEX, CURRENT_IMAGE_LIST
    # 如果遇到文件，进行判断，如果是图像则将图像存到列表中,并结束递归
    if os.path.exists(folder):
        if os.path.isfile(folder):
            tail = folder[folder.rfind('.'):len(folder)].lower()
            # print(tail)
            if tail.find('.jpg') != -1 or tail.find('.png') != -1 or tail.find('.bmp') != -1:
                CURRENT_IMAGE_LIST.append(folder)
                SELECTED_IMAGE_NUMBERS = SELECTED_IMAGE_NUMBERS + 1
            return
        elif os.path.isdir(folder):
            dirs = os.listdir(folder)
            for dir in dirs:
                list_image_from_folder(os.path.join(folder, dir))


# 选中文件夹
def _select_folder():
    global SELECTED_IMAGE_NUMBERS, SELECTED_FILE_NAME, CURRENT_IMAGE_INDEX, CURRENT_IMAGE_LIST, SELECTED_FOLDER
    folder_name = filedialog.askdirectory(title='选择文件夹',
                                          initialdir=(os.path.expanduser(DEFAULT_DIR)))
    print(folder_name)
    SELECTED_FOLDER = folder_name
    list_image_from_folder(folder_name)
    if SELECTED_IMAGE_NUMBERS > 0:
        CURRENT_IMAGE_INDEX = 0
    show_image_in_canvas()
    print(len(CURRENT_IMAGE_LIST))


# 退出工具
def _quit(main_window):
    main_window.quit()
    main_window.destroy()
    exit()


# 创建菜单栏
def generate_menu(main_window):
    # 菜单栏
    main_menu_bar = Menu(main_window)
    main_window.config(menu=main_menu_bar)

    file_menu = Menu(main_menu_bar, tearoff=0)
    about_menu = Menu(main_menu_bar, tearoff=0)
    main_menu_bar.add_cascade(label='文件', menu=file_menu)
    main_menu_bar.add_cascade(label='关于', menu=about_menu)
    # 在文件选项下生成点击命令
    # file_menu.add_command(label='选择文件', command=lambda: _select_file())
    file_menu.add_command(label='选择文件夹', command=lambda: _select_folder())
    file_menu.add_separator()
    file_menu.add_command(label='退出', command=lambda: _quit(main_window))

    about_menu.add_command(label='关于我')

    return file_menu


# ========================start=======生成坐标点
# 1.当前是否已经点击了point按钮
# 2.当前坐标是否在图片允许范围内（400,400）
def generate_point_txt_file(x_pos, y_pos):
    global save_points, CURRENT_POINT_NUMBER_IN_IMAGE, \
        HAS_SAVED, mid_canvas, \
        CIRCLE_RADIUS, IS_POINT_EVENT_DONE, DOUBLE_IMAGE_WIDTH, DOUBLE_IMAGE_HEIGHT
    if CURRENT_POINT_NUMBER_IN_IMAGE >= 4:
        messagebox.showinfo(title='tip', message='当前图中已经包含了四个点')
        return
    else:
        HAS_SAVED = False
        c_x_start = x_pos - CIRCLE_RADIUS
        c_y_start = y_pos - CIRCLE_RADIUS
        c_x_end = x_pos + CIRCLE_RADIUS
        c_y_end = y_pos + CIRCLE_RADIUS
        mid_canvas.create_oval(c_x_start, c_y_start, c_x_end, c_y_end, fill='green')
        save_points.put(Point(x_pos * DOUBLE_IMAGE_WIDTH, y_pos * DOUBLE_IMAGE_HEIGHT))
        CURRENT_POINT_NUMBER_IN_IMAGE = CURRENT_POINT_NUMBER_IN_IMAGE + 1
        if CURRENT_POINT_NUMBER_IN_IMAGE == 4:
            IS_POINT_EVENT_DONE = True


# 保存当前的点集
def _on_save():
    global save_points, \
        CURRENT_POINT_NUMBER_IN_IMAGE, \
        HAS_SAVED, SELECTED_FILE_NAME, \
        CURRENT_IMAGE_INDEX, \
        SELECTED_IMAGE_NUMBERS, \
        CURRENT_IMAGE_LIST, mid_canvas
    if HAS_SAVED:
        pass
    elif CURRENT_POINT_NUMBER_IN_IMAGE != 4:
        messagebox.showinfo('tip', message='还没选好4组点')
        return False
    elif CURRENT_POINT_NUMBER_IN_IMAGE == 4:
        txt_filename = SELECTED_FILE_NAME[0:SELECTED_FILE_NAME.rfind('.')] + '.txt'
        fp = open(txt_filename, 'w')
        fp.write(SELECTED_FILE_NAME)
        fp.write(' ')
        while not save_points.empty():
            point = save_points.get()
            fp.write(str(point))
            fp.write(' ')
        print(txt_filename)
        fp.close()
        # 当本张图完成标点操作，则从列表中移除
        del CURRENT_IMAGE_LIST[CURRENT_IMAGE_INDEX]
        SELECTED_IMAGE_NUMBERS = SELECTED_IMAGE_NUMBERS - 1
        mid_canvas.delete('all')
        show_image_in_canvas()
        # 重置为0
        CURRENT_POINT_NUMBER_IN_IMAGE = 0
    return True


# 在触发了标点按钮后再在图上点击时进行标点
def _on_mouse_click_in_canvas(event):
    global IS_POINT_EVENT_DONE, CURRENT_POINT_NUMBER_IN_IMAGE
    x_pos, y_pos = event.x, event.y
    if IS_POINT_EVENT_DONE is not True:
        if 0 <= x_pos <= 400 and 0 <= y_pos <= 400:
            generate_point_txt_file(x_pos, y_pos)


# ========================end=======生成坐标点文件

def draw_rec():
    global IS_POINT_EVENT_DONE
    IS_POINT_EVENT_DONE = not IS_POINT_EVENT_DONE
    print(IS_POINT_EVENT_DONE)


# 鼠标在canvas中移动的事件回调，配置鼠标的指针样式
def _on_mouse_move_in_canvas(event):
    global mid_canvas
    x_pos, y_pos = event.x, event.y
    if IS_POINT_EVENT_DONE is not True:
        mid_canvas.config(
            cursor='circle'
        )
    else:
        mid_canvas.config(
            cursor='arrow'
        )
    # print('moving in canvas (%d,%d)' % (x_pos, y_pos))


def generate_left_button(left_frame):
    """
    左侧按钮设置
    """
    # 按钮1
    '''
    Grid.columnconfigure(left_frame, 0, weight=1)
    Grid.rowconfigure(left_frame, 0, weight=1)
    top_btn = Button(left_frame, text='选择文件', command=lambda: _select_file())
    top_image = PhotoImage(file='/test/button/icon/file.png')
    top_btn.config(image=top_image, compound=TOP)
    top_btn.image = top_image
    top_btn.grid(row=0, column=0, sticky=NSEW, padx=1, pady=1)
    '''

    # 按钮2
    Grid.columnconfigure(left_frame, 0, weight=1)
    Grid.rowconfigure(left_frame, 1, weight=1)
    dire_btn = Button(left_frame, text='选择文件夹', command=lambda: _select_folder())
    dire_image = PhotoImage(file='button/icon/folder.png')
    dire_btn.config(image=dire_image, compound=TOP)
    dire_btn.image = dire_image
    dire_btn.grid(row=1, column=0, sticky=NSEW, padx=1, pady=1)

    # 按钮3
    Grid.columnconfigure(left_frame, 0, weight=1)
    Grid.rowconfigure(left_frame, 2, weight=1)
    next_btn = Button(left_frame, text='下一张', command=lambda: _next_image())
    next_image = PhotoImage(file='button/icon/next.png')
    next_btn.config(image=next_image, compound=TOP)
    next_btn.image = next_image
    next_btn.grid(row=2, column=0, sticky=NSEW, padx=1, pady=1)

    # 按钮4
    Grid.columnconfigure(left_frame, 0, weight=1)
    Grid.rowconfigure(left_frame, 3, weight=1)
    former_btn = Button(left_frame, text='上一张', command=lambda: _former_image())
    former_image = PhotoImage(file='button/icon/rewind.png')
    former_btn.config(image=former_image, compound=TOP)
    former_btn.image = former_image
    former_btn.grid(row=3, column=0, sticky=NSEW, padx=1, pady=1)

    # 按钮5
    Grid.columnconfigure(left_frame, 0, weight=1)
    Grid.rowconfigure(left_frame, 4, weight=1)
    point_btn = Button(left_frame, text='生成点', command=draw_rec)
    point_image = PhotoImage(file='button/icon/dot.png')
    point_btn.config(image=point_image, compound=TOP)
    point_btn.image = point_image
    point_btn.grid(row=4, column=0, sticky=NSEW, padx=1, pady=1)

    # 按钮6
    Grid.columnconfigure(left_frame, 0, weight=1)
    Grid.rowconfigure(left_frame, 5, weight=1)
    save_btn = Button(left_frame, text='保存', command=_on_save)
    save_image = PhotoImage(file='button/icon/save.png')
    save_btn.config(image=save_image, compound=TOP)
    save_btn.image = save_image
    save_btn.grid(row=5, column=0, sticky=NSEW, padx=1, pady=1)


# 处理鼠标滚轮事件，使能中间的canvas的滚动效果绑定鼠标
# 同时实现图片在canvas中的缩放
def mousewheel_proceed(event):
    global mid_canvas, IS_CTRL_PRESSED, CURRENT_IMAGE_SIZE_IN_CANVAS, IMAGE_RESIZE_RATIO
    # print(event.char)
    if IS_CTRL_PRESSED:
        # 当前按住ctrl键，滚动鼠标滚轮，进行图片缩放
        if event.delta > 0:
            # 滚轮向上
            kw_width = {'width': CURRENT_IMAGE_SIZE_IN_CANVAS[0] + IMAGE_RESIZE_RATIO}
            mid_canvas.delete('all')
            show_image_in_canvas(**kw_width)
        else:
            # 向下
            if CURRENT_IMAGE_SIZE_IN_CANVAS[0] - IMAGE_RESIZE_RATIO <= 640:
                re_re_width = 640
            else:
                re_re_width = CURRENT_IMAGE_SIZE_IN_CANVAS[0] - IMAGE_RESIZE_RATIO
            kw_width = {'width': re_re_width}
            mid_canvas.delete('all')
            show_image_in_canvas(**kw_width)

    else:
        if event.delta > 0:
            # 滚轮向上
            mid_canvas.yview_scroll(-1, 'units')
        else:
            # 向下
            mid_canvas.yview_scroll(1, 'units')


def _on_control_l_key_press(event):
    global IS_CTRL_PRESSED
    IS_CTRL_PRESSED = True
    # print(event)


def _on_control_l_key_release(event):
    global IS_CTRL_PRESSED
    IS_CTRL_PRESSED = False
    # print(event)


def generate_mid_canvas(mid_frame):
    # 在中间布局添加canvas
    global mid_canvas
    if mid_canvas is None:
        # 为canvas添加x轴滚动条
        x_scrollbar = Scrollbar(mid_frame, orient=HORIZONTAL)
        x_scrollbar.grid(row=1, column=0, sticky=EW)
        # 为canvas添加y轴滚动条
        y_scrollbar = Scrollbar(mid_frame)
        y_scrollbar.grid(row=0, column=1, sticky=NS)
        mid_canvas = Canvas(
            mid_frame,
            xscrollcommand=x_scrollbar.set,
            yscrollcommand=y_scrollbar.set,
            bd=0,
        )
        Grid.rowconfigure(mid_frame, 0, weight=1)
        Grid.columnconfigure(mid_frame, 0, weight=10)
        mid_canvas.grid(row=0, column=0, sticky=N + S + E + W, padx=1, pady=1)
        x_scrollbar.config(command=mid_canvas.xview)
        y_scrollbar.config(command=mid_canvas.yview)
        mid_canvas.bind('<MouseWheel>', mousewheel_proceed)
        mid_canvas.bind('<Motion>', _on_mouse_move_in_canvas)
        mid_canvas.bind('<Button-1>', _on_mouse_click_in_canvas)


def main():
    # 主窗口
    main_window = Tk()
    main_window.title('特征点标记工具')
    main_window.geometry('800x600')
    main_window.minsize(160, 120)

    main_window.bind('<KeyPress-Control_L>', _on_control_l_key_press)
    main_window.bind('<KeyRelease-Control_L>', _on_control_l_key_release)

    # 生成菜单栏
    generate_menu(main_window)

    # 配置frame自适应窗口大小
    Grid.columnconfigure(main_window, 0, weight=1)
    Grid.rowconfigure(main_window, 0, weight=1)
    Grid.columnconfigure(main_window, 1, weight=8)
    Grid.rowconfigure(main_window, 0, weight=1)
    Grid.columnconfigure(main_window, 2, weight=1)
    Grid.rowconfigure(main_window, 0, weight=1)

    # 声明三个布局 |口|
    left_frame = Frame(master=main_window, bg='gray')
    left_frame.grid(row=0, column=0, sticky=N + S + E + W)

    mid_frame = Frame(master=main_window, bg='white')
    mid_frame.grid(row=0, column=1, sticky=N + S + E + W)

    right_frame = Frame(master=main_window, bg='black')
    right_frame.grid(row=0, column=2, sticky=N + S + E + W)

    # 按照布局生成界面
    generate_left_button(left_frame)
    generate_mid_canvas(mid_frame)

    # img = Image.open(os.path.join(os.path.curdir, 'test.jpg'))
    # image = ImageTk.PhotoImage(image=img)
    #
    # canvas.create_image(300, 400, image=image)

    main_window.mainloop()


if __name__ == '__main__':
    main()
