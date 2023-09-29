from app import VeryImportantClass, decorator
import numbers


class HackedClass(VeryImportantClass):
    def __init__(self):
        super(HackedClass, self).__init__()
        cls = VeryImportantClass
        for attr in cls.__dict__:
            if attr[0] == '_':
                continue
            elif callable(getattr(cls, attr)):
                setattr(type(self), attr, decorator(getattr(cls, attr)))
            elif isinstance(getattr(cls, attr), numbers.Number):
                setattr(type(self), attr, 2 * getattr(cls, attr))
            elif '__contains__' in type(getattr(cls, attr)).__dict__:
                setattr(type(self), attr, type(getattr(cls, attr))())
