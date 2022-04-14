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
export default class Case extends autoImplements() {
    equalTo(other) {
        return (this.date.equals(other.date)
            && this.location === other.location
            && this.severity === other.severity
            && this.death === other.death
            && this.injury === other.injury);
    }
}
