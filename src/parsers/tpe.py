from ..case import *

from csv import DictReader
import pickle
from pprint import pprint


def get_pickle_path(year: int) -> str:
    return f'tpe-{year}.pickle'


def parse_csv(filename: str, year: int):
    cases = {}
    with open(filename) as f:
        reader = DictReader(f)
        for row in reader:
            if row['非交通事故'] == '1' or row['性別'] == '3': # 性別 == 3: 物或動物
                continue
            try:
                case_type = int(row['15事故類型及型態'] or 0)
                case = Case(
                    id=row['案號'],
                    date=datetime.strptime(
                        f'{int(row["發生年"]) + 1911}/{row["發生月"]}/{row["發生日"]} {row["發生時"].zfill(2)}:{row["發生分"].zfill(2)}',
                        '%Y/%m/%d %H:%M'),
                    location=row['肇事地點'],
                    severity=int(row['處理別']),
                    is_self=case_type >= 18 and case_type <= 29,
                    parties=[],
                )
                # field should only omit for A4
                party = Party(
                    order=int(row['當事人序']),
                    gender=int(row['性別'] or 5),
                    age=int(row['年齡'] or -1),
                    injury_severity=int(row['22受傷程度'] or 6),
                    vehicle=Vehicle(row['車種']),
                    cause=int(row['肇因碼-個別'] or 0)
                )
                # if row['年齡'] == '0' and row['處理別'] != '4' and row['35個人肇逃否'] != '2' and row['肇逃'] != '1' and row['未依規定處置'] != '1' and party.vehicle != Vehicle.PASSENGER and not row['肇因研判O'].startswith('當事人未到案說明'):
                #     raise ValueError(row)
                # if party.cause == 0 and row['處理別'] != '4' and row['35個人肇逃否'] != '2' and row['肇逃'] != '1' and row['未依規定處置'] != '1'  and not row['肇因研判O'].startswith('當事人未到案說明'):
                #     raise ValueError(row)
            except ValueError as e:
                pprint(e.args)
                raise ValueError(row)
            if case.id in cases:
                if not cases[case.id].is_same_unsafe(case):
                    raise Exception(f'{case} {cases[case.id]} not the same')
                cases[case.id].parties.append(party)
            else:
                case.parties.append(party)
                cases[case.id] = case
    # with open(get_pickle_path(year), 'wb') as f:
    #     pickle.dump(list(cases.values()), f)
    return list(cases.values())

def parse_public_csv(filename: str, year: int):
    cases = {}
    with open(filename) as f:
        reader = DictReader(f)
        for row in reader:
            if row['性別'] == '3': # 性別 == 3: 物或動物
                continue
            try:
                date = datetime.strptime(
                        f'{int(row["發生年"]) + 1911}/{row["發生月"]}/{row["發生日"]} {row["發生時"].zfill(2)}:{row["發生分"].zfill(2)}',
                        '%Y/%m/%d %H:%M')
                location=row['肇事地點']
                id=f'{date.strftime("%Y%m%d_%H%M")}-{location}'
                case = Case(
                    id=id,
                    date=date,
                    location=location,
                    severity=int(row['處理別']),
                    parties=[],
                )
                party = Party(
                    order=int(row['當事人序']),
                    gender=int(row['性別'] or 5),
                    age=int(row['年齡'] or -1),
                    injury_severity=int(row['受傷程度'] or 6),
                    vehicle=Vehicle(row['車種']),
                    # data before 2019, included, doesn't have personal cause
                    cause=int(row.get('肇因碼-個別', 0) or 0)
                )
            except ValueError as e:
                pprint(e.args)
                raise ValueError(row)
            if case.id in cases:
                if not cases[case.id].is_same_unsafe(case):
                    raise Exception(f'{case} {cases[case.id]} not the same')
                cases[case.id].parties.append(party)
            else:
                case.parties.append(party)
                cases[case.id] = case
    # with open(get_pickle_path(year), 'wb') as f:
    #     pickle.dump(list(cases.values()), f)
    return list(cases.values())

# parse_csv('台北市/新增資料夾 (5)/109.csv', 2020)
