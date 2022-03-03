import json
import glob
import csv
from collections import defaultdict
from pprint import pprint
import re
from collections import Counter

result = defaultdict(Counter)
files_glob = '全國/109*A[123]*.csv'
location_filter = re.compile(r'^新北市')

vehicle_groups = {
    '大客車': [
        '公營公車-大客車',
        '公營客運-大客車',
        '民營公車-大客車',
        '民營客運-大客車',
        '遊覽車-大客車',
        '自用大客車-大客車',
    ],
    '大貨車': [
        '營業用-大貨車',
        '自用-大貨車',
        '營業用-全聯結車',
        '自用-全聯結車',
        '營業用-半聯結車',
        '自用-半聯結車',
        '營業用-曳引車',
        '自用-曳引車',
    ],
    '小客車': [
        '計程車-小客車',
        '租賃車-小客車',
        '自用-小客車',
    ],
    '小貨車': [
        '營業用-小貨車(含客、貨兩用)',
        '自用-小貨車(含客、貨兩用)',
    ],
    '機車': [
        '大型重型1(550C.C.以上)-機車',
        '大型重型2(250-550C.C.)-機車',
        '普通重型-機車',
        '普通輕型-機車',
        '小型輕型-機車',
    ],
    '自行車': [
        '電動自行車-慢車',
        '電動輔助自行車-慢車',
        '腳踏自行車-慢車',
    ],
    '行人': ['行人-人',],
    '其他車': [
        '小型車-軍車',
        '警備車-特種車',
        '消防車-特種車',
        '救護車-特種車',
        '其他特種車-特種車',
        '動力機械-其他車',
        '農耕用車(或機械)-其他車',
        '拖車(架)-其他車',
        '拼裝車-其他車',
        '其他車-其他車',
        '人力車-慢車',
        '其他慢車-慢車',
    ],
    '其他人': [
        '乘客-人',
        '其他人-人',
    ],
    '其他': ['無',],
}

vehicle_group_lookup = defaultdict(str)
for vehicle_group, vehicles in vehicle_groups.items():
    for vehicle in vehicles:
        vehicle_group_lookup[vehicle] = vehicle_group

for file in glob.glob(files_glob):
    reader = csv.DictReader(open(file))
    for line in reader:
        if location_filter.search(line['發生地點']) and line['\ufeff發生時間'] < '109年11月01日':
            vehicles = line['車種'].split(';')
            result[vehicles[0]][vehicles[1] if len(vehicles) > 1 else '無'] += 1

grouped_result = defaultdict(Counter)
for first, seconds in result.items():
    first_group = vehicle_group_lookup[first] or first
    grouped_seconds = grouped_result[first_group]
    for second, number in seconds.items():
        second_group = vehicle_group_lookup[second] or second
        grouped_seconds[second_group] += number

def print_result(r):
    for first in sorted(r):
        print(first)
        for second in sorted(r[first]):
            print(f'  {second}: {r[first][second]}')

print_result(result)
print_result(grouped_result)
