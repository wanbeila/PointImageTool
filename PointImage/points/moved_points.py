# Author:wanbeila
# -*- coding:utf-8 -*-
# @Time     : 
# @Author   :wanbeila
# @File     :moved_points.py
from tkinter import *

"""
自建一个能够移动的点类：
在指定位置生成点
获得鼠标事件，鼠标拖拽、鼠标右键等
显示点的标签
 ------
| 标签 |
 ------
|     |
 -----
关于鼠标的拖拽的实现，先以标签中的圆形为基础，以圆心坐标为基准，计算出当前的鼠标对于圆心的偏移量，通过偏移量再得到鼠标拖动时应当移动的横纵坐标的值
默认标签圆大小为2
"""


class MovingPoint(object):
    def __init__(self, canvas=None, label='0', radius=2, x_pos=0, y_pos=0, **kw):
        self.editable = False
        # 保存创建标签点的中心坐标，也即圆心坐标
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.canvas = canvas
        self.radius = radius
        if radius < 5:
            self.font_size = 10
        else:
            self.font_size = radius * 2 - 3
        self.label = 'No.' + label
        self.master = canvas

        # 需要保存的值
        self.save_x = 0.0
        self.save_y = 0.0

        # print(kw)
        if kw:
            self.raw_image_width = kw['raw_width']
            self.raw_image_height = kw['raw_height']
            self.double_image_width = kw['double_image_width']
            self.double_image_height = kw['double_image_height']

            self.save_x = self.x_pos * self.double_image_width / self.raw_image_width
            self.save_y = self.y_pos * self.double_image_height / self.raw_image_height

        # 使用此变量来及时保存鼠标当前的位置
        self.m_x_pos = 0
        self.m_y_pos = 0

        # 在canvas上半部分画出标签文字
        # 在canvas下半部分画出点
        self.canvas.create_text(self.x_pos, self.y_pos - (self.radius * 2), text=self.label, fill='green',
                                tag=self.label,
                                font='宋体 ' + str(self.font_size), justify=CENTER)
        self.canvas.create_oval(self.x_pos - self.radius, self.y_pos - self.radius,
                                self.x_pos + self.radius,
                                self.y_pos + self.radius, fill='green', tag=self.label)

        if self.canvas:
            self.canvas.tag_bind(self.label, '<B1-Motion>', self._on_mouse_drag)
            self.canvas.tag_bind(self.label, '<Enter>', self._on_mouse_enter)
            self.canvas.tag_bind(self.label, '<Leave>', self._on_mouse_leave)
            self.canvas.tag_bind(self.label, '<ButtonPress-1>', self._on_mouse_press)

    def _on_mouse_drag(self, event):
        # print(event)
        # 圆心应当移动的坐标值
        # x_togo = event.x - self.x_pos - self.x_offset
        # y_togo = event.y - self.y_pos - self.y_offset
        x_togo = event.x - self.x_pos
        y_togo = event.y - self.y_pos
        self.canvas.move(self.label, x_togo, y_togo)
        self.x_pos = x_togo + self.x_pos
        self.y_pos = y_togo + self.y_pos
        self.set_save_x_y()
        # print('pos: ', self.x_pos, self.y_pos)

    def _on_mouse_enter(self, event):
        self.canvas.config(
            cursor='hand2'
        )
        # self.canvas.unbind('<ButtonPress-1>')

    def _on_mouse_leave(self, event):
        # print('enter')
        self.canvas.config(
            cursor='arrow'
        )

    def _on_mouse_press(self, event):
        self.x_offset = event.x - self.x_pos
        self.y_offset = event.y - self.y_pos
        # print('offset: ', self.x_offset, self.y_offset)

    def set_save_x_y(self):
        self.save_x = self.x_pos * self.double_image_width / self.raw_image_width
        self.save_y = self.y_pos * self.double_image_height / self.raw_image_height

    def get_save_x_y(self):
        return str(self.save_x) + ' ' + str(self.save_y)
