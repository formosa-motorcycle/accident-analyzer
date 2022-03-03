import got from "got";
import cheerio from "cheerio";
import stream from "node:stream";
import fs from 'fs';
import { promisify } from "node:util";

/**
 * This script is for downloading accident data of TYC.
 */

const baseURI = "https://data.tycg.gov.tw";
const baseDir = "data/tyc/";
fs.mkdirSync(baseDir, { recursive: true });

const data = await got(
  `${baseURI}/opendata/datalist/search?page=0&organize=380130000C&allText=桃園市交通事故資料表`,
  {
    http2: true,
  }
).text();

const $ = cheerio.load(data);
const dataPageLinks = $("li.list-group-item").map((_, el) => {
  return $("a", el).first().attr("href");
});

async function downloadCSV(dataPageLink: string) {
  const page = await got(`${baseURI}${dataPageLink}`, {
    http2: true,
  }).text();

  const $page = cheerio.load(page);

  const downloadLinkElement = $page('a[title$=".csv"][href*="/download?"]');
  const downloadLink = downloadLinkElement.attr('href');
  const filename = downloadLinkElement.attr('title');

  const pipeline = promisify(stream.pipeline);
  console.log(`downloading ${filename}`);
  await pipeline(
    got.stream(`${baseURI}${downloadLink}`),
    fs.createWriteStream(`${baseDir}${filename}`)
  );
}

await Promise.all(dataPageLinks.map((_, link) => downloadCSV(link)));
