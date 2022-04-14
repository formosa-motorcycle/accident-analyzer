var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
/* eslint-disable no-restricted-syntax */
import fs from 'fs';
import readline from 'readline';
import csv from 'csv-parser';
import luxon from 'luxon';
import { staticImplements } from '../utilities';
import Case from '../Case';
import Party from '../Party';
import Vehicle from '../Vehicle';
function isNumber(value) {
    return !Number.isNaN(value);
}
function isChineseNumberOrNumber(value) {
    return (['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'].includes(value)
        || isNumber(value));
}
function normalizeMetersBefore(value) {
    if (['NA', '0'].includes(value)) {
        return ' ';
    }
    return value;
}
function buildValidator(fail) {
    const required = (msg, value, format = () => true) => {
        if (!value.trim() || !format(value)) {
            console.error(msg);
            fail();
        }
    };
    const optional = (msg, value, format = () => true) => {
        if (value.trim() && !format(value)) {
            console.error(msg, value, format);
            fail();
        }
    };
    const empty = (msg, value) => {
        if (value.trim()) {
            console.error(msg);
            fail();
        }
    };
    return [required, optional, empty];
}
let TYCParser = class TYCParser {
    static async parseCSV(filename, verify = false) {
        const inStream = fs.createReadStream(filename);
        const cases = [];
        let prevCase = null;
        const parseLineBefore2016 = (data) => {
            console.log(data);
            let locationSections = [
                data['縣市'],
                data['區'],
                data['村里'],
                data['鄰'],
                data['街道'],
                data['段'],
                data['巷'],
                data['弄'],
                data['號'],
                data['公尺處'],
                data['街道1'],
                data['段1'],
                data['側'],
                data['附近'],
                data['道路'],
                data['公里'],
                data['公尺處1'],
                data['向'],
                data['車道'],
                data['平交道'],
                data['公里1'],
                data['公尺處2'],
                data['附近1'],
            ];
            locationSections = locationSections.filter((section) => section !== 'NA');
            const date = luxon.DateTime.fromObject({
                year: Number(data['西元年']),
                month: Number(data['月']),
                day: Number(data['日']),
                hour: Number(data['時']),
                minute: Number(data['分']),
            }, {
                zone: 'Asia/Taipei',
            });
            const location = locationSections.join('');
            const death = Number(data['死']);
            const injury = Number(data['受傷']);
            let severity = 3;
            if (death) {
                severity = 1;
            }
            else if (injury) {
                severity = 2;
            }
            let currentCase = new Case({
                date,
                location,
                severity,
                death,
                injury,
                parties: [],
                id: `${date.toFormat('yyyyMMdd_HHmm')}_${location}`,
            });
            if (prevCase != null && currentCase.equalTo(prevCase)) {
                currentCase = prevCase;
            }
            else {
                cases.push(currentCase);
                prevCase = currentCase;
            }
            let vehicleCode = data['當事者區分類別'];
            vehicleCode = vehicleCode === 'NA' ? '' : vehicleCode;
            const injurySeverity = data['受傷程度'];
            const party = new Party({
                vehicle: Vehicle.codeToVehicleMapping[vehicleCode],
                order: Number(data['當事者順序']),
                cause: Number(data['肇事因素個別']),
            });
            if (injurySeverity !== 'NA') {
                party.injurySeverity = Number(injurySeverity);
            }
            currentCase.parties.push(party);
        };
        const set1 = new Set();
        const parseLine = (data) => {
            if (verify) {
                if (!['交叉路口', '一般地址', '其他', '無'].includes(data['地址類型名稱'])) {
                    console.log(data);
                    throw new Error(`Invalid address type:${data['地址類型名稱']}`);
                }
            }
            // set1.add(data['地址類型名稱']);
            const districtSections = [data['發生縣市名稱'], data['發生市區鄉鎮名稱']];
            const addressSections = [
                data['發生地址_村里名稱'],
                data['發生地址_鄰'],
                data['發生地址_路街'],
                data['發生地址_段'],
                data['發生地址_巷'],
                data['發生地址_弄'],
                data['發生地址_號'],
                data['發生地址_前幾公尺'] === '0' ? ' ' : data['發生地址_前幾公尺'],
                data['發生地址_側名稱'],
            ];
            const intersectionSections = [
                data['發生交叉路口_村里名稱'],
                data['發生交叉路口_路街口'],
                data['發生交叉路口_段'],
                data['發生交叉路口_巷'],
                data['發生交叉路口_弄'],
            ];
            // data['發生地址_其他'];
            let location = `${data['發生縣市名稱']}${data['發生市區鄉鎮名稱']}`;
            if (data['發生地址_村里名稱'] !== ' ') {
                location += data['發生地址_村里名稱'];
            }
            if (data['發生地址_鄰'] !== ' ') {
                location += `${data['發生地址_鄰']}鄰`;
            }
            if (data['發生地址_路街'] !== ' ') {
                location += data['發生地址_路街'];
            }
            if (data['發生地址_段'] !== ' ') {
                if (isChineseNumberOrNumber(data['發生地址_段'])) {
                    location += `${data['發生地址_段']}段`;
                }
                else {
                    location += data['發生地址_段'];
                }
            }
            if (data['發生地址_巷'] !== ' ') {
                location += `${data['發生地址_巷']}巷`;
            }
            if (data['發生地址_弄'] !== ' ') {
                location += `${data['發生地址_弄']}弄`;
            }
            if (data['發生地址_號'] !== ' ') {
                if (isNumber(data['發生地址_號'])) {
                    location += `${data['發生地址_號']}號`;
                }
                else {
                    location += data['發生地址_號'];
                }
            }
            if (data['發生地址_其他'] !== ' ') {
                location += data['發生地址_其他'];
            }
            let intersection = '';
            if (data['發生交叉路口_路街口'] !== ' ') {
                intersection += data['發生交叉路口_路街口'];
            }
            if (data['發生交叉路口_段'] !== ' ') {
                if (isChineseNumberOrNumber(data['發生交叉路口_段'])) {
                    intersection += `${data['發生交叉路口_段']}段`;
                }
                else {
                    intersection += data['發生交叉路口_段'];
                }
            }
            if (data['發生交叉路口_巷'] !== ' ') {
                intersection += `${data['發生交叉路口_巷']}巷`;
            }
            if (data['發生交叉路口_弄'] !== ' ') {
                intersection += `${data['發生交叉路口_弄']}弄`;
            }
            if (intersection && data['發生交叉路口_村里名稱'] !== ' ') {
                intersection = data['發生交叉路口_村里名稱'] + intersection;
            }
            if (intersection) {
                location += `/${intersection}`;
            }
            if (verify) {
                if (!districtSections.every((s) => s.trim())) {
                    console.log(data);
                    console.log(districtSections);
                    throw new Error(districtSections.toString());
                }
                const [required, optional, empty] = buildValidator(() => {
                    console.log(data);
                    console.log(addressSections);
                    throw new Error(addressSections.toString());
                });
                if (data['地址類型名稱'] === '一般地址' || data['地址類型名稱'] === '交叉路口') {
                    optional('發生地址_村里名稱', data['發生地址_村里名稱']);
                    optional('發生地址_鄰', data['發生地址_鄰'], isNumber);
                    required('發生地址_路街', data['發生地址_路街']);
                    optional('發生地址_段', data['發生地址_段'], isChineseNumberOrNumber);
                    optional('發生地址_巷', data['發生地址_巷'], isNumber);
                    optional('發生地址_弄', data['發生地址_弄'], isNumber);
                    optional('發生地址_號', data['發生地址_號'], isNumber);
                    optional('發生地址_前幾公尺', normalizeMetersBefore(data['發生地址_前幾公尺']), isNumber);
                    optional('發生地址_側名稱', data['發生地址_側名稱']);
                }
                else if (data['地址類型名稱'] === '無') {
                    optional('發生地址_村里名稱', data['發生地址_村里名稱']);
                    empty('發生地址_鄰', data['發生地址_鄰']);
                    empty('發生地址_路街', data['發生地址_路街']);
                    empty('發生地址_段', data['發生地址_段']);
                    empty('發生地址_巷', data['發生地址_巷']);
                    empty('發生地址_弄', data['發生地址_弄']);
                    // some special cases have address number
                    optional('發生地址_號', data['發生地址_號']);
                    empty('發生地址_前幾公尺', normalizeMetersBefore(data['發生地址_前幾公尺']));
                    empty('發生地址_側名稱', data['發生地址_側名稱']);
                }
                else if (data['地址類型名稱'] === '其他') {
                    optional('發生地址_村里名稱', data['發生地址_村里名稱']);
                    optional('發生地址_鄰', data['發生地址_鄰'], isNumber);
                    optional('發生地址_路街', data['發生地址_路街']);
                    optional('發生地址_段', data['發生地址_段'], isChineseNumberOrNumber);
                    optional('發生地址_巷', data['發生地址_巷'], isNumber);
                    optional('發生地址_弄', data['發生地址_弄'], isNumber);
                    optional('發生地址_號', data['發生地址_號'], isNumber);
                    optional('發生地址_前幾公尺', normalizeMetersBefore(data['發生地址_前幾公尺']), isNumber);
                    optional('發生地址_側名稱', data['發生地址_側名稱']);
                }
                let good = false;
                if (data['地址類型名稱'] === '交叉路口') {
                    good = !intersectionSections.every((s) => !s.trim());
                }
                else if (data['地址類型名稱'] === '一般地址') {
                    good = intersectionSections.slice(1).every((s) => !s.trim());
                    if (!data['發生交叉路口_村里名稱'].trim()) {
                        console.log(data);
                        console.warn(`normal address contains village name: ${data['發生交叉路口_村里名稱']}`);
                    }
                }
                else if (data['地址類型名稱'] === '無') {
                    good = intersectionSections.slice(1).every((s) => !s.trim());
                    if (data['發生交叉路口_村里名稱'].trim()) {
                        console.warn(`other address contains village name: ${data['發生交叉路口_村里名稱']}`);
                    }
                }
                else if (data['地址類型名稱'] === '其他') {
                    good = true;
                }
                if (!good) {
                    console.log(data);
                    console.log(intersectionSections);
                    throw new Error(intersectionSections.toString());
                }
                good = true;
                if (data['地址類型名稱'] === '其他') {
                    good = Boolean(data['發生地址_其他'].trim());
                }
                else if (data['地址類型名稱'] === '無') {
                    good = !data['發生地址_其他'].trim();
                }
                if (!good) {
                    console.log(data);
                    console.log(data['地址類型名稱']);
                    throw new Error(data['地址類型名稱']);
                }
            }
            // set1.add(data['地址類型名稱']);
            // const date = luxon.DateTime.fromFormat(
            //   `${data['發生日期']}${data['發生時間']}`,
            //   'yyyyMMddHHmmss',
            //   {
            //     zone: 'Asia/Taipei',
            //   },
            // );
        };
        const outStream = csv().on('headers', (headers) => {
            if (headers.includes('發生日期')) {
                outStream.on('data', parseLine);
            }
            else if (headers.includes('西元年')) {
                outStream.on('data', parseLineBefore2016);
            }
            else {
                throw Error(`Unsupported CSV format: ${filename}`);
            }
        });
        const rl = readline.createInterface({
            input: inStream,
        });
        const l = 0;
        for await (const line of rl) {
            if (l < 10) {
                outStream.write(line);
                outStream.write('\n');
                // console.log(line);
                // l += 1;
            }
            else {
                break;
            }
        }
        for (const c of cases) {
            console.log(c);
        }
        console.log(Array.from(set1));
        return cases;
    }
};
TYCParser = __decorate([
    staticImplements()
], TYCParser);
export default TYCParser;
