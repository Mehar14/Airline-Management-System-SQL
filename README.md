# Airline-Management-System-SQL
This project focuses on the use of different SQL queries to manage CRUD (Create, Read, Update, Delete) operations involved in an Airline Management System with GUI development based on PyQt library. 

# Introduction to the Idea

• Air travel is the most popular transport system around the globe, yet the complexities attached
with it amplify with an increasing demand.

• Recent studies show that every second about 270 flights take off and make landing.

• Hence an updated system is the need of today therefore we have worked on an improvised and a
robust flight database model.

• It allows to effectively implement the functionalities coupled with it.

• Database system operations can be easily employed to handle the huge amount of data ranging
from passenger details to flight details in the field of flight handling.

# Tools used for implementation

This project is a desktop-based application which implements the MVC architecture in the following way:

• Model: We have used MySQL RDBMS to create the data layer of the project. Variety of
data related to the aviation management system has been stored in more than 20
relations each defining a unique aspect.

• View: PyQt5 library is used to create a User Interactive GUI Application which links all the
dataset to the application layer through various functions that come along with it.

• Controller: Python along with it’s libraries such as MySQL. Connecter has been used to
connect the data layer with the application layer to implement logic which processes the
data

# Functionalities of the Product
Functionalities included in the project are the mentioned below however not limited to:

• Allows the admin user only to manage updation, deletion, and insertion into the
database. This way we implement authorization and authentication for the security of
project.

• Main areas of the database i.e., passenger details, flight details, aircraft details and
airport details form the main pillars of the project and are linked to each other through
the execution of different queries working to ensure strong connectivity between each of
these entities.

• While we cover maximum fields of this database systems, yet there is still a plethora of
different activities that can be implemented as the structural design is easy to
understand.

• In addition, we have linked the QtWidgets functionalities with each query that is being
executed in the RDBMS.

# ERD
<img width="610" alt="erd" src="https://github.com/Mehar14/Airline-Management-System-SQL/assets/103940154/1bbc2f66-1ab7-4b19-a80c-b7dfeb75af9e">

# Overview of the GUI
• Login Window: Authorizes the admin of the user and moves to the next Main Menu window, if not it asks
for correct details. However, a unique feature is the fact that Guest can also Login but
only view the non-private data

• Main Menu: Gives option to choose what details the admin wants to see.

• Passenger Details: View passenger’s personal information and generate a PDF file of the ticket. Also, it
allows to view Passenger Luggage Details. Moreover, admin has the authority to update, insert and delete new passenger details.

• Flight Details: Table view of the passenger, meal and crew member information are displayed on this
window for a specific flight ID.

• Aircraft Details: Sub aircraft entities like model details, health status and repair warehouse information is
displayed through the functionality of pressing a function.

• Menu bar: Navigates the user to other windows, logout and access tools defined in the specified window.

• Airport Details: The airport authority who has bought the software have their details and patent shown
on this window.

# Snippets of GUI

Login:

![Login](https://github.com/Mehar14/Airline-Management-System-SQL/assets/103940154/95f85a05-3987-4e0a-b65f-7923a0f8b741)

List of Passengers:

![Passengers](https://github.com/Mehar14/Airline-Management-System-SQL/assets/103940154/747058c5-505c-4fd6-b1db-179273f9b96e)

Passenger Details:

![PassengerDetails](https://github.com/Mehar14/Airline-Management-System-SQL/assets/103940154/45597f20-cdac-4c1a-843e-2afe201cb23b)

Aircraft Details:

![AircraftModel](https://github.com/Mehar14/Airline-Management-System-SQL/assets/103940154/f44a4c3a-78a6-43f3-8a50-166a697be568)

Ticket:

![Ticket](https://github.com/Mehar14/Airline-Management-System-SQL/assets/103940154/8daff06a-85c6-4495-8154-4ef5fa77c5ff)

# Views, Triggers and Stored Procedures
• Views: Views have been used in the project to carry out the data showing part of the project.
The database consists of views related to showing passenger details, aircraft details and
flight details which are stored in the views.

• Triggers: Three different triggers have been defined which are linked with one table that records
the history of modifications in the database such that the timestamp and the
modification status are inserted into that table.

• Stored Procedures: Stored procedures have been created for every query that is running in the backend of
the application to connect with the database.













