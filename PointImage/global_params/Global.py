"""
用于存放所有的全局变量
"""
from queue import Queue

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
# 中部label
mid_label = None
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
# 当前图片的原始大小
CURRENT_IMAGE_IN_CANVAS_RAW_WIDTH = 0
CURRENT_IMAGE_IN_CANVAS_RAW_HEIGHT = 0
# 右侧布局的listbox用于显示文件名称
file_listbox = None
# 需要将要显示的图片展示在外面，也就是将canvas即将绘制的图片放在与main_loop同一作用域下面
# 局部的image会被gc回收
image_to_show = None
save_moving_points = Queue(4)
