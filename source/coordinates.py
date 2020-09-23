from ctypes import c_double, Structure


class Coordinates(Structure):
    _fields_ = [("x", c_double),
                ("y", c_double),
                ("z", c_double)]
