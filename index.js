import TYCParser from './src/parsers/TYCParser';
import CSVExporter from './src/exporters/CSVExporter';
const dataDir = 'data';
const outputsDir = 'outputs';
// TYCCrawler.downloadAll(dataDir);
const allCases = await Promise.all([
    TYCParser.parseCSV(`${dataDir}/tyc/101.csv`),
    TYCParser.parseCSV(`${dataDir}/tyc/102.csv`),
    TYCParser.parseCSV(`${dataDir}/tyc/traffic_accident_103.csv`),
    TYCParser.parseCSV(`${dataDir}/tyc/traffic_accident_104.csv`),
    TYCParser.parseCSV(`${dataDir}/tyc/traffic_accident_105.csv`),
    // TYCParser.parseCSV(`${dataDir}/tyc/traffic106_10809_fix.csv`),
    // TYCParser.parseCSV(`${dataDir}/tyc/traffic109_fix.csv`),
    // TYCParser.parseCSV(`${dataDir}/tyc/traffic11011_fix.csv`),
]);
CSVExporter.export(`${outputsDir}/tyc/tyc-2012.csv`, allCases[0], 2);
CSVExporter.export(`${outputsDir}/tyc/tyc-2013.csv`, allCases[1], 2);
CSVExporter.export(`${outputsDir}/tyc/tyc-2014.csv`, allCases[2], 2);
CSVExporter.export(`${outputsDir}/tyc/tyc-2015.csv`, allCases[3], 2);
CSVExporter.export(`${outputsDir}/tyc/tyc-2016.csv`, allCases[4], 2);
const excludedFields = new Set([
    '村里',
    '鄰',
    '街道',
    '段',
    '巷',
    '弄',
    '號',
    '公尺處',
    '街道1',
    '段1',
    '側',
    '附近',
    '道路',
    '公里',
    '公尺處1',
    '向',
    '車道',
    '平交道',
    '公里1',
    '公尺處2',
    '附近1',
]);
const shapeOfFields = {};
// await generateShapeOfFields(`${outDir}101.csv`, excludedFields, shapeOfFields);
// await generateShapeOfFields(`${outDir}102.csv`, excludedFields, shapeOfFields);
// await generateShapeOfFields(`${outDir}traffic_accident_103.csv`, excludedFields, shapeOfFields);
// await generateShapeOfFields(`${outDir}traffic_accident_104.csv`, excludedFields, shapeOfFields);
// await generateShapeOfFields(`${outDir}traffic_accident_105.csv`, excludedFields, shapeOfFields);
// console.log(util.inspect(shapeOfFields, { showHidden: false, depth: null, colors: true }));
