class Point(object):
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_kv_pos(self):
        return self.x_pos, self.y_pos

    def __str__(self):
        return str(self.x_pos) + ' ' + str(self.y_pos)


