# UAV Flight Performance Calculator
# Version 2: Basic input validation
def calculate_range(airspeed_kmh,flight_time_hours):
   flight_range_km = airspeed_kmh*flight_time_hours
   return flight_range_km
while True:
   try:
    airspeed_kmh = float(input("Enter airspeed (km/h): "))
    if airspeed_kmh <=0:
       print("enter a positive number!!")
    else:
       break
   except ValueError:
    print("Enter a number!!!")
while True:  
   try:
     flight_time_hours = float(input("Enter flight duration (hours): "))
     if flight_time_hours<=0:
        print("error enter positive value!!")
     else:
        break
   except ValueError:
     print("Enter a number!!!")

flight_range_km = calculate_range(airspeed_kmh,flight_time_hours)
print("\n----- UAV Flight Report -----")
print("Airspeed: ", airspeed_kmh, "km/h")
print("Duration:", flight_time_hours, "hours")
print("Estimated range: ", flight_range_km, "km")
if flight_range_km <= 100:
    print("The flight is short range flight ")
else:
    print("The flight is a long range flight")
print("The calculation completed succesfully")
