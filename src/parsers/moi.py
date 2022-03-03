from csv import DictReader
from datetime import datetime
from datetime import timedelta
from ..case import *
import re

vehicle_name2enum = {
    '公營公車-大客車': Vehicle.PUBLIC_CITY_BUS,
    '民營公車-大客車': Vehicle.PRIVATE_CITY_BUS,
    '公營客運-大客車': Vehicle.PUBLIC_HIGHWAY_BUS,
    '民營客運-大客車': Vehicle.PRIVATE_HIGHWAY_BUS,
    '遊覽車-大客車': Vehicle.TOUR_BUS,
    '自用大客車-大客車': Vehicle.PERSONAL_BUS,
    '營業用-大貨車': Vehicle.BUSINESS_HEAVY_TRUCK,
    '自用-大貨車': Vehicle.PERSONAL_HEAVY_TRUCK,
    '營業用-全聯結車': Vehicle.BUSINESS_FULL_TRAILER,
    '自用-全聯結車': Vehicle.PERSONAL_FULL_TRAILER,
    '營業用-半聯結車': Vehicle.BUSINESS_SEMI_TRAILER,
    '自用-半聯結車': Vehicle.PERSONAL_SEMI_TRAILER,
    '營業用-曳引車': Vehicle.BUSINESS_TRACTOR,
    '自用-曳引車': Vehicle.PERSONAL_TRACTOR,
    '計程車-小客車': Vehicle.TAXI,
    '租賃車-小客車': Vehicle.RENTAL_CAR,
    '自用-小客車': Vehicle.PERSONAL_CAR,
    '營業用-小貨車': Vehicle.BUSINESS_PICKUP_TRUCK,
    '營業用-小貨車(含客、貨兩用)': Vehicle.BUSINESS_PICKUP_TRUCK,
    '自用-小貨車': Vehicle.PERSONAL_PICKUP_TRUCK,
    '自用-小貨車(含客、貨兩用)': Vehicle.PERSONAL_PICKUP_TRUCK,
    '大型重型1(550C.C.以上)-機車': Vehicle.MOTORCYCLE_550_UP,
    '大型重型1-機車': Vehicle.MOTORCYCLE_550_UP,
    '大型重型2(250-550C.C.)-機車': Vehicle.MOTORCYCLE_250_TO_549,
    '大型重型2-機車': Vehicle.MOTORCYCLE_250_TO_549,
    '普通重型-機車': Vehicle.MOTORCYCLE_50_TO_249,
    # XXX: Is this a motorcycle or a special vehicle?
    '普通重型-特種車': Vehicle.MOTORCYCLE_50_TO_249,
    '普通輕型-機車': Vehicle.MOTORCYCLE_49_UNDER,
    '小型輕型-機車': Vehicle.MOTORCYCLE_45_KPH_UNDER,
    '大客車-軍車': Vehicle.MILITARY_BUS,
    '載重車-軍車': Vehicle.MILITARY_HEAVY_TRUCK,
    '小型車-軍車': Vehicle.MILITARY_CAR,
    '救護車-特種車': Vehicle.AMBULANCE,
    '消防車-特種車': Vehicle.FIRE_ENGINE,
    '警備車-特種車': Vehicle.POLICE_VEHICLE,
    '工程車-特種車': Vehicle.ENGINEERING_VEHICLE,
    '其他特種車-特種車': Vehicle.OTHER_SPECIAL_VEHICLE,
    '腳踏自行車-慢車': Vehicle.BICYCLE,
    '電動輔助自行車-慢車': Vehicle.PEDELEC,
    '電動自行車-慢車': Vehicle.PEDAL_FREE_PEDELEC,
    '人力車-慢車': Vehicle.RICKSHAW,
    '獸力車-慢車': Vehicle.ANIMAL_DRAWN_VEHICLE,
    '其他慢車-慢車': Vehicle.OTHER_SLOW_VEHICLE,
    '拼裝車-其他車': Vehicle.SELF_ASSEMBLED_VEHICLE,
    '農耕用車(或機械)-其他車': Vehicle.AGRICULTURAL_MACHINARY,
    '動力機械-其他車': Vehicle.POWER_MACHINE,
    '拖車(架)-其他車': Vehicle.TRAILER,
    '火車-其他車': Vehicle.TRAIN,
    '其他車-其他車': Vehicle.OTHER_VEHICLE,
    '行人-人': Vehicle.PEDESTRIAN,
    '乘客-人': Vehicle.PASSENGER,
    '其他人-人': Vehicle.OTEHR_PEOPLE,
    '': Vehicle.OTHER,
}


class MoiParser:

    def toAd(self, case_time: str) -> str:
        '''
        "106年08月06日 "
        "108年01月09日 17時11分70秒"
        "108年01月09日 17時11分13秒"
        "108年01月09日 17時11分"
        '''
        year, remainer = case_time.split('年')
        if not remainer.endswith('秒'):
            remainer += '00秒'
        return f'{int(year) + 1911}年{remainer}'

    def parse(self, csv_filename: str, severity: int) -> list[Case]:
        print(f'parsing {csv_filename}')
        cases = []
        with open(csv_filename) as f:
            reader = DictReader(f)
            for row in reader:
                try:
                    case = Case(
                        date=datetime.strptime(self.toAd(row['\ufeff發生時間']),
                                               '%Y年%m月%d日 %H時%M分%S秒'),
                        location=row['發生地點'],
                        severity=severity,
                        parties=[],
                    )
                    if '經度' in row:
                        case.gps = Gps(
                            float(row['經度']),
                            float(row['緯度']),
                        )
                    # verify severity
                    if '死亡受傷人數' in row:
                        match = re.match(r'死亡(\d+);受傷(\d+)', row['死亡受傷人數'])
                        if match is None:
                            raise ValueError(
                                f'The format of death/injury number is not correct: {row["死亡受傷人數"]}'
                            )
                        death = int(match.group(1))
                        injury = int(match.group(2))
                        if death and severity != 1 or death + injury and severity > 2:
                            raise ValueError(
                                'Severity in data does not match the argument.')
                    vehicles = row['車種'].split(';')
                    for i in range(len(vehicles)):
                        if vehicles[i] == '普通重型-特種車':
                            print(case)
                        case.parties.append(
                            Party(order=i + 1,
                                  vehicle=vehicle_name2enum[vehicles[i]]))
                    cases.append(case)
                except Exception as e:
                    print(e)
        return cases