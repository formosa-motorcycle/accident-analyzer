import util from 'util';

import TYCCrawler from './src/crawlers/TYCCrawler';
import TYCParser from './src/parsers/TYCParser';
import { ShapeOfFields, generateShapeOfFields } from './src/tools/shapeOfFields';

const outDir = 'data/tyc/';

// TYCCrawler.downloadAll(outDir);
// const allCases = await Promise.all([
//   TYCParser.parseCSV(`${outDir}101.csv`),
//   TYCParser.parseCSV(`${outDir}102.csv`),
//   TYCParser.parseCSV(`${outDir}traffic_accident_103.csv`),
//   TYCParser.parseCSV(`${outDir}traffic_accident_104.csv`),
//   TYCParser.parseCSV(`${outDir}traffic_accident_105.csv`),
//   TYCParser.parseCSV(`${outDir}traffic106_10809_fix.csv`),
//   TYCParser.parseCSV(`${outDir}traffic109_fix.csv`),
//   TYCParser.parseCSV(`${outDir}traffic11011_fix.csv`),
// ]);

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

const shapeOfFields: ShapeOfFields = {};

await generateShapeOfFields(`${outDir}101.csv`, excludedFields, shapeOfFields);
await generateShapeOfFields(`${outDir}102.csv`, excludedFields, shapeOfFields);
await generateShapeOfFields(`${outDir}traffic_accident_103.csv`, excludedFields, shapeOfFields);
await generateShapeOfFields(`${outDir}traffic_accident_104.csv`, excludedFields, shapeOfFields);
await generateShapeOfFields(`${outDir}traffic_accident_105.csv`, excludedFields, shapeOfFields);
console.log(util.inspect(shapeOfFields, { showHidden: false, depth: null, colors: true }));
