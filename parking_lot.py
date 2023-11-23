import random
import string
import boto3
import json
import config
import os


class Car:
    def __init__(self, license_plate):
        if len(str(license_plate)) != 7:
            raise ValueError("License plate must be a 7-digit number.")
        self._license_plate = license_plate

    def __str__(self):
        return (f"Car with license plate {self.license_plate}")

    def park(self, parking_lot):
        """Function that allocates suitable parking spot for cars"""
        try:
            spot = random.choice(range(len(parking_lot.available_spots)))
            if parking_lot.available_spots[spot] == "0":
                parking_lot.available_spots[spot] = self.license_plate
                return (f"{self} parked successfully in spot {spot+1}")
            else:
                print(
                    f"The spot {spot + 1} is already occupied, when {self} tried to park. Already parked by {parking_lot.available_spots[spot]}"
                )
                return self.park(parking_lot)
        except Exception as error:
            return ("Exception occured due to", str(error))
    @property
    def license_plate(self):
        return self._license_plate


class ParkingLot:
    def __init__(self, lot_space=2000, width=8, height=12):
        self.lot_space = lot_space
        self.size = height * width
        self.parking_spots = (self.lot_space//self.size)
        self.available_spots = ["0"] * self.parking_spots

    def map_vehicles(self):
        """Function that maps between car and their spots in parking lot"""
        vehicle_mapping = {}
        for index, license_plate in enumerate(self.available_spots):
            if license_plate != "0":
                vehicle_mapping[index+1] = license_plate
        return (vehicle_mapping)

    @staticmethod
    def upload_to_s3():
        """Static fucntion that uploads file to S3 Bucket"""
        s3 = boto3.client(
            's3', aws_access_key_id=config.AWS_SECRET_KEY,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=config.REGION_NAME
        )
        try:
            location = os.getcwd() + config.FILE
            s3_upload = s3.upload_file(location, config.BUCKET_NAME, config.KEY)
            s3.put_object_acl(
                ACL='public-read', Bucket=config.BUCKET_NAME, Key=config.KEY
            )
            return ("Upload status is", s3_upload)
        except Exception as e:
            return(f'Error uploading file: {e}')

def main():
    parking_lot = ParkingLot(
        lot_space=config.LOT_SPACE, width=config.WIDTH, height=config.HEIGHT
    )
    cars = [Car(''.join(random.choices(string.digits, k=7))) for _ in range(config.CAR_NUM)]
    if len(cars) > len(parking_lot.available_spots):
        print("The number of cars are more than what can be occupied, so cars are occupied on FIFO basis")
        cars = cars[:len(parking_lot.available_spots)]
    for car in cars:
        status = car.park(parking_lot)
        print(status)
    json_object = parking_lot.map_vehicles()
    with open(config.FILE, "w") as file:
        json.dump(json_object, file)
    file.close()
    print(json_object)
    """
    # s3 = ParkingLot.upload_to_s3()
    #print(s3)

    """

if __name__ == "__main__":
    main()
