from collections import defaultdict, Counter
from csv import DictReader, DictWriter
from pprint import pprint
import json
from pathlib import Path

data = defaultdict(lambda: {'A': '0', 'p': []})
all_type = set()

# people_tb = {
#     'A01': '公營公車',
#     'A01': '民營公車',
#     'A01': '公營客運',
#     'A01': '民營客運',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
#     'A01': 'A01',
# }

cause_tb = {
'01': '違規超車',
 '02': '爭(搶)道行駛',
 '03': '蛇行、方向不定',
 '04': '逆向行駛',
 '05': '未靠右行駛',
 '06': '未依規定讓車',
 '07': '變換車道或方向不當',
 '08': '左轉彎未依規定',
 '09': '右轉彎未依規定',
 '10': '迴轉未依規定',
 '11': '橫越道路不慎',
 '12': '倒車未依規定',
 '13': '超速失控',
 '14': '未依規定減速',
 '15': '搶越行人穿越道',
'16': '未保持行車安全距離',
 '17': '未保持行車安全間隔',
 '18': '停車操作時，未注意其他車(人)安全',
'19': '起步未注意其他車(人)安全',
 '20': '吸食違禁物後駕駛失控',
 '21': '酒醉(後)駕駛失控',
 '22': '疲勞(患病)駕駛失控',
 '23': '未注意車前狀態',
 '24': '搶(闖)越平交道',
 '25': '違反號誌管制或指揮',
 '26': '違反特定標誌(線)禁制',
 '27': '未依規定使用燈光',
 '28': '暗處停車無燈光、標識',
 '29': '夜間行駛無燈光設備',
 '30': '裝載貨物不穩妥',
 '31': '載貨超重而失控',
 '32': '超載人員而失控',
 '33': '貨物超長、寬、高而肇事',
 '34': '裝卸貨不當',
 '35': '裝載未盡安全措施',
 '36': '未待乘客安全上下開車',
 '37': '其他裝載不當肇事',
 '38': '違規停車或暫停不當而肇事',
 '39': '拋錨未採安全措施',
 '40': '開啟車門不當而肇事',
 '41': '使用手持行動電話失控',
 '42': '其他引起事故之違規或不當行為',
'43': '不明原因肇事',
 '44': '尚未發現肇事因素',
 '45': '煞車失靈',
 '46': '方向操縱系統故障',
 '47': '燈光系統故障',
 '48': '車輪脫落或輪胎爆裂',
 '49': '車輛零件脫落',
'50': '其他引起事故之故障',
'51': '未依規定行走行人穿越道、地下道、天橋而穿越道路',
'52': '未依標誌、標線、號誌或手勢指揮穿越道路', 
'53': '穿越道路未注意左右來車',
 '54': '在道路上嬉戲或奔走不定',
 '55': '未待車輛停妥而上下車',
 '56': '上下車輛未注意安全',
 '57': '頭手伸出車外而肇事',
 '58': '乘坐不當而跌落',
 '59': '在路上工作未設適當標識',
 '60': '其他引起事故之疏失或行為',
 '61': '路況危險無安全（警告）設施',
 '62': '交通管制設施失靈或損毀',
 '63': '交通指揮不當',
 '64': '平交道看守疏失或未放柵欄',
 '65': '其他交通管制不當',
  '66': '動物竄出',
'67': '尚未發現肇事因素',
'':'空白',
}

people_type = {
    'A01': '大客車',
    'A02': '大客車',
    'A03': '大客車',
    'A04': '大客車',
    'A05': '大客車',
    'A06': '大客車',
    'A11': '大貨車',
    'A12': '大貨車',
    'A21': '大貨車',
    'A22': '大貨車',
    'A31': '大貨車',
    'A32': '大貨車',
    'A41': '大貨車',
    'A42': '大貨車',
    'B01': '小客車',
    'B02': '小客車',
    'B03': '小客車',
    'B11': '小貨車',
    'B12': '小貨車',
    'C01': '機車',
    'C02': '機車',
    'C03': '機車',
    'C04': '機車',
    'C05': '機車',
    # 'D01': '大客車',
    # 'D02': '大貨車',
    # 'D03': '小客車',
    'D01': '軍車',
    'D02': '軍車',
    'D03': '軍車',
    'E01': '特種車',
    'E02': '特種車',
    'E03': '特種車',
    'E04': '特種車',
    'E05': '特種車',
    'F01': '慢車',
    'F02': '慢車',
    'F03': '慢車',
    'F04': '慢車',
    'F05': '慢車',
    'F06': '慢車',
    'G01': '其他車',
    'G02': '其他車',
    'G03': '其他車',
    'G04': '其他車',
    'G05': '其他車',
    'G06': '其他車',
    'H01': '行人',
    'H02': '乘客',
    'H03': '其他人',
    '': '',
}


filtered_data = {}
main_counter = Counter()
maker_counter = Counter()
year = '109'
filename_tb = {
    'bike': '機車',
    'car': '汽車',
}
# input_file = f'{year}-l-g.csv'
input_file = f'{year}.csv'
filtered_filename = f'filtered_data-{year}-l-g.json'


def calc_data():
    with open(input_file) as f:
        reader = DictReader(f)
        for row in reader:
            all_type.add(row['處理別'])
            cur = data[row['案號']]
            cur['A'] = row['處理別']
            cur['p'].append(row)
    pprint(all_type)

    for c, v in data.items():
        if v['A'] not in ['1', '2', '3']:
            continue
        ps = v['p']
        # if '行人' not in [people_type[p['車種']] for p in ps]:
        # if '機車' not in [people_type[p['車種']] for p in ps]:
        #     continue
        is_target = False
        for p in ps:
            if '安康' in p['肇事地點'] and '康寧' in p['肇事地點']:
                is_target = True
                break
        if not is_target:
            continue
        main_cause = set(p['肇因碼-主要'] for p in ps)
        if len(main_cause) != 1:
            print(f'{c} 主肇因不只一項: {str(main_cause)}')
        v['main'] = main_cause.pop()
        main_counter[v['main']] += 1
        for p in ps:
            if p['當事人序'] == '1':
                v['maker'] = people_type[p['車種']]
                maker_counter[v['maker']] += 1
        if 'maker' not in v:
            v['maker'] = '空白'
            print(f'沒有主肇事者:{p["案號"]}')
        filtered_data[c] = v
    json.dump(filtered_data, open(filtered_filename, 'w'), indent=2, ensure_ascii=False)


def analyze(cases, print_detail = False):

    print('總數')
    total = len(cases)
    pprint(total)

    print('主要肇因')
    main_counter = Counter(v['main'] for v in cases)
    main_counter = dict((cause_tb[c],v) for c, v in main_counter.items())
    pprint(sorted(main_counter.items(), key=lambda x:x[1], reverse=True))

    print('主要肇事者')
    maker_counter = Counter(v['maker'] for v in cases)
    pprint(maker_counter)
    
    if print_detail:
        cause_counters = defaultdict(Counter)
        for case in cases:
            for person in case['p']:
                cause_counter = cause_counters[people_type[person['車種']]] 
                cause_counter[person['肇因碼-個別']] += 1
        for car_type, cause_counter in cause_counters.items(): 
            cause_counter = dict((cause_tb[c],v) for c, v in cause_counter.items())
            print(car_type)
            pprint(sorted(cause_counter.items(), key=lambda x:x[1], reverse=True))
    print()

def main(data):
    car_distributed = defaultdict(list)
    for case in data:
        car_distributed[case['maker']].append(case)

    print('全部')
    analyze(data, True)

    for car_type, cases in car_distributed.items():
        print(car_type)
        analyze(cases, True)



# if not Path(filtered_filename).is_file():
#     calc_data()
# else:
#     filtered_data = json.load(open(filtered_filename))
#     # main_counter = Counter(v['main'] for v in filtered_data.values())
#     # maker_counter = Counter(v['maker'] for v in filtered_data.values())
#     # cause_counter = Counter(p['肇因碼-個別'] for v in filtered_data.values() for p in v['p'] if people_type[p['車種']] == '機車')

filtered_data_108 = json.load(open(f'filtered_data-108-l-g.json'))
filtered_data_109 = json.load(open(f'filtered_data-109-l-g.json'))

filtered_data = list(filtered_data_108.values()) + list(filtered_data_109.values())


# main(filtered_data.values())
main(filtered_data)
