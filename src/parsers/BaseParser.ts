import Case from '../Case';

export default interface BaseParser {
    parseCSV(filename: string): Promise<Case[]>;
}
