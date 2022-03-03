from dataclasses import asdict, dataclass, InitVar
from datetime import datetime
from enum import Enum, IntEnum, unique, auto
from copy import copy

# cause_tb = {
# '01': '違規超車',
#  '02': '爭(搶)道行駛',
#  '03': '蛇行、方向不定',
#  '04': '逆向行駛',
#  '05': '未靠右行駛',
#  '06': '未依規定讓車',
#  '07': '變換車道或方向不當',
#  '08': '左轉彎未依規定',
#  '09': '右轉彎未依規定',
#  '10': '迴轉未依規定',
#  '11': '橫越道路不慎',
#  '12': '倒車未依規定',
#  '13': '超速失控',
#  '14': '未依規定減速',
#  '15': '搶越行人穿越道',
# '16': '未保持行車安全距離',
#  '17': '未保持行車安全間隔',
#  '18': '停車操作時，未注意其他車(人)安全',
# '19': '起步未注意其他車(人)安全',
#  '20': '吸食違禁物後駕駛失控',
#  '21': '酒醉(後)駕駛失控',
#  '22': '疲勞(患病)駕駛失控',
#  '23': '未注意車前狀態',
#  '24': '搶(闖)越平交道',
#  '25': '違反號誌管制或指揮',
#  '26': '違反特定標誌(線)禁制',
#  '27': '未依規定使用燈光',
#  '28': '暗處停車無燈光、標識',
#  '29': '夜間行駛無燈光設備',
#  '30': '裝載貨物不穩妥',
#  '31': '載貨超重而失控',
#  '32': '超載人員而失控',
#  '33': '貨物超長、寬、高而肇事',
#  '34': '裝卸貨不當',
#  '35': '裝載未盡安全措施',
#  '36': '未待乘客安全上下開車',
#  '37': '其他裝載不當肇事',
#  '38': '違規停車或暫停不當而肇事',
#  '39': '拋錨未採安全措施',
#  '40': '開啟車門不當而肇事',
#  '41': '使用手持行動電話失控',
#  '42': '其他引起事故之違規或不當行為',
# '43': '不明原因肇事',
#  '44': '尚未發現肇事因素',
#  '45': '煞車失靈',
#  '46': '方向操縱系統故障',
#  '47': '燈光系統故障',
#  '48': '車輪脫落或輪胎爆裂',
#  '49': '車輛零件脫落',
# '50': '其他引起事故之故障',
# '51': '未依規定行走行人穿越道、地下道、天橋而穿越道路',
# '52': '未依標誌、標線、號誌或手勢指揮穿越道路',
# '53': '穿越道路未注意左右來車',
#  '54': '在道路上嬉戲或奔走不定',
#  '55': '未待車輛停妥而上下車',
#  '56': '上下車輛未注意安全',
#  '57': '頭手伸出車外而肇事',
#  '58': '乘坐不當而跌落',
#  '59': '在路上工作未設適當標識',
#  '60': '其他引起事故之疏失或行為',
#  '61': '路況危險無安全（警告）設施',
#  '62': '交通管制設施失靈或損毀',
#  '63': '交通指揮不當',
#  '64': '平交道看守疏失或未放柵欄',
#  '65': '其他交通管制不當',
#   '66': '動物竄出',
# '67': '尚未發現肇事因素',
# '':'空白',
# }


@unique
class Weather(IntEnum):
    STROM = 1
    STRONG_WIND = 2
    SAND_WIND = 3
    SMOKE = 4
    SNOWE = 5
    RAIN = 6
    CLOUDY = 7
    SUNNY = 8


@unique
class Light(IntEnum):
    DAYTIME = 1
    SUNRISE_SUNSET = 2
    NIGHT_LIGHTING = 3
    NIGHT_DARK = 4


@unique
class RoadHierarchy(IntEnum):
    FREEWAY = 1
    PROVINCIAL = 2
    COUNTY = 3
    COUNTRY = 4
    CITY = 5
    VILLAGE = 6
    EXCLUDED = 7
    OTHER = 8


@unique
class VehicleCategory(IntEnum):
    BUS = auto()
    HEAVY_TRUCK = auto()
    CAR = auto()
    PICKUP_TRUCK = auto()
    MOTORCYCLE = auto()
    BICYCLE = auto()
    PEDESTRIAN = auto()
    OTHER_VEHICLE = auto()
    OTHER_PEOPLE = auto()
    OTHER = auto()

    def __str__(self):
        vehicle_category_name_lookup = {
            VehicleCategory.BUS: '大客車',
            VehicleCategory.HEAVY_TRUCK: '大貨車',
            VehicleCategory.CAR: '小客車',
            VehicleCategory.PICKUP_TRUCK: '小貨車',
            VehicleCategory.MOTORCYCLE: '機車',
            VehicleCategory.BICYCLE: '自行車',
            VehicleCategory.PEDESTRIAN: '行人',
            VehicleCategory.OTHER_VEHICLE: '其他車',
            VehicleCategory.OTHER_PEOPLE: '其他人',
            VehicleCategory.OTHER: '其他',
        }
        return vehicle_category_name_lookup[self.value]


@unique
class Vehicle(Enum):
    PUBLIC_CITY_BUS = 'A01'
    PRIVATE_CITY_BUS = 'A02'
    PUBLIC_HIGHWAY_BUS = 'A03'
    PRIVATE_HIGHWAY_BUS = 'A04'
    TOUR_BUS = 'A05'
    PERSONAL_BUS = 'A06'
    BUSINESS_HEAVY_TRUCK = 'A11'
    PERSONAL_HEAVY_TRUCK = 'A12'
    BUSINESS_FULL_TRAILER = 'A21'
    PERSONAL_FULL_TRAILER = 'A22'
    BUSINESS_SEMI_TRAILER = 'A31'
    PERSONAL_SEMI_TRAILER = 'A32'
    BUSINESS_TRACTOR = 'A41'
    PERSONAL_TRACTOR = 'A42'
    TAXI = 'B01'
    RENTAL_CAR = 'B02'
    PERSONAL_CAR = 'B03'
    BUSINESS_PICKUP_TRUCK = 'B11'
    PERSONAL_PICKUP_TRUCK = 'B12'
    MOTORCYCLE_550_UP = 'C01'
    MOTORCYCLE_250_TO_549 = 'C02'
    MOTORCYCLE_50_TO_249 = 'C03'
    MOTORCYCLE_49_UNDER = 'C04'
    MOTORCYCLE_45_KPH_UNDER = 'C05'
    MILITARY_BUS = 'D01'
    MILITARY_HEAVY_TRUCK = 'D02'
    MILITARY_CAR = 'D03'
    AMBULANCE = 'E01'
    FIRE_ENGINE = 'E02'
    POLICE_VEHICLE = 'E03'
    ENGINEERING_VEHICLE = 'E04'
    OTHER_SPECIAL_VEHICLE = 'E05'
    BICYCLE = 'F01'
    PEDELEC = 'F02'
    PEDAL_FREE_PEDELEC = 'F03'
    RICKSHAW = 'F04'
    ANIMAL_DRAWN_VEHICLE = 'F05'
    OTHER_SLOW_VEHICLE = 'F06'
    SELF_ASSEMBLED_VEHICLE = 'G01'
    AGRICULTURAL_MACHINARY = 'G02'
    POWER_MACHINE = 'G03'
    TRAILER = 'G04'
    TRAIN = 'G05'
    OTHER_VEHICLE = 'G06'
    PEDESTRIAN = 'H01'
    PASSENGER = 'H02'
    OTEHR_PEOPLE = 'H03'
    OTHER = ''

    # def __str__(self):
    #     return ''

    @property
    def category(self) -> VehicleCategory:
        vehicle_category_lookup = {
            Vehicle.PUBLIC_CITY_BUS: VehicleCategory.BUS,
            Vehicle.PRIVATE_CITY_BUS: VehicleCategory.BUS,
            Vehicle.PUBLIC_HIGHWAY_BUS: VehicleCategory.BUS,
            Vehicle.PRIVATE_HIGHWAY_BUS: VehicleCategory.BUS,
            Vehicle.TOUR_BUS: VehicleCategory.BUS,
            Vehicle.PERSONAL_BUS: VehicleCategory.BUS,
            Vehicle.BUSINESS_HEAVY_TRUCK: VehicleCategory.HEAVY_TRUCK,
            Vehicle.PERSONAL_HEAVY_TRUCK: VehicleCategory.HEAVY_TRUCK,
            Vehicle.BUSINESS_FULL_TRAILER: VehicleCategory.HEAVY_TRUCK,
            Vehicle.PERSONAL_FULL_TRAILER: VehicleCategory.HEAVY_TRUCK,
            Vehicle.BUSINESS_SEMI_TRAILER: VehicleCategory.HEAVY_TRUCK,
            Vehicle.PERSONAL_SEMI_TRAILER: VehicleCategory.HEAVY_TRUCK,
            Vehicle.BUSINESS_TRACTOR: VehicleCategory.HEAVY_TRUCK,
            Vehicle.PERSONAL_TRACTOR: VehicleCategory.HEAVY_TRUCK,
            Vehicle.TAXI: VehicleCategory.CAR,
            Vehicle.RENTAL_CAR: VehicleCategory.CAR,
            Vehicle.PERSONAL_CAR: VehicleCategory.CAR,
            Vehicle.BUSINESS_PICKUP_TRUCK: VehicleCategory.PICKUP_TRUCK,
            Vehicle.PERSONAL_PICKUP_TRUCK: VehicleCategory.PICKUP_TRUCK,
            Vehicle.MOTORCYCLE_550_UP: VehicleCategory.MOTORCYCLE,
            Vehicle.MOTORCYCLE_250_TO_549: VehicleCategory.MOTORCYCLE,
            Vehicle.MOTORCYCLE_50_TO_249: VehicleCategory.MOTORCYCLE,
            Vehicle.MOTORCYCLE_49_UNDER: VehicleCategory.MOTORCYCLE,
            Vehicle.MOTORCYCLE_45_KPH_UNDER: VehicleCategory.MOTORCYCLE,
            Vehicle.MILITARY_BUS: VehicleCategory.OTHER_VEHICLE,
            Vehicle.MILITARY_HEAVY_TRUCK: VehicleCategory.OTHER_VEHICLE,
            Vehicle.MILITARY_CAR: VehicleCategory.OTHER_VEHICLE,
            Vehicle.AMBULANCE: VehicleCategory.OTHER_VEHICLE,
            Vehicle.FIRE_ENGINE: VehicleCategory.OTHER_VEHICLE,
            Vehicle.POLICE_VEHICLE: VehicleCategory.OTHER_VEHICLE,
            Vehicle.ENGINEERING_VEHICLE: VehicleCategory.OTHER_VEHICLE,
            Vehicle.OTHER_SPECIAL_VEHICLE: VehicleCategory.OTHER_VEHICLE,
            Vehicle.BICYCLE: VehicleCategory.BICYCLE,
            Vehicle.PEDELEC: VehicleCategory.BICYCLE,
            Vehicle.PEDAL_FREE_PEDELEC: VehicleCategory.BICYCLE,
            Vehicle.RICKSHAW: VehicleCategory.OTHER_VEHICLE,
            Vehicle.ANIMAL_DRAWN_VEHICLE: VehicleCategory.OTHER_VEHICLE,
            Vehicle.OTHER_SLOW_VEHICLE: VehicleCategory.OTHER_VEHICLE,
            Vehicle.SELF_ASSEMBLED_VEHICLE: VehicleCategory.OTHER_VEHICLE,
            Vehicle.AGRICULTURAL_MACHINARY: VehicleCategory.OTHER_VEHICLE,
            Vehicle.POWER_MACHINE: VehicleCategory.OTHER_VEHICLE,
            Vehicle.TRAILER: VehicleCategory.OTHER_VEHICLE,
            Vehicle.TRAIN: VehicleCategory.OTHER_VEHICLE,
            Vehicle.OTHER_VEHICLE: VehicleCategory.OTHER_VEHICLE,
            Vehicle.PEDESTRIAN: VehicleCategory.PEDESTRIAN,
            Vehicle.PASSENGER: VehicleCategory.OTHER_PEOPLE,
            Vehicle.OTEHR_PEOPLE: VehicleCategory.OTHER_PEOPLE,
            Vehicle.OTHER: VehicleCategory.OTHER
        }
        return vehicle_category_lookup[self]


@dataclass
class Gps:
    lng: float
    lat: float


@dataclass
class Party:
    vehicle: Vehicle
    order: int | None = None
    gender: int | None = None
    age: int | None = None
    injury_severity: int | None = None
    cause: int | None = None


@dataclass(slots=True)
class Case:
    """Class for indicate an accident case"""
    date: datetime
    location: str
    severity: int
    # death: int
    # injury: int
    # weather: Weather
    # light: Light
    # road_hierarchy: RoadHierarchy
    # speed_limit: int
    # road_geometry: int
    # lane: int
    # road_surface: int
    parties: list[Party]
    id: str | None = None
    gps: Gps | None = None

    def is_same(self, other: 'Case'):
        excluded_fields = set(['parties'])
        fields = self.__dataclass_fields__.keys()
        return all(
            getattr(self, f) == getattr(other, f)
            for f in fields
            if f not in excluded_fields)

    def is_same_unsafe(self, other: 'Case'):
        tmp_self_parties = []
        tmp_other_parties = []
        [tmp_self_parties, self.parties] = [self.parties, tmp_self_parties]
        [tmp_other_parties, other.parties] = [other.parties, tmp_other_parties]
        result = self == other
        [tmp_self_parties, self.parties] = [self.parties, tmp_self_parties]
        [tmp_other_parties, other.parties] = [other.parties, tmp_other_parties]
        return result





if __name__ == '__main__':
    c = Case('', datetime(1990, 1, 1), '', 1, [])
    c2 = Case('', datetime(1990, 1, 1), '', 1, ['123'])
    import timeit

    # For Python>=3.5 one can also write:
    print(timeit.timeit("c.is_same(c2)", globals=locals(), number = 100000))
    print(timeit.timeit("c.is_same_unsafe(c2)", globals=locals(), number = 100000))