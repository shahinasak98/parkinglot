import random
import string
import boto3

class Car:
    def __init__(self, license_plate):
        if len(str(license_plate))!=7:
            raise ValueError("License plate must be a 7-digit number.")
        self.license_plate = license_plate

    def __str__(self):
        return (f"Car with license plate {self.license_plate}")

    def park(self, parking_lot):
        spot = random.choice(range(len(parking_lot.available_spots)))
        if parking_lot.available_spots[spot] == "0":
            parking_lot.available_spots[spot] = self.license_plate
            return (f"{self} parked successfully in spot {spot+1}")
        else:
            print(f"The spot {spot + 1} is already occupied, when {self} tried to park. Already parked by {parking_lot.available_spots[spot]}")
            return self.park(parking_lot)



class ParkingLot:
    def __init__(self, lot_space=2000, width=8, height=12):
        self.lot_space = lot_space
        self.size = height * width
        self.parking_spots = (self.lot_space//self.size)
        self.available_spots = ["0"] * self.parking_spots

    def map_vehicles(self):
        vehicle_mapping = {}
        for index, license_plate in enumerate(self.available_spots):
            if license_plate != "0":
                vehicle_mapping[index] = license_plate
        return vehicle_mapping

def main():
    parking_lot = ParkingLot(lot_space=2000, width=100, height=2)
    cars = [Car(''.join(random.choices(string.digits, k=7))) for _ in range(20)]
    json = {}
    if len(cars) > len(parking_lot.available_spots):
        print("The number of cars are more than what can be ocupied, so cars are occupied in FIFO basis")
        cars = cars[:len(parking_lot.available_spots)]
    for car in cars:
        status = car.park(parking_lot)
        print(status)
    json = parking_lot.map_vehicles()
    print(json)
if __name__ == "__main__":
    main()
