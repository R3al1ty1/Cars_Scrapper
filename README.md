# Cars_Scrapper

## Main task - find the best solution for the user (look up for the best car by user request)

### Tasks:
1. Get all available cars from query
2. Save all cars to the database
3. Find the best one
4. Use ML for that
5. How to add to DB cars by going through IDs on the websites?
---

### Required Websites analysis

* auto.ru
* drom.ru
* avito.ru
* mobile.de

---

### Required params (If param does not exist on page, use placeholders)

- [X] Mileage
- [X] Release year
- [X] Owner's number
- [X] Is owner selling the car?
- [X] Number of registrations
- [X] Car specifications compared to car passport
- [X] Frame type
- [X] Transmission Type
- [X] Drive Type (Rear, Front or 4WD)
- [X] Fuel used for the car
- [X] Date of advert publish
- [X] Tax
- [X] Steering wheel side
- [X] Color
- [X] Power of car
- [X] Volume of engine
- [ ] Car price
- [ ] Car location
---
### Side Params (Could be done later)
- [ ] Cylinders number
- [ ] Frame name
- [ ] Ecology class
- [ ] Equipment
- [ ] Clearence
- [ ] Fuel Consumption
- [ ] Trunk volume
- [ ] Wheels characteristic
- [ ] Passenger capacity
- [ ] Car dimensions
- [ ] Car weight
- [ ] Fuel tank volume
- [ ] Brakes type

## **IMPORTANT**
### Advertisment index - sum of all points of advertisment analysis, defines betterness and priority of selected ad

- Rate an ad with the average of all params. The rating should be based on gathered required params (e.g. mileage, release year etc.)


> 0.2 * mileage + 0.2 * advert age + 0.3 * price difference to the middle + 0.3 * car age

## Import costs calculation
### If selected car should be imported from the foreign country, script should sum car price with import fees and estimated delivery cost

## Neural Networks

## Additional analysis

### Required tasks

* Analyze car conditions in case of photos and output car conditions in points (0-64 points, where 0 is worst and 64 is the best)
* Analyse description text and output chance of car problems (0-64, where 0 is very problematic car and 64 is best car ever)
* Gather data from media and recognize pros and cons from each article

## Graphical interface

### Required simple and pretty user interface, which includes queue input and result output. Interface should be simple and intuitive

## Notifications

### Telegram integration for instant user notification about new announcements

## Learning of Postgres (both)

* Create the DB of all cars on the website and configs for models. (essential)
* Download DB
* ML from Required tasks
* Reseller checker
* News analysis (brand mentions)
