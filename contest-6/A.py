import sys


class ExtendedList(list):

    def __init__(self, arr):
        super(ExtendedList, self).__init__(arr)

    def __getattr__(self, item):
        if item in ['reversed', 'R']:
            return self[::-1]
        if item in ['first', 'F']:
            return self[0]
        if item in ['last', 'L']:
            return self[-1]
        if item in ['size', 'S']:
            return len(self)
        raise AttributeError(f'{item} not in attribute')

    def __setattr__(self, key, value):
        if key in ['first', 'F']:
            self[0] = value
        elif key in ['last', 'L']:
            self[-1] = value
        elif key in ['size', 'S']:
            if value > len(self):
                self.extend([None for i in range(value - len(self))])
            else:
                del self[value:]
        else:
            raise AttributeError('f{key} not in attribute')

exec(sys.stdin.read())

