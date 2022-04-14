// TYCCrawler.downloadAll(outDir);
import TYCParser from './src/parsers/TYCParser';
const outDir = 'data/tyc/';
const allCases = await Promise.all([
    // TYCParser.parseCSV(`${outDir}101.csv`),
    //   TYCParser.parseCSV(`${outDir}102.csv`),
    //   TYCParser.parseCSV(`${outDir}traffic_accident_103.csv`),
    //   TYCParser.parseCSV(`${outDir}traffic_accident_104.csv`),
    //   TYCParser.parseCSV(`${outDir}traffic_accident_105.csv`),
    TYCParser.parseCSV(`${outDir}traffic106_10809_fix.csv`),
    //   TYCParser.parseCSV(`${outDir}traffic109_fix.csv`),
    //   TYCParser.parseCSV(`${outDir}traffic11011_fix.csv`),
]);
