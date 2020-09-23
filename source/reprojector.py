import os
import sys

from ctypes import c_int, CDLL, POINTER, WinDLL

from source.coordinates import Coordinates


class OSTN15Reprojector:
    def __init__(self, source_srid, target_srid, revision_source=0, revision_target=2015, datum=1, dll=None):
        self.source_srid = c_int(source_srid)
        self.source_revision = c_int(revision_source)
        self.target_srid = c_int(target_srid)
        self.target_revision = c_int(revision_target)
        self.datum = c_int(datum)

        if dll is None:
            grid_in_quest_lib = self.retrieve_dll()
        else:
            grid_in_quest_lib = dll
        self.convert_function = self.set_up_function(grid_in_quest_lib)

    @staticmethod
    def get_windows_dll(folder):
        path = os.path.join(folder, "GIQ.dll")
        return WinDLL(path)

    @staticmethod
    def get_linux_dll(folder):
        path = os.path.join(folder, "libgiq.so")
        return CDLL(path)

    @staticmethod
    def get_darwin_dll(folder):
        path = os.path.join(folder, "libGIQ.dylib")
        return CDLL(path)

    def retrieve_dll(self):
        lib_folder = os.path.split(os.path.realpath(__file__))[0]
        if sys.platform.startswith('win'):
            return self.get_windows_dll(lib_folder)
        elif sys.platform.startswith('linux'):
            return self.get_linux_dll(lib_folder)
        elif sys.platform.startswith('darwin'):
            return self.get_darwin_dll(lib_folder)

    @staticmethod
    def set_up_function(grid_in_quest_lib):
        convert_func = grid_in_quest_lib.ConvertCoordinates
        convert_func.argtypes = [c_int, c_int, c_int, c_int,
                                 POINTER(Coordinates),
                                 POINTER(Coordinates),
                                 POINTER(c_int)]
        convert_func.restype = bool
        return convert_func

    def convert(self, lon, lat, alt):
        source = Coordinates(lon, lat, alt)
        target = Coordinates(0, 0, 0)
        call_ok = self.convert_function(self.source_srid, self.target_srid,
                                        self.source_revision, self.target_revision,
                                        source, target,
                                        self.datum)
        if call_ok:
            return target.x, target.y, target.z
        else:
            raise Exception("call failed")