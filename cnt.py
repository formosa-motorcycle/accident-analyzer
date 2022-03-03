import csv
import os
import re
from collections import defaultdict
from typing import Pattern

result = defaultdict(lambda: defaultdict(int))

def parse_address(address):
    address = address.strip()
    address = address.replace(' ', '')

    '''
    臺南市下營區開化里區道南61線口 / 臺南市下營區省道臺19甲線
    高雄市小港區沿海二路山明783燈桿號前0.0公尺
    嘉義縣梅山鄉永興村台3線271.2公里
    彰化縣和美鎮地潭里彰新路6段182號前0.0公尺前
    新北市板橋區板城路85之1號前0.0公尺
    桃園市龍潭區上華里中正路上華段81號前0.0公尺附近
    桃園市平鎮區快速路一段P276梁柱處附近
    苗栗縣造橋鄉朝楊村台13甲線6.8公里與產業道路口
    苗栗縣通霄鎮國道3號152公里700.0公尺處南側向外側
    屏東縣枋山鄉台1線457公里500.0公尺處北側
    臺東縣長濱鄉台11線94公里800.0公尺處北側向路肩
    桃園市平鎮區國道1號65公里100.0公尺處北側向中線
    高雄市旗津區旗津三路/高雄市旗津區安樂巷
    新竹市香山區竹香北路221040桿
    臺南市新化區全興里竹子腳226之1號前
    高雄市大寮區188縣道/高雄市大寮區光明路2段
    苗栗縣後龍鎮埔頂里高鐵六路487巷8號旁
    彰化縣溪州鄉大庄村新生巷前0.0公尺
    臺南市東區崇興路上
    高雄市旗山區旗屏二路/高雄市旗山區高92鄉道
    嘉義縣水上鄉寬士村24鄰崎子頭167號前
    屏東縣長治鄉中興路578號長治國中前
    臺南市七股區台17線159公里100.0公尺處南側
    屏東縣九如鄉昌榮路慈玄宮前
    嘉義縣東石鄉掌潭村台61線266公里500公尺處南向車道。
    臺南市善化區國道3號347公里100.0公尺處南側向中線
    桃園市中壢區中正路2段43號前0.0公尺北側
    南投縣信義鄉台16線29公里西側向路肩
    嘉義縣朴子市永和里台82線橋下便道與161縣道路口
    嘉義縣竹崎鄉和平村台3線與166線路口
    桃園市龜山區東萬壽路18.5K處
    屏東縣里港鄉舊鐵道路、屏15線
    屏東縣滿州鄉縣200線12公里西側
    臺南市安定區嘉同里市道178線六塊寮18-6號前0.0公尺
    臺南市新市區環西路一段近南科南路口。
    雲林縣崙背鄉羅厝村156縣道東興40-1號
    臺南市安定區海寮里區道南132線海寮124-1號前0.0公尺
    南投縣名間鄉庄仔巷5-3號前
    桃園市大園區三石里7鄰63-8號前產業道路
    桃園市新屋區望間里望間路357巷路燈桿
    雲林縣虎尾鎮墾地里墾地3-27號前
    南投縣草屯鎮新豐里中正路與中正路1178巷口
    臺南市柳營區士林里仁愛路071號路燈旁
    高雄市大樹區三和路三和橋處號前0.0公尺
    嘉義市西區湖內里民生南路933附1號前0.0公尺
    屏東縣南州鄉萬華路段
    苗栗縣大湖鄉苗62線2.4公里處西向
    嘉義縣中埔鄉同仁村同仁32-1號(台3線292公里300公尺處)
    新北市林口區臺61線道路前0.0公尺
    新竹縣新豐鄉松柏林路坑子口105-20號前0.0公尺
    新竹縣關西鎮國道3號76公里500.0公尺處北側向輔助
    臺南市永康區永康里中山路南側/臺南市永康區永康里中山南路東側
    '''

    todo = [
        '高雄市大樹區三和路三和橋處號前0.0公尺',
        '桃園市大園區三石里7鄰63-8號前產業道路',
        '嘉義縣中埔鄉同仁村同仁32-1號(台3線292公里300公尺處)',
    ]
    if address in todo :
        return
    has_note = re.match(r'(\w*?)\((.+?)\)(\w*?)', address)
    note = None
    if has_note is not None:
        note = has_note.group(2)
        address = has_note.group(1) + has_note.group(3)
    pattern = r'(\w+?[市縣])?((\w+?鄉)(\w+?村(\d+鄰)?)?|(\w+?[鎮市區])(\w+?里(\d+鄰)?)?)?(((\w+?\d+[甲乙丙丁戊]?線|\w+?[路街]段?)(\w+?段)?|\w+?[縣鄉市]道|國道[1-9]號|安樂巷|竹子腳|新生巷|崎子頭|庄仔巷|墾地|同仁)(橋下便道)?)(路口|口|道路)?(\d+巷(\d+弄)?口?)?(((東興|海寮|六塊寮|坑子口)?(\d+\-\d+|\d+之\d+|\d+附\d+|\d+)號)|(\d+(\.\d+)?(公里|K)(\d+(\.\d+)?公尺)?處?)|(\w+?梁柱處?|\w+?\d+燈桿號|\d+桿))?(前?(\d+\.\d+公[里尺])?(前|附近|旁|上)?)?([東西南北](側向|側|向).*|長治國中前|慈玄宮前|近南科南路口。|路燈桿|路燈旁)?(.*)'
    
    match = re.match(pattern, address)
    if match is None:
        raise Exception(f'Invalid address: {address}')
    remain_index = len(match.groups())
    if match.group(remain_index):
        second_part = match.group(remain_index).strip()
        if not len(second_part): raise Exception(f'-----{address}---')
        if second_part[0] in '/與、':
            second_part = second_part[1:].strip()
        else:
            raise Exception(f'Invalid address: {address}')
        try:
            parse_address(second_part)
        except Exception as e:
            raise Exception(f'Invalid address: {address}')
    # match_again = re.match(pattern, match.group(3))
    # if match_again is not None and match_again.group(2) is not None:
    #     match = match_again
    # return {
    #     'county': match.group(1),
    #     'district': match.group(2),
    #     'road': match.group(3),
    # }


def count_intersection_accidents(filename, serious, store):
    with open(filename) as f:
        reader = csv.DictReader(f)
        for line in reader:
            location = line['發生地點']
            try:
                parse_address(location)
            except Exception as e:
                if re.search(r'[/和與]', location):
                    print(location)
            # if '/' in location:
            #     ways = location.split('/')
            # elif '與' in location:
            #     ways = location.split('與')
            # else:
            #     continue
            # ways = [parse_address(w) for w in ways]
            # if ways[0]['county'] is None:
            #     raise location
            # if ways[1]['county'] is None:
            #     ways[1]['county'] = ways[0]['county']
            # if ways[1]['district'] is None:
            #     ways[1]['district'] = ways[0]['district']
            # ways = [f'{w["county"]}{w["district"]}{w["road"]}' for w in ways]
            # if ways[0] == ways[1]:
            #     continue
            # ways.sort()
            # store['/'.join(ways)][serious] += 1

def export(year, store, keys):
    filename = f'{year}年度事故路口排名-{"".join(keys)}.csv'
    pairs = []
    for intersection, counts in store.items():
        total = sum(counts[k] for k in keys)
        pairs.append((total, intersection))
    pairs.sort(reverse=True)
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, ['路口'] + keys + ['總計'], extrasaction='ignore')
        writer.writeheader()
        for total, intersection in pairs:
            row = {
                '路口': intersection,
                '總計': total,
            }
            row = {**row, **store[intersection]}
            writer.writerow(row)



for filename in os.listdir('.'):
    if filename.startswith('109年度A'):
        count_intersection_accidents(filename, filename[5:7], result)

# export('109', result, ['A1', 'A2'])
# export('109', result, ['A1', 'A2', 'A3'])

