from ctypes import c_int, POINTER

from source.coordinates import Coordinates
from source.datum import Datum
from source.dll_retriever import DllRetriever
from source.srid import SRID


class OSTN15Reprojector:
    def __init__(self, source_srid: SRID, target_srid: SRID, giq_location,
                 revision_source=0, revision_target=2015, datum: Datum = Datum.NO_DATUM):
        self.source_srid = c_int(source_srid.value)
        self.target_srid = c_int(target_srid.value)
        self.source_revision = c_int(revision_source)
        self.target_revision = c_int(revision_target)
        self.datum = c_int(datum.value)

        grid_in_quest_lib = DllRetriever().retrieve_dll(giq_location)

        self.convert_function = self.set_up_function(grid_in_quest_lib)

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
