from collections import defaultdict
import secrets
import numpy as np
from src.parsers.moi import MoiParser
from src.parsers.tpe import parse_csv
from src.parsers.tpe import parse_public_csv
from src.case import *
from glob import glob
import pickle
import re
from pathlib import Path
from pprint import pprint

'''
Importing matplotlib takes too much time, so comment out it by defaut.
'''
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
# import matplotlib.colors as colors
# import matplotlib

# import json
# import matplotlib.font_manager as fm
# import mplcairo


def load_national_data(year: int) -> list[Case]:
    pickle_path = f'./outputs/pickles/nation-{year}.pickle'
    if Path(pickle_path).is_file():
        with open(pickle_path, 'rb') as f:
            print(f'loading {pickle_path}')
            return pickle.load(f)
    moi_parser = MoiParser()
    cases = []
    for csv_filename in glob(f'data/全國/{year - 1911}*.csv'):
        match = re.search(r'(\d+)年度A(\d).*交通事故資料', csv_filename)
        if match is None:
            print(f'wrong filename: {csv_filename}')
            continue
        severity = int(match.group(2))
        cases += moi_parser.parse(csv_filename, severity)
    if cases:
        with open(pickle_path, 'wb') as f:
            pickle.dump(cases, f)
    return cases


def load_all_national_data() -> dict[int, list[Case]]:
    all_years_cases = {}
    for year in range(2013, 2021):
        all_years_cases[year] = load_national_data(year)
    return all_years_cases


def load_tpe_data(year: int) -> list[Case]:
    pickle_path = f'./outputs/pickles/tpe-{year}.pickle'
    if Path(pickle_path).is_file():
        with open(pickle_path, 'rb') as f:
            print(f'loading {pickle_path}')
            return pickle.load(f)
    # moi_parser = MoiParser()
    filename_with_full_data = f'./data/台北市/新增資料夾 (5)/{year - 1911}.csv'
    print(f'start to parse {year}')
    if Path(filename_with_full_data).is_file():
        cases = parse_csv(filename_with_full_data, year)
    else:
        cases = parse_public_csv(f'./data/台北市/{year - 1911}.csv', year)
    if cases:
        with open(pickle_path, 'wb') as f:
            pickle.dump(cases, f)
    return cases

def load_all_tpe_data() -> dict[int, list[Case]]:
    all_years_cases = {}
    for year in range(2012, 2022):
        all_years_cases[year] = load_tpe_data(year)
    return all_years_cases


@dataclass
class InvoleStatistics:
    total: int = 0
    motorcycle_case: int = 0
    cars_case: int = 0
    four_wheels_case: int = 0

    def add_case(self, case: Case):
        self.total += 1
        self.motorcycle_case += any(
            party.vehicle.category == VehicleCategory.MOTORCYCLE
            for party in case.parties)
        self.cars_case += any(
            party.vehicle.category in (VehicleCategory.CAR,
                                       VehicleCategory.PICKUP_TRUCK)
            for party in case.parties)
        self.four_wheels_case += any(
            party.vehicle.category in (VehicleCategory.BUS,
                                       VehicleCategory.HEAVY_TRUCK,
                                       VehicleCategory.CAR,
                                       VehicleCategory.PICKUP_TRUCK)
            for party in case.parties)

    def print_percentages(self):
        if not self.total:
            print('no cases')
            return
        print(f'motorcycle case: {self.motorcycle_case / self.total * 100}%')
        print(f'car case: {self.cars_case / self.total * 100}%')
        print(f'four wheels case: {self.four_wheels_case / self.total * 100}%')


def print_percentages_from_national():
    death_and_injury = InvoleStatistics()
    no_injury = InvoleStatistics()

    # for year, cases in load_all_national_data().items():
    for year, cases in {2020: load_national_data(2020)}.items():
        print(f'adding {year}')
        count = 0
        for case in cases:
            if case.severity <= 2:
                death_and_injury.add_case(case)
            else:
                no_injury.add_case(case)
            count += 1
            if count % 1000 == 0:
                print(f'{count} cases added')

    pprint(death_and_injury)
    death_and_injury.print_percentages()
    pprint(no_injury)
    no_injury.print_percentages()


a1a2_first_and_second = {
    VehicleCategory.MOTORCYCLE: {
        VehicleCategory.MOTORCYCLE: 650622,
        VehicleCategory.CAR: 340099,
        VehicleCategory.OTHER: 194375,
        VehicleCategory.BICYCLE: 36373,
        VehicleCategory.OTHER_VEHICLE: 3257,
        VehicleCategory.PEDESTRIAN: 45614,
        VehicleCategory.HEAVY_TRUCK: 9834,
        VehicleCategory.BUS: 6461,
        VehicleCategory.PICKUP_TRUCK: 57693,
        VehicleCategory.OTHER_PEOPLE: 22562,
    },
    VehicleCategory.CAR: {
        VehicleCategory.CAR: 66511,
        VehicleCategory.MOTORCYCLE: 666266,
        VehicleCategory.PICKUP_TRUCK: 10967,
        VehicleCategory.OTHER: 18806,
        VehicleCategory.OTHER_PEOPLE: 7618,
        VehicleCategory.OTHER_VEHICLE: 1403,
        VehicleCategory.BICYCLE: 24373,
        VehicleCategory.PEDESTRIAN: 38117,
        VehicleCategory.BUS: 1353,
        VehicleCategory.HEAVY_TRUCK: 3350,
    },
    VehicleCategory.BICYCLE: {
        VehicleCategory.CAR: 16140,
        VehicleCategory.MOTORCYCLE: 35927,
        VehicleCategory.OTHER: 11193,
        VehicleCategory.OTHER_PEOPLE: 639,
        VehicleCategory.PICKUP_TRUCK: 3113,
        VehicleCategory.PEDESTRIAN: 1820,
        VehicleCategory.BUS: 431,
        VehicleCategory.BICYCLE: 2401,
        VehicleCategory.HEAVY_TRUCK: 577,
        VehicleCategory.OTHER_VEHICLE: 102,
    },
    VehicleCategory.PEDESTRIAN: {
        VehicleCategory.CAR: 5661,
        VehicleCategory.MOTORCYCLE: 22334,
        VehicleCategory.OTHER: 1684,
        VehicleCategory.PEDESTRIAN: 42,
        VehicleCategory.PICKUP_TRUCK: 1064,
        VehicleCategory.HEAVY_TRUCK: 171,
        VehicleCategory.BICYCLE: 460,
        VehicleCategory.BUS: 260,
        VehicleCategory.OTHER_VEHICLE: 60,
        VehicleCategory.OTHER_PEOPLE: 4,
    },
    VehicleCategory.PICKUP_TRUCK: {
        VehicleCategory.MOTORCYCLE: 118763,
        VehicleCategory.PEDESTRIAN: 7298,
        VehicleCategory.HEAVY_TRUCK: 1283,
        VehicleCategory.CAR: 12412,
        VehicleCategory.PICKUP_TRUCK: 4685,
        VehicleCategory.OTHER: 4529,
        VehicleCategory.BICYCLE: 4785,
        VehicleCategory.OTHER_VEHICLE: 336,
        VehicleCategory.BUS: 327,
        VehicleCategory.OTHER_PEOPLE: 1661,
    },
    VehicleCategory.OTHER_VEHICLE: {
        VehicleCategory.MOTORCYCLE: 6166,
        VehicleCategory.PICKUP_TRUCK: 244,
        VehicleCategory.BICYCLE: 219,
        VehicleCategory.PEDESTRIAN: 392,
        VehicleCategory.OTHER: 599,
        VehicleCategory.OTHER_VEHICLE: 94,
        VehicleCategory.CAR: 921,
        VehicleCategory.HEAVY_TRUCK: 88,
        VehicleCategory.OTHER_PEOPLE: 139,
        VehicleCategory.BUS: 38,
    },
    VehicleCategory.OTHER_PEOPLE: {
        VehicleCategory.CAR: 335,
        VehicleCategory.MOTORCYCLE: 1369,
        VehicleCategory.OTHER: 61,
        VehicleCategory.PICKUP_TRUCK: 48,
        VehicleCategory.BICYCLE: 64,
        VehicleCategory.HEAVY_TRUCK: 18,
        VehicleCategory.BUS: 43,
        VehicleCategory.OTHER_VEHICLE: 5,
        VehicleCategory.OTHER_PEOPLE: 7,
    },
    VehicleCategory.HEAVY_TRUCK: {
        VehicleCategory.MOTORCYCLE: 18106,
        VehicleCategory.CAR: 4555,
        VehicleCategory.HEAVY_TRUCK: 1360,
        VehicleCategory.PEDESTRIAN: 825,
        VehicleCategory.OTHER_VEHICLE: 133,
        VehicleCategory.OTHER: 1476,
        VehicleCategory.BICYCLE: 989,
        VehicleCategory.PICKUP_TRUCK: 1658,
        VehicleCategory.BUS: 135,
        VehicleCategory.OTHER_PEOPLE: 342,
    },
    VehicleCategory.BUS: {
        VehicleCategory.CAR: 1290,
        VehicleCategory.MOTORCYCLE: 6889,
        VehicleCategory.PEDESTRIAN: 1219,
        VehicleCategory.PICKUP_TRUCK: 284,
        VehicleCategory.BICYCLE: 573,
        VehicleCategory.BUS: 204,
        VehicleCategory.OTHER_PEOPLE: 1713,
        VehicleCategory.HEAVY_TRUCK: 125,
        VehicleCategory.OTHER: 65,
        VehicleCategory.OTHER_VEHICLE: 45,
    },
    VehicleCategory.OTHER: {
        VehicleCategory.OTHER: 5,
    },
}
a1a2a3_2020_first_and_second = {
    VehicleCategory.CAR: {
        VehicleCategory.MOTORCYCLE: 108228,
        VehicleCategory.BUS: 1743,
        VehicleCategory.CAR: 105464,
        VehicleCategory.OTHER: 12871,
        VehicleCategory.PICKUP_TRUCK: 12577,
        VehicleCategory.BICYCLE: 4147,
        VehicleCategory.HEAVY_TRUCK: 3479,
        VehicleCategory.OTHER_PEOPLE: 1318,
        VehicleCategory.PEDESTRIAN: 5510,
        VehicleCategory.OTHER_VEHICLE: 448,
    },
    VehicleCategory.MOTORCYCLE: {
        VehicleCategory.OTHER_PEOPLE: 3664,
        VehicleCategory.CAR: 64399,
        VehicleCategory.MOTORCYCLE: 109474,
        VehicleCategory.OTHER: 29238,
        VehicleCategory.PEDESTRIAN: 6064,
        VehicleCategory.PICKUP_TRUCK: 8830,
        VehicleCategory.HEAVY_TRUCK: 1467,
        VehicleCategory.BUS: 995,
        VehicleCategory.BICYCLE: 5313,
        VehicleCategory.OTHER_VEHICLE: 414,
    },
    VehicleCategory.PEDESTRIAN: {
        VehicleCategory.MOTORCYCLE: 3231,
        VehicleCategory.BICYCLE: 91,
        VehicleCategory.BUS: 37,
        VehicleCategory.CAR: 892,
        VehicleCategory.OTHER: 178,
        VehicleCategory.PICKUP_TRUCK: 134,
        VehicleCategory.HEAVY_TRUCK: 33,
        VehicleCategory.PEDESTRIAN: 4,
        VehicleCategory.OTHER_VEHICLE: 10,
    },
    VehicleCategory.PICKUP_TRUCK: {
        VehicleCategory.CAR: 19544,
        VehicleCategory.MOTORCYCLE: 17375,
        VehicleCategory.PICKUP_TRUCK: 4821,
        VehicleCategory.PEDESTRIAN: 883,
        VehicleCategory.OTHER: 2460,
        VehicleCategory.BICYCLE: 667,
        VehicleCategory.HEAVY_TRUCK: 930,
        VehicleCategory.OTHER_PEOPLE: 305,
        VehicleCategory.OTHER_VEHICLE: 97,
        VehicleCategory.BUS: 375,
    },
    VehicleCategory.BUS: {
        VehicleCategory.CAR: 2159,
        VehicleCategory.PICKUP_TRUCK: 306,
        VehicleCategory.MOTORCYCLE: 930,
        VehicleCategory.OTHER: 184,
        VehicleCategory.BUS: 134,
        VehicleCategory.PEDESTRIAN: 138,
        VehicleCategory.BICYCLE: 82,
        VehicleCategory.OTHER_PEOPLE: 423,
        VehicleCategory.HEAVY_TRUCK: 78,
        VehicleCategory.OTHER_VEHICLE: 22,
    },
    VehicleCategory.OTHER_PEOPLE: {
        VehicleCategory.MOTORCYCLE: 208,
        VehicleCategory.CAR: 156,
        VehicleCategory.BICYCLE: 12,
        VehicleCategory.PICKUP_TRUCK: 17,
        VehicleCategory.OTHER_PEOPLE: 3,
        VehicleCategory.OTHER: 22,
        VehicleCategory.BUS: 12,
        VehicleCategory.HEAVY_TRUCK: 2,
    },
    VehicleCategory.HEAVY_TRUCK: {
        VehicleCategory.OTHER: 1724,
        VehicleCategory.CAR: 7912,
        VehicleCategory.MOTORCYCLE: 2865,
        VehicleCategory.PICKUP_TRUCK: 1317,
        VehicleCategory.PEDESTRIAN: 130,
        VehicleCategory.OTHER_PEOPLE: 120,
        VehicleCategory.HEAVY_TRUCK: 1136,
        VehicleCategory.BICYCLE: 159,
        VehicleCategory.BUS: 140,
        VehicleCategory.OTHER_VEHICLE: 100,
    },
    VehicleCategory.BICYCLE: {
        VehicleCategory.BICYCLE: 415,
        VehicleCategory.MOTORCYCLE: 6251,
        VehicleCategory.HEAVY_TRUCK: 98,
        VehicleCategory.CAR: 3613,
        VehicleCategory.OTHER: 1999,
        VehicleCategory.BUS: 63,
        VehicleCategory.PEDESTRIAN: 323,
        VehicleCategory.PICKUP_TRUCK: 526,
        VehicleCategory.OTHER_PEOPLE: 93,
        VehicleCategory.OTHER_VEHICLE: 20,
    },
    VehicleCategory.OTHER_VEHICLE: {
        VehicleCategory.OTHER_VEHICLE: 16,
        VehicleCategory.PICKUP_TRUCK: 93,
        VehicleCategory.MOTORCYCLE: 689,
        VehicleCategory.HEAVY_TRUCK: 43,
        VehicleCategory.CAR: 628,
        VehicleCategory.OTHER: 126,
        VehicleCategory.PEDESTRIAN: 27,
        VehicleCategory.BUS: 22,
        VehicleCategory.BICYCLE: 18,
        VehicleCategory.OTHER_PEOPLE: 27,
    },
    VehicleCategory.OTHER: {
        VehicleCategory.OTHER: 89,
        VehicleCategory.CAR: 221,
        VehicleCategory.MOTORCYCLE: 120,
        VehicleCategory.BUS: 10,
        VehicleCategory.PICKUP_TRUCK: 21,
        VehicleCategory.OTHER_VEHICLE: 1,
        VehicleCategory.OTHER_PEOPLE: 1,
    },
}


def print_first_and_second(first_and_second: dict[VehicleCategory,
                                                  dict[VehicleCategory, int]]):
    print('{')
    for first in first_and_second:
        print(f'    VehicleCategory.{first.name}:{{')
        for second in first_and_second[first]:
            print(
                f'        VehicleCategory.{second.name}: {first_and_second[first][second]},'
            )
        print('    },')
    print('}')


def stat_first_and_second(
        cases: list[Case]) -> dict[VehicleCategory, dict[VehicleCategory, int]]:
    first_and_second = defaultdict(lambda: defaultdict(int))
    for case in cases:
        if len(case.parties) >= 2:
            first = case.parties[0].vehicle.category
            second = case.parties[1].vehicle.category
            first_and_second[first][second] += 1
        elif len(case.parties) == 1:
            first = case.parties[0].vehicle.category
            second = VehicleCategory.OTHER
            first_and_second[first][second] += 1
    print_first_and_second(first_and_second)
    return first_and_second


def draw_vehicle_diagram():
    tpe_cases = load_tpe_data(2020)
    national_cases = load_all_national_data()
    # Taipei's A3 date is not contained in the national data
    a1a2a3_2020_cases = national_cases[2020] + [
        c for c in tpe_cases if c.severity == 3
    ]
    # only data of 2020 contains A3 cases
    national_cases[2020] = [c for c in national_cases[2020] if c.severity <= 2]
    a1a2_cases = sum(national_cases.values(), [])
    _draw_vehicle_diagram('A1、A2（2013-2020）', 'A1A2-2013_2020.png',
                          stat_first_and_second(a1a2_cases))
    _draw_vehicle_diagram('A1、A2、A3（2020）', 'A1A2A3-2020.png',
                          stat_first_and_second(a1a2a3_2020_cases))


def draw_vehicle_diagram_with_cache():
    _draw_vehicle_diagram('A1、A2（2013-2020）', 'A1A2-2013_2020.png',
                          a1a2_first_and_second)
    _draw_vehicle_diagram('A1、A2、A3（2020）', 'A1A2A3-2020.png',
                          a1a2a3_2020_first_and_second)


def _draw_vehicle_diagram(title: str, filename: str,
                          first_and_second: dict[VehicleCategory,
                                                 dict[VehicleCategory, int]]):

    categories = list(VehicleCategory)
    values = []
    for c1 in categories:
        for c2 in categories:
            if c1 not in first_and_second or c2 not in first_and_second[c1]:
                values.append(0)
            else:
                values.append(first_and_second[c1][c2])
    values = np.array(values)
    # values = np.random.randint(100, 30000, len(categories) ** 2)
    max_value = 1000
    normorlized_values = values * max_value / values.max()
    base = list(range(1, 1 + len(categories) * 2, 2))
    x = [base * len(categories)]
    y = [[n] * len(categories) for n in base]
    x = [i for l in x for i in l]
    y = [i for l in y for i in l]

    # for showing color emojis
    matplotlib.use("module://mplcairo.tk")

    plt.style.use('fivethirtyeight')
    # font = Path('TaipeiSansTCBeta-Regular.ttf')
    font = 'Noto Sans TC'
    emoji_font = Path('NotoColorEmoji.ttf')
    fig, ax = plt.subplots()
    fig.set_size_inches(8.50, 6.00)

    # This settings cannot set different alpha values to the face color and the
    # edge color.
    # ax.scatter(
    #     x,
    #     y,
    #     s=values**0.9,
    #     marker='o',
    #     c=normorlized_values,
    #     cmap='Oranges',
    #     alpha=0.5,
    #     linewidth=1,
    #     norm=colors.LogNorm(),
    # )
    # log_values = colors.LogNorm(vmin=5, vmax=800, clip=True)(1000 - normorlized_values)
    log_values = colors.PowerNorm(gamma=0.9, vmin=0, vmax=1250)(max_value - normorlized_values)
    # log_values = colors.TwoSlopeNorm(vmin=-500, vcenter=600, vmax=1000)(normorlized_values)
    edge_colors = plt.cm.autumn(log_values, alpha=1)
    face_colors = plt.cm.autumn(log_values, alpha=0.6)
    ax.scatter(
        x,
        y,
        # https://river.cat/2011/08/Visualisation-with-Area-and-Circles
        s=(normorlized_values**1.25) * 0.8,
        marker='o',
        facecolor=face_colors,
        edgecolor=edge_colors,
        linewidth=1,
    )
    threshold = 100
    interests = []
    for i in range(len(values)):
        if normorlized_values[i] > threshold:
            interests.append(values[i])
    avg = sum(interests) / len(interests)
    round_function = lambda n: n
    unit = ''
    if avg >= 10_000:
        round_function = lambda n: round(n / 10_000)
        unit = '萬'
    elif avg >= 100_000_000:
        round_function = lambda n: round(n / 100_000_000)
        unit = '億'
    for i in range(len(values)):
        if normorlized_values[i] > threshold:
            ax.annotate(
                f'{round_function(values[i])} {unit}'.strip(),
                xy=(x[i], y[i]),
                xytext=(0, 0),
                textcoords='offset points',
                ha='center',
                va='center',
                fontsize='x-small',
                font=font,
                # fontweight='ultralight',
            )

    letter_label_mapping = {
        VehicleCategory.BUS: '',
        VehicleCategory.HEAVY_TRUCK: '',
        VehicleCategory.CAR: '',
        VehicleCategory.PICKUP_TRUCK: '',
        VehicleCategory.MOTORCYCLE: '',
        VehicleCategory.BICYCLE: '',
        VehicleCategory.PEDESTRIAN: '',
        VehicleCategory.OTHER_VEHICLE: VehicleCategory.OTHER_VEHICLE,
        VehicleCategory.OTHER_PEOPLE: VehicleCategory.OTHER_PEOPLE,
        VehicleCategory.OTHER: VehicleCategory.OTHER,
    }
    emoji_label_mapping = {
        VehicleCategory.BUS: '🚌',
        VehicleCategory.HEAVY_TRUCK: '🚛',
        VehicleCategory.CAR: '🚗',
        VehicleCategory.PICKUP_TRUCK: '🛻',
        VehicleCategory.MOTORCYCLE: '🛵',
        VehicleCategory.BICYCLE: '🚲',
        VehicleCategory.PEDESTRIAN: '🚶',
        VehicleCategory.OTHER_VEHICLE: '',
        VehicleCategory.OTHER_PEOPLE: '',
        VehicleCategory.OTHER: '',
    }
    major_ticks = [n - 1 for n in base] + [base[-1] + 1]
    minor_ticks = base
    letter_labels = [letter_label_mapping[v] for v in VehicleCategory]
    emoji_labels = [emoji_label_mapping[v] for v in VehicleCategory]

    ax.set_xticks(major_ticks, labelsize=200)
    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    ax.set_xticks(
        minor_ticks,
        labels=letter_labels,
        minor=True,
        font=font,
        fontsize='small',
    )
    for tick in ax.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('center')

    ax.set_yticks(major_ticks)
    ax.yaxis.set_major_formatter(ticker.NullFormatter())
    ax.set_yticks(minor_ticks,
                  labels=letter_labels,
                  minor=True,
                  font=font,
                  fontsize='small')
    for tick in ax.yaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_verticalalignment('center')

    # This is a workaround for
    # https://github.com/matplotlib/matplotlib/issues/18883
    ax_x2 = ax.twiny()
    ax_x2.set_xticks(major_ticks, labelsize=200)
    ax_x2.xaxis.set_major_formatter(ticker.NullFormatter())
    ax_x2.set_xticks(
        minor_ticks,
        labels=emoji_labels,
        minor=True,
        font=emoji_font,
        fontsize='xx-large',
    )
    for tick in ax_x2.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('center')

    ax_y2 = ax.twinx()
    ax_y2.set_yticks(major_ticks)
    ax_y2.yaxis.set_major_formatter(ticker.NullFormatter())
    ax_y2.set_yticks(minor_ticks,
                     labels=emoji_labels,
                     minor=True,
                     font=emoji_font,
                     fontsize='xx-large')
    for tick in ax.yaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_verticalalignment('center')

    ax.invert_yaxis()
    ax_y2.invert_yaxis()

    # must after twiny()
    ax.xaxis.tick_top()
    ax_x2.xaxis.tick_top()
    # ax.xaxis.tick_bottom()
    # ax_x2.xaxis.tick_bottom()

    # must after twinx()
    ax.yaxis.tick_left()
    ax_y2.yaxis.tick_left()

    ax.grid(False)
    ax_x2.grid(False)
    ax_y2.grid(False)
    # ax.set_xlabel('第二當事人', font=font, labelpad=25.0, horizontalalignment='left', position=(0, 0))
    ax.set_xlabel(
        '第二當事人',
        font=font,
        labelpad=25.0,
        # magic!!!
        horizontalalignment='left',
        position=(0.022, 0))
    ax.xaxis.set_label_position('top')
    # ax.xaxis.set_label_position('bottom')
    ax.set_ylabel(
        '\n'.join([c for c in '第一當事人']),
        font=font,
        rotation='horizontal',
        labelpad=20.0,
        # magic!!!
        horizontalalignment='left',
        #   verticalalignment='bottom',
        position=(0, 0.7),
    )
    ax.set_title(title,
                 pad=10.0,
                 font=font,
                 fontsize='x-large',
                 fontweight='bold')
    fig.tight_layout()
    plt.savefig(filename, dpi=500)
    plt.show()

def print_tpe_bicycle_case_per_month():
    all_cases = load_all_tpe_data()
    deaths = defaultdict(int)
    injuries = defaultdict(int)
    for year in range(2019, 2022):
        for case in all_cases[year]:
            for party in case.parties:
                if party.vehicle.category == VehicleCategory.BICYCLE:
                    if party.injury_severity in [1, 5]: 
                        deaths[f'{case.date.year}-{case.date.month}'] += 1
                    elif party.injury_severity == 2:
                        injuries[f'{case.date.year}-{case.date.month}'] += 1
    keys = [f'{year}-{month}' for year in range(2019, 2022) for month in range(1, 13)]
    for key in keys:
        print(f'{key}: {deaths[key]}')
    for key in keys:
        print(f'{key}: {injuries[key]}')

    def get_pk(k, arr):
        a = len(arr) * k
        if a % 100 == 0:
            a //= 100
            return (arr[a - 1] + arr[a]) / 2
        a = int(a / 100)
        return arr[a]

    sorted_deaths = sorted([deaths[key] for key in keys])
    sorted_injuries = sorted([injuries[key] for key in keys])
    ks = [50, 60, 80]
    print(sorted_deaths)
    print(min(sorted_deaths), *[get_pk(k, sorted_deaths) for k in ks], max(sorted_deaths))
    print(sorted_injuries)
    print(min(sorted_injuries), *[get_pk(k, sorted_injuries) for k in ks], max(sorted_injuries))

def count_tpe_first_party():
    all_cases = load_all_tpe_data()
    all_cases = { y: all_cases[y] for y in range(2019, 2022) }
    first_party_count = defaultdict(int)
    for cases in all_cases.values():
        for case in cases:
            if case.severity == 1:
                for party in case.parties:
                    if party.order == 1:
                        first_party_count[party.vehicle.category] += 1
                        continue
    print(first_party_count)


if __name__ == '__main__':
    # print_percentages_from_national()
    # draw_vehicle_diagram()
    # draw_vehicle_diagram_with_cache()
    # print_tpe_bicycle_case_per_month()
    count_tpe_first_party()