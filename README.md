# AirTicketingApp

## Description

The application allows users to view, search, and purchase airline tickets, as well as manage flights and users. Registered customers can buy tickets, check-in for flights, and view their upcoming flights. Sellers can sell, modify, and delete tickets, as well as search for sold tickets. Managers have additional capabilities for managing sellers, creating, modifying, and deleting flights, and reporting.

## Main Features

- **Common features for all users:**
  - Log in to the system
  - Log out from the application
  - View upcoming flights
  - Flight search (multi-criteria search)
  - Display the 10 cheapest flights between specified departure and destination airports
  - Flexible departures

- **Unregistered customers:**
  - Registration

- **Registered customers:**
  - Ticket purchase
  - View upcoming flights
  - Check-in for flights

- **Sellers:**
  - Ticket sales
  - Check-in for flights
  - Ticket modification
  - Ticket deletion
  - Search for sold tickets

- **Managers:**
  - Search for sold tickets
  - Registration of new sellers
  - Creation of flights
  - Flight modification
  - Ticket deletion
  - Reporting

## Entity Data

- **Users:**
  - Username, Password, First Name, Last Name, Role (customer, seller, manager)
  - Registered customers: Passport number, Nationality, Contact phone number, Email address, Gender

- **Flights:**
  - Flight number, Departure airport, Destination airport, Departure and arrival times, Start and end dates of flight operations, Carrier, Days of operation, Aircraft model, Price

- **Specific Flights:**
  - Specific flight code, Flight number, Departure and arrival dates and times

- **Aircraft Models:**
  - Name, Number of rows, Seat position in the row

- **Airports:**
  - Airport code (IATA code), Full name, City, Country

## Non-Functional Requirements

- Handling incorrect entries and other errors, making the program robust against user mistakes.
- Storing data in CSV format.
- Tabular display of entities.

## Test Data

For testing, provide data that includes:
- One manager
- 2 sellers
- 3 customers
- 20 flights
- 60 specific flights
- 10 airports
- 2-3 aircraft models

The application can use real airline flight data, which can be obtained from [OpenFlights](http://openflights.org/data.html).

