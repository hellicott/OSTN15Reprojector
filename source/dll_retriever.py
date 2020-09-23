import os
import sys
from ctypes import WinDLL, CDLL


class DllRetriever:
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