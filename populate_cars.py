import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_rental.settings')
django.setup()
import requests
from datetime import datetime
from cars.models import Car


manufacturers = [
  "Acura",
  "Alfa Romeo",
  "Aston Martin",
  "Audi",
  "Bentley",
  "BMW",
  "Buick",
  "Cadillac",
  "Chevrolet",
  "Chrysler",
  "Citroen",
  "Dodge",
  "Ferrari",
  "Fiat",
  "Ford",
  "GMC",
  "Honda",
  "Hyundai",
  "Infiniti",
  "Jaguar",
  "Jeep",
  "Kia",
  "Lamborghini",
  "Land Rover",
  "Lexus",
  "Lincoln",
  "Maserati",
  "Mazda",
  "McLaren",
  "Mercedes-Benz",
  "MINI",
  "Mitsubishi",
  "Nissan",
  "Porsche",
  "Ram",
  "Rolls-Royce",
  "Subaru",
  "Tesla",
  "Toyota",
  "Volkswagen",
  "Volvo",
]



url = "https://cars-by-api-ninjas.p.rapidapi.com/v1/cars"
headers = {
	"x-rapidapi-key": "40d0cc352dmshc7f2620671de911p16ad36jsn03214c14f1a6",
	"x-rapidapi-host": "cars-by-api-ninjas.p.rapidapi.com"
}


def popolate_data(manufacturers, url, headers):
        for make in manufacturers:
        
                print(f'########## {make} ########')
                querystring = {"make": make, "year":2020, "Limit":1}
                response = requests.get(url, headers=headers, params=querystring)
                car_list = response.json()
             
                for car in car_list:
                       car_model = car['model']
                       car_make = car['make']
                       try:
                          car_cylinder = car['cylinders']
                          car_displacement = car['displacement']
                       except KeyError:
                              car_cylinder=0
                              car_displacement=0.0

                               
                               
                       existing_car = Car.objects.filter(make=car_make, model=car_model).exists()
                       if existing_car:
                              print("car already exists")
                              pass
                       else:
                              new_car = Car(
                                        city_mpg = car['city_mpg'],
                                        car_class = car['class'],
                                        combination_mpg = car['combination_mpg'],
                                        cylinders = car_cylinder,
                                        displacement = car_displacement,
                                        drive = car['drive'],
                                        fuel_type = car['fuel_type'],
                                        highway_mpg = car['highway_mpg'],
                                        make = car['make'],
                                        model = car['model'],
                                        transmission = car['transmission'],
                                        year = car['year'],
                                        
                                        )
                              new_car.save()
                              print(f'car_model: {new_car.model}, car_make: {new_car.make}')
                              print(f'\n\n')
                       

def calculate_price():
       cars = Car.objects.all()
       base_price_per_day = 30000  
       mileage_factor = 0.1     
       age_factor = 0.05 

       for car in cars:
                 city_mpg = int(car.city_mpg)
                 year = int(car.year)
             
                 mileage_rate = city_mpg * mileage_factor
                 age_rate = (datetime.now().year - year) * age_factor

                 rental_rate_per_day = base_price_per_day + mileage_rate + age_rate

                 daily_rent = round(rental_rate_per_day)

                 car.daily_rent = daily_rent
                 car.save()
                 print('car daily_rent saved')
             
                


if __name__ == "__main__":
    popolate_data(manufacturers, url, headers)
    calculate_price()


