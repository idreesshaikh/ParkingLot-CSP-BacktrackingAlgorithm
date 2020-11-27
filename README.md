# ParkingLot-CSP-BacktrackingAlgorithm

We have a parking lot with fixed dimension, and there is a large variety of cars, busses, motorcycles and various other vehicles that need to be parked on it for long term. In the long term, we do not care where the individual vehicles are, and if they are accessible or not, all that we care about is to fit all of the vehicles on the lot.
Note: We can rotate the vehicles to fit them into the parking lot.

### **Input:**

The input is multiple lines of text, with the individual elements being tab separated. The first line contains the length and width of the parking lot. The second line contains the number of vehicles. Each subsequent row contains the length and width of a single vehicle.


*4    4<br/>
4<br/>
4    2<br/>
2    2<br/>
1    2<br/>
2    1*<br/>

### **Output:**

Output to the standard output with values on each line are separated by tabs.

*1    1    1    1<br/>
1    1    1    1<br/>
2    2    3    3<br/>
2    2    4    4*<br/>
