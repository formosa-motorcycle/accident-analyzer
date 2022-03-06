export var VehicleCategory;
(function (VehicleCategory) {
    VehicleCategory["BUS"] = "\u5927\u5BA2\u8ECA";
    VehicleCategory["HEAVY_TRUCK"] = "\u5927\u8CA8\u8ECA";
    VehicleCategory["CAR"] = "\u5C0F\u5BA2\u8ECA";
    VehicleCategory["PICKUP_TRUCK"] = "\u5C0F\u8CA8\u8ECA";
    VehicleCategory["MOTORCYCLE"] = "\u6A5F\u8ECA";
    VehicleCategory["BICYCLE"] = "\u81EA\u884C\u8ECA";
    VehicleCategory["PEDESTRIAN"] = "\u884C\u4EBA";
    VehicleCategory["OTHER_VEHICLE"] = "\u5176\u4ED6\u8ECA";
    VehicleCategory["OTHER_PEOPLE"] = "\u5176\u4ED6\u4EBA";
    VehicleCategory["OTHER"] = "\u5176\u4ED6";
})(VehicleCategory || (VehicleCategory = {}));
export class Vehicle {
    // private to disallow creating other instances of this type
    constructor(key, category) {
        this.key = key;
        this.category = category;
    }
}
Vehicle.PUBLIC_CITY_BUS = new Vehicle('A01', VehicleCategory.BUS);
Vehicle.PRIVATE_CITY_BUS = new Vehicle('A02', VehicleCategory.BUS);
Vehicle.PUBLIC_HIGHWAY_BUS = new Vehicle('A03', VehicleCategory.BUS);
Vehicle.PRIVATE_HIGHWAY_BUS = new Vehicle('A04', VehicleCategory.BUS);
Vehicle.TOUR_BUS = new Vehicle('A05', VehicleCategory.BUS);
Vehicle.PERSONAL_BUS = new Vehicle('A06', VehicleCategory.BUS);
Vehicle.BUSINESS_HEAVY_TRUCK = new Vehicle('A11', VehicleCategory.HEAVY_TRUCK);
Vehicle.PERSONAL_HEAVY_TRUCK = new Vehicle('A12', VehicleCategory.HEAVY_TRUCK);
Vehicle.BUSINESS_FULL_TRAILER = new Vehicle('A21', VehicleCategory.HEAVY_TRUCK);
Vehicle.PERSONAL_FULL_TRAILER = new Vehicle('A22', VehicleCategory.HEAVY_TRUCK);
Vehicle.BUSINESS_SEMI_TRAILER = new Vehicle('A31', VehicleCategory.HEAVY_TRUCK);
Vehicle.PERSONAL_SEMI_TRAILER = new Vehicle('A32', VehicleCategory.HEAVY_TRUCK);
Vehicle.BUSINESS_TRACTOR = new Vehicle('A41', VehicleCategory.HEAVY_TRUCK);
Vehicle.PERSONAL_TRACTOR = new Vehicle('A42', VehicleCategory.HEAVY_TRUCK);
Vehicle.TAXI = new Vehicle('B01', VehicleCategory.CAR);
Vehicle.RENTAL_CAR = new Vehicle('B02', VehicleCategory.CAR);
Vehicle.PERSONAL_CAR = new Vehicle('B03', VehicleCategory.CAR);
Vehicle.BUSINESS_PICKUP_TRUCK = new Vehicle('B11', VehicleCategory.PICKUP_TRUCK);
Vehicle.PERSONAL_PICKUP_TRUCK = new Vehicle('B12', VehicleCategory.PICKUP_TRUCK);
Vehicle.MOTORCYCLE_550_UP = new Vehicle('C01', VehicleCategory.MOTORCYCLE);
Vehicle.MOTORCYCLE_250_TO_549 = new Vehicle('C02', VehicleCategory.MOTORCYCLE);
Vehicle.MOTORCYCLE_50_TO_249 = new Vehicle('C03', VehicleCategory.MOTORCYCLE);
Vehicle.MOTORCYCLE_49_UNDER = new Vehicle('C04', VehicleCategory.MOTORCYCLE);
Vehicle.MOTORCYCLE_45_KPH_UNDER = new Vehicle('C05', VehicleCategory.MOTORCYCLE);
Vehicle.MILITARY_BUS = new Vehicle('D01', VehicleCategory.OTHER_VEHICLE);
Vehicle.MILITARY_HEAVY_TRUCK = new Vehicle('D02', VehicleCategory.OTHER_VEHICLE);
Vehicle.MILITARY_CAR = new Vehicle('D03', VehicleCategory.OTHER_VEHICLE);
Vehicle.AMBULANCE = new Vehicle('E01', VehicleCategory.OTHER_VEHICLE);
Vehicle.FIRE_ENGINE = new Vehicle('E02', VehicleCategory.OTHER_VEHICLE);
Vehicle.POLICE_VEHICLE = new Vehicle('E03', VehicleCategory.OTHER_VEHICLE);
Vehicle.ENGINEERING_VEHICLE = new Vehicle('E04', VehicleCategory.OTHER_VEHICLE);
Vehicle.OTHER_SPECIAL_VEHICLE = new Vehicle('E05', VehicleCategory.OTHER_VEHICLE);
Vehicle.BICYCLE = new Vehicle('F01', VehicleCategory.BICYCLE);
Vehicle.PEDELEC = new Vehicle('F02', VehicleCategory.BICYCLE);
Vehicle.PEDAL_FREE_PEDELEC = new Vehicle('F03', VehicleCategory.BICYCLE);
Vehicle.RICKSHAW = new Vehicle('F04', VehicleCategory.OTHER_VEHICLE);
Vehicle.ANIMAL_DRAWN_VEHICLE = new Vehicle('F05', VehicleCategory.OTHER_VEHICLE);
Vehicle.OTHER_SLOW_VEHICLE = new Vehicle('F06', VehicleCategory.OTHER_VEHICLE);
Vehicle.SELF_ASSEMBLED_VEHICLE = new Vehicle('G01', VehicleCategory.OTHER_VEHICLE);
Vehicle.AGRICULTURAL_MACHINARY = new Vehicle('G02', VehicleCategory.OTHER_VEHICLE);
Vehicle.POWER_MACHINE = new Vehicle('G03', VehicleCategory.OTHER_VEHICLE);
Vehicle.TRAILER = new Vehicle('G04', VehicleCategory.OTHER_VEHICLE);
Vehicle.TRAIN = new Vehicle('G05', VehicleCategory.OTHER_VEHICLE);
Vehicle.OTHER_VEHICLE = new Vehicle('G06', VehicleCategory.OTHER_VEHICLE);
Vehicle.PEDESTRIAN = new Vehicle('H01', VehicleCategory.PEDESTRIAN);
Vehicle.PASSENGER = new Vehicle('H02', VehicleCategory.OTHER_PEOPLE);
Vehicle.OTEHR_PEOPLE = new Vehicle('H03', VehicleCategory.OTHER_PEOPLE);
Vehicle.OTHER = new Vehicle('', VehicleCategory.OTHER);
export default Vehicle;
