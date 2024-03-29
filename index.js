/* eslint-disable no-console */
/* eslint-disable @typescript-eslint/no-unused-vars */
import util from 'util';
import TYCCrawler from './src/crawlers/TYCCrawler';
import TYCParser from './src/parsers/TYCParser';
import { generateShapeOfFields } from './src/tools/shapeOfFields';
import CSVExporter from './src/exporters/CSVExporter';
const dataDir = 'data';
const outputsDir = 'outputs';
async function downloadTYCData() {
    return TYCCrawler.downloadAll(dataDir);
}
async function parseAndExportTYCDate() {
    const allCases = await Promise.all([
        new TYCParser(`${dataDir}/tyc/101.csv`).parse(),
        new TYCParser(`${dataDir}/tyc/102.csv`).parse(),
        new TYCParser(`${dataDir}/tyc/traffic_accident_103.csv`).parse(),
        new TYCParser(`${dataDir}/tyc/traffic_accident_104.csv`).parse(),
        new TYCParser(`${dataDir}/tyc/traffic_accident_105.csv`).parse(),
        // not support yet
        // new TYCParser(`${dataDir}/tyc/traffic106_10809_fix.csv`).parse(),
        // new TYCParser(`${dataDir}/tyc/traffic109_fix.csv`).parse(),
        // new TYCParser(`${dataDir}/tyc/traffic11011_fix.csv`).parse(),
    ]);
    CSVExporter.export(`${outputsDir}/tyc/tyc-2012_2016.csv`, [].concat(...allCases), 
    /* partyNumber= */ 2);
}
async function generateTYCShapeOfFields() {
    const outDir = `${outputsDir}/tyc/`;
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
    await generateShapeOfFields(`${outDir}101.csv`, excludedFields, shapeOfFields);
    await generateShapeOfFields(`${outDir}102.csv`, excludedFields, shapeOfFields);
    await generateShapeOfFields(`${outDir}traffic_accident_103.csv`, excludedFields, shapeOfFields);
    await generateShapeOfFields(`${outDir}traffic_accident_104.csv`, excludedFields, shapeOfFields);
    await generateShapeOfFields(`${outDir}traffic_accident_105.csv`, excludedFields, shapeOfFields);
    console.log(util.inspect(shapeOfFields, { showHidden: false, depth: null, colors: true }));
}
