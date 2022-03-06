// cause_tb = {
// '01': '違規超車',
//  '02': '爭(搶)道行駛',
//  '03': '蛇行、方向不定',
//  '04': '逆向行駛',
//  '05': '未靠右行駛',
//  '06': '未依規定讓車',
//  '07': '變換車道或方向不當',
//  '08': '左轉彎未依規定',
//  '09': '右轉彎未依規定',
//  '10': '迴轉未依規定',
//  '11': '橫越道路不慎',
//  '12': '倒車未依規定',
//  '13': '超速失控',
//  '14': '未依規定減速',
//  '15': '搶越行人穿越道',
//  '16': '未保持行車安全距離',
//  '17': '未保持行車安全間隔',
//  '18': '停車操作時，未注意其他車(人)安全',
//  '19': '起步未注意其他車(人)安全',
//  '20': '吸食違禁物後駕駛失控',
//  '21': '酒醉(後)駕駛失控',
//  '22': '疲勞(患病)駕駛失控',
//  '23': '未注意車前狀態',
//  '24': '搶(闖)越平交道',
//  '25': '違反號誌管制或指揮',
//  '26': '違反特定標誌(線)禁制',
//  '27': '未依規定使用燈光',
//  '28': '暗處停車無燈光、標識',
//  '29': '夜間行駛無燈光設備',
//  '30': '裝載貨物不穩妥',
//  '31': '載貨超重而失控',
//  '32': '超載人員而失控',
//  '33': '貨物超長、寬、高而肇事',
//  '34': '裝卸貨不當',
//  '35': '裝載未盡安全措施',
//  '36': '未待乘客安全上下開車',
//  '37': '其他裝載不當肇事',
//  '38': '違規停車或暫停不當而肇事',
//  '39': '拋錨未採安全措施',
//  '40': '開啟車門不當而肇事',
//  '41': '使用手持行動電話失控',
//  '42': '其他引起事故之違規或不當行為',
//  '43': '不明原因肇事',
//  '44': '尚未發現肇事因素',
//  '45': '煞車失靈',
//  '46': '方向操縱系統故障',
//  '47': '燈光系統故障',
//  '48': '車輪脫落或輪胎爆裂',
//  '49': '車輛零件脫落',
// '50': '其他引起事故之故障',
// '51': '未依規定行走行人穿越道、地下道、天橋而穿越道路',
// '52': '未依標誌、標線、號誌或手勢指揮穿越道路',
// '53': '穿越道路未注意左右來車',
//  '54': '在道路上嬉戲或奔走不定',
//  '55': '未待車輛停妥而上下車',
//  '56': '上下車輛未注意安全',
//  '57': '頭手伸出車外而肇事',
//  '58': '乘坐不當而跌落',
//  '59': '在路上工作未設適當標識',
//  '60': '其他引起事故之疏失或行為',
//  '61': '路況危險無安全（警告）設施',
//  '62': '交通管制設施失靈或損毀',
//  '63': '交通指揮不當',
//  '64': '平交道看守疏失或未放柵欄',
//  '65': '其他交通管制不當',
//   '66': '動物竄出',
// '67': '尚未發現肇事因素',
// '':'空白',
// }
import { autoImplements } from './utilities';
export var Weather;
(function (Weather) {
    Weather[Weather["STROM"] = 1] = "STROM";
    Weather[Weather["STRONG_WIND"] = 2] = "STRONG_WIND";
    Weather[Weather["SAND_WIND"] = 3] = "SAND_WIND";
    Weather[Weather["SMOKE"] = 4] = "SMOKE";
    Weather[Weather["SNOWE"] = 5] = "SNOWE";
    Weather[Weather["RAIN"] = 6] = "RAIN";
    Weather[Weather["CLOUDY"] = 7] = "CLOUDY";
    Weather[Weather["SUNNY"] = 8] = "SUNNY";
})(Weather || (Weather = {}));
export var Light;
(function (Light) {
    Light[Light["DAYTIME"] = 1] = "DAYTIME";
    Light[Light["SUNRISE_SUNSET"] = 2] = "SUNRISE_SUNSET";
    Light[Light["NIGHT_LIGHTING"] = 3] = "NIGHT_LIGHTING";
    Light[Light["NIGHT_DARK"] = 4] = "NIGHT_DARK";
})(Light || (Light = {}));
export var RoadHierarchy;
(function (RoadHierarchy) {
    RoadHierarchy[RoadHierarchy["FREEWAY"] = 1] = "FREEWAY";
    RoadHierarchy[RoadHierarchy["PROVINCIAL"] = 2] = "PROVINCIAL";
    RoadHierarchy[RoadHierarchy["COUNTY"] = 3] = "COUNTY";
    RoadHierarchy[RoadHierarchy["COUNTRY"] = 4] = "COUNTRY";
    RoadHierarchy[RoadHierarchy["CITY"] = 5] = "CITY";
    RoadHierarchy[RoadHierarchy["VILLAGE"] = 6] = "VILLAGE";
    RoadHierarchy[RoadHierarchy["EXCLUDED"] = 7] = "EXCLUDED";
    RoadHierarchy[RoadHierarchy["OTHER"] = 8] = "OTHER";
})(RoadHierarchy || (RoadHierarchy = {}));
/**
 * Class for indicate an accident case
 */
export class Case extends autoImplements() {
}
export default Case;
