from enum import Enum


class SRID(Enum):
    ETRS89_CARTESIAN = 4936
    ETRS89_GEODETIC = 4937
    ETRS89_ZONE_29 = 25829
    ETRS89_ZONE_30 = 25830
    ETRS89_ZONE_31 = 25831
    OSGB36_BNG = 27700
    IRISH_TRANSVERSE_MERCATOR = 2157
    IRISH_GRID = 29903