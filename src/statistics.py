import pickle
from collections import Counter, defaultdict
from typing import Callable
from case import *
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from pathlib import Path

with open('tpe-2020.pickle', 'rb') as f:
    cases = pickle.load(f)


@dataclass
class SubTask:
    filter_party: Callable[[Party], bool]
    field: str
    title: str
    filename: str
    counter: Counter = field(default_factory=Counter)


@dataclass
class Task:
    filter_case: Callable[[Case], bool]
    subtasks: list[SubTask]


@dataclass
class Analyzer:
    cases: list[Case]
    tasks: list[Task] = field(default_factory=list)

    def run(self):
        for case in cases:
            for task in self.tasks:
                if not task.filter_case(case):
                    continue
                for party in case.parties:
                    for subtask in task.subtasks:
                        if subtask.filter_party(party):
                            subtask.counter[getattr(party, subtask.field)] += 1
        for task in self.tasks:
            min_x = min(
                min(subtask.counter.keys()) for subtask in task.subtasks)
            max_x = max(
                max(subtask.counter.keys()) for subtask in task.subtasks)
            x = range(min_x, max_x + 1)
            for subtask in task.subtasks:
                y = [subtask.counter[x_value] for x_value in x]
                fig, ax = plt.subplots()
                ax.bar(x, y)
                ax.set_xticks(
                    range((min_x // 10 + 1) * 10, max_x // 10 * 10 + 11, 10))
                ax.set_xlabel('年齡', font=Path('TaipeiSansTCBeta-Regular.ttf'))
                ax.set_ylabel('人\n數',
                              font=Path('TaipeiSansTCBeta-Regular.ttf'),
                              rotation='horizontal',
                              labelpad=10.0)
                ax.set_title(subtask.title,
                             font=Path('TaipeiSansTCBeta-Regular.ttf'))
                plt.axvline(x=33, color='orange', linewidth=0.8)
                plt.tight_layout()
                plt.savefig(subtask.filename, dpi=500)


plt.style.use('fivethirtyeight')


def is_a1a2(case: Case):
    return case.severity <= 2


def is_a1a2a3(case: Case):
    return case.severity <= 3


def has_age(party: Party):
    return party.age != 0


a1a2_task = Task(is_a1a2, [
    SubTask(lambda party: has_age(party) and party.order == 1, 'age',
            '第一當事人年齡分布-A1、A2', 'A1A2_第一當事人年齡分布.png'),
    SubTask(
        lambda party: has_age(party) and party.order == 1 and party.vehicle.
        category == VehicleCategory.CAR, 'age', '第一當事人開車的年齡分布-A1、A2',
        'A1A2_第一當事人開車的年齡分布.png'),
    SubTask(lambda party: has_age(party) and party.order != 1, 'age',
            '非第一當事人年齡分布-A1、A2', 'A1A2_非第一當事人年齡分布.png'),
    SubTask(lambda party: has_age(party) and party.order == 2, 'age',
            '第二當事人年齡分布-A1、A2', 'A1A2_第二當事人年齡分布.png'),
    SubTask(lambda party: has_age(party) and party.cause == 13, 'age',
            '當事人超速年齡分布-A1、A2', 'A1A2_當事人超速年齡分布.png'),
    SubTask(lambda party: has_age(party) and party.cause == 23, 'age',
            '當事人未注意車前狀況年齡分布-A1、A2', 'A1A2_當事人未注意車前狀況年齡分布.png'),
    SubTask(lambda party: has_age(party) and party.cause != 23, 'age',
            '當事人非未注意車前狀況年齡分布-A1、A2', 'A1A2_當事人飛未注意車前狀況年齡分布.png'),
])

a1a2a3_task = Task(is_a1a2a3, [
    SubTask(lambda party: has_age(party) and party.order == 1, 'age',
            '第一當事人年齡分布-A1、A2、A3', 'A1A2A3_第一當事人年齡分布.png'),
    SubTask(
        lambda party: has_age(party) and party.order == 1 and party.vehicle.
        category == VehicleCategory.CAR, 'age', '第一當事人開車的年齡分布-A1、A2、A3',
        'A1A2A3_第一當事人開車的年齡分布.png'),
    SubTask(lambda party: has_age(party) and party.order != 1, 'age',
            '非第一當事人年齡分布-A1、A2、A3', 'A1A2A3_非第一當事人年齡分布.png'),
    SubTask(lambda party: has_age(party) and party.order == 2, 'age',
            '第二當事人年齡分布-A1、A2、A3', 'A1A2A3_第二當事人年齡分布.png'),
    SubTask(lambda party: has_age(party) and party.cause == 13, 'age',
            '當事人超速年齡分布-A1、A2、A3', 'A1A2A3_當事人超速年齡分布.png'),
    SubTask(lambda party: has_age(party) and party.cause == 23, 'age',
            '當事人未注意車前狀況年齡分布-A1、A2、A3', 'A1A2A3_當事人未注意車前狀況年齡分布.png'),
    SubTask(lambda party: has_age(party) and party.cause != 23, 'age',
            '當事人非未注意車前狀況年齡分布-A1、A2、A3', 'A1A2A3_當事人非未注意車前狀況年齡分布.png'),
])

analyzer = Analyzer(cases, [a1a2_task, a1a2a3_task])
analyzer.run()

a1a2a3_is_first = a1a2a3_task.subtasks[0]
a1a2a3_not_first = a1a2a3_task.subtasks[2]

all_keys = set(a1a2a3_is_first.counter) | set(a1a2a3_not_first.counter)
divided = defaultdict(float)
for k in all_keys:
    if k < 16 or k > 84:
        continue
    if a1a2a3_is_first.counter[k] == 0:
        divided[k] = 0
    else:
        divided[k] = a1a2a3_not_first.counter[k] / a1a2a3_is_first.counter[k]


min_x = min(divided)
max_x = max(divided)
x = range(min_x, max_x + 1)
y = [divided[x_value] for x_value in x]
fig, ax = plt.subplots()
ax.bar(x, y)
ax.set_xticks(
    range((min_x // 10 + 1) * 10, max_x // 10 * 10 + 11, 10))
ax.set_xlabel('年齡', font=Path('TaipeiSansTCBeta-Regular.ttf'))
ax.set_ylabel('比\n率',
              font=Path('TaipeiSansTCBeta-Regular.ttf'),
              rotation='horizontal',
              labelpad=10.0)
ax.set_title('非第一當事人除第一當事人比率-16 至 84 歲-A1、A2、A3',
             font=Path('TaipeiSansTCBeta-Regular.ttf'))
plt.axvline(x=33, color='orange', linewidth=0.8)
plt.tight_layout()
plt.savefig('A1A2A3_非第一當事人與第一當事人比率_16至84歲.png', dpi=500)



a1a2_is_first = a1a2_task.subtasks[0]
a1a2_not_first = a1a2_task.subtasks[2]

all_keys = set(a1a2_is_first.counter) | set(a1a2_not_first.counter)
divided = defaultdict(float)
for k in all_keys:
    if k < 16 or k > 84:
        continue
    if a1a2_is_first.counter[k] == 0:
        divided[k] = 0
    else:
        divided[k] = float(a1a2_not_first.counter[k]) / a1a2_is_first.counter[k]


min_x = min(divided)
max_x = max(divided)
x = range(min_x, max_x + 1)
y = [divided[x_value] for x_value in x]
fig, ax = plt.subplots()
ax.bar(x, y)
ax.set_xticks(
    range((min_x // 10 + 1) * 10, max_x // 10 * 10 + 11, 10))
ax.set_xlabel('年齡', font=Path('TaipeiSansTCBeta-Regular.ttf'))
ax.set_ylabel('比\n率',
              font=Path('TaipeiSansTCBeta-Regular.ttf'),
              rotation='horizontal',
              labelpad=10.0)
ax.set_title('非第一當事人除第一當事人比率-16 至 84 歲-A1、A2',
             font=Path('TaipeiSansTCBeta-Regular.ttf'))
plt.axvline(x=33, color='orange', linewidth=0.8)
plt.tight_layout()
plt.savefig('A1A2_非第一當事人與第一當事人比率_16至84歲.png', dpi=500)