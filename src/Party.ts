import { autoImplements } from './utilities';
import { Vehicle } from './Vehicle';

interface PartyParameters {
    vehicle: Vehicle;
    order?: number;
    gender?: number;
    age?: number;
    injurySeverity?: number;
    cause?: number;
  }

export default class Party extends autoImplements<PartyParameters>() {}
