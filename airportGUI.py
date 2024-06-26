from PyQt5 import QtWidgets,uic
import sys
import os
import mysql.connector
import qrcode
from PIL import Image
from fpdf import FPDF
global guestuser


def UpdatePassengerRecord(PassportNum,NewPhone,NewEmail):
    changeEmail = False #add function return for tickbox
    changePhone = True

    if NewEmail != "":
        query = 'update passengers set email = "'+NewEmail+'" where passportnumber = "'+PassportNum+'";'
        cursor.execute(query)
    if NewPhone != "":
        query = 'update passengers set phonenumber = '+str(NewPhone)+' where passportnumber = "'+PassportNum+'";'
        cursor.execute(query)
    
    connection.commit()


def InsertPassengerRecord(tup):
    hasLuggage = True
    query = 'insert into passengers values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    values = (tup[0],tup[1],tup[2],tup[3],tup[4],tup[5],tup[6],tup[7],tup[8])
    cursor.execute(query,values)
    connection.commit()

    query = 'insert into ticket values(%s,%s,%s,%s,%s,%s)'
    values = (tup[9],tup[10],tup[0],tup[11],tup[13],tup[12])
    cursor.execute(query,values)
    connection.commit()

    if hasLuggage:
        query = 'insert into luggage values (%s,%s,%s,%s)'
        values = (tup[9],tup[14],tup[15],tup[16])
        cursor.execute(query,values)
        connection.commit()

    print("Record inserted")

def DeletePassengerRecord(PassportNum):
    #query = 'delete from passengers where passportnumber = "'+PassportNum+'";'
    cursor.execute('delete from mealforticket where ticketnumber in(select ticketnumber from ticket where passportnumber = "'+PassportNum+'");')
    connection.commit()
    cursor.execute('delete from luggage where ticketnumber in(select ticketnumber from ticket where passportnumber = "'+PassportNum+'");')
    connection.commit()
    cursor.execute('delete from ticket where passportnumber = "'+PassportNum+'";')
    connection.commit()
    cursor.execute('delete from passengers where passportnumber = "'+PassportNum+'";')
    connection.commit()
    print("Record deleted")

def ViewPassengerRecord(PassportNum):
    cursor.callproc('SelectPassengerDetails',[str(PassportNum)])
    result = cursor.stored_results()
    for i in result:
        j = i.fetchall() 
    return j[0]

def FetchLuggageCount(flightid):
    cursor.execute('select sum(LuggagePieces) from luggage where ticketnumber in(select ticketnumber from ticket where FlightID ="'+flightid+'");')
    result = cursor.fetchall()
    return result[0][0]

def FetchFlightStatus(FlightID):
    cursor.execute('select IsArr_Dept from flight where flightid = "'+FlightID+'"')
    return cursor.fetchall()

def ViewFlightRecord(FlightID):
    status = FetchFlightStatus(FlightID)
    if status[0][0] == 'Arrival':
        cursor.callproc('GetFlightDetailsArrival',[FlightID])
        result = cursor.stored_results()
        for i in result:
            j = i.fetchall()

        j.append('a')
        return j 

    elif status[0][0] == 'Departure':
        cursor.callproc('GetFlightDetailsDepartures',[FlightID])
        result = cursor.stored_results()
        for i in result:
            j = i.fetchall() 
        
        j.append('d')
        return j

    else: 
        j = ['x','x']

def FetchPassengerOnFlightCount(flightid):
    cursor.execute('select count(*) from ticket where flightid = "'+flightid+'"')
    return cursor.fetchall()[0][0]

def InsertPassengerRecord(tup):
    hasLuggage = True
    query = 'insert into passengers values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    values = (tup[0],tup[1],tup[2],tup[3],tup[4],tup[5],tup[6],tup[7],tup[8])
    cursor.execute(query,values)
    connection.commit()

    query = 'insert into ticket values(%s,%s,%s,%s,%s,%s)'
    values = (tup[9],tup[10],tup[0],tup[11],tup[13],tup[12])
    cursor.execute(query,values)
    connection.commit()

    if hasLuggage:
        query = 'insert into luggage values (%s,%s,%s,%s)'
        values = (tup[9],tup[14],tup[15],tup[16])
        cursor.execute(query,values)
        connection.commit()

    print("Record inserted")


connection = mysql.connector.connect(host = "localhost", database = "airportproject", password = "fruity", user = "root")
cursor = connection.cursor()

path = os.path.dirname(__file__)
path = '//'.join(path.split("\\"))

#Ticket Class
class ticketDialog(QtWidgets.QDialog):
    def __init__(self):
        super(ticketDialog,self).__init__()
        uic.loadUi(path + "//UI//ticketdialog.ui",self)

class ticketmaker():
    #Ticket Info
    pdf_airline = ""
    pdf_ticketnumber = ""
    pdf_flightID = ""
    pdf_passport_numb = ""
    pdf_username = ""
    pdf_class = ""
    pdf_seatNumber = ""
    pdf_departure = ""
    pdf_arrival = ""

    data = ""
   
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

    def __init__(self,passportnum):
        self.passport_numb = passportnum;
        cursor.execute('select airlinename,TicketNumber,flightid,passportnumber,firstname,lastname,class,seatnumber,DepartureAirportIATA from (select * from departures join airline where DepartureAirlineIATA = AirlineIATA) as t join ticket using(flightid) join passengers using(passportnumber) where passportnumber = "'+self.passport_numb+'";')
        tup= cursor.fetchall()
        info = tup[0]
        self.pdf_airline = info[0]
        self.pdf_ticketnumber = info[1]
        self.pdf_flightID = info[2]
        self.pdf_passport_numb = info[3]
        self.pdf_username = info[4] + " " + info[5]
        self.pdf_class = info[6]
        self.pdf_seatNumber = info[7]
        self.pdf_departure = "KHI"
        self.pdf_arrival = info[8]

    def preparedata(self):
    
        #Making Data Variable for QRcode
        self.data = "Airline: " + self.pdf_airline + "\n"
        self.data = self.data + "Ticket Number: " + self.pdf_ticketnumber + "\n"
        self.data = self.data + "Flight ID: " + self.pdf_flightID + "\n"
        self.data = self.data + "Name: " + self.pdf_username + "\n"
        self.data = self.data + "Passport Number: " + self.pdf_passport_numb + "\n"
        self.data = self.data + "Seat Number: " + self.pdf_seatNumber + "\n"
        self.data = self.data + "Flight ID: " + self.pdf_flightID + "\n"
        self.data = self.data + "From: " + self.pdf_departure + "\n"
        self.data = self.data + "To: " + self.pdf_arrival + "\n"

        self.pdf_name = self.pdf_ticketnumber +"-"+ self.pdf_username + ".pdf"

    def makepdf(self):
        #Make QR
        self.preparedata()
        self.qr.add_data(self.data)
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color="black", back_color="white").convert('RGB')
        img.save(path + "\\tickets\\Temp_QR_CODE\\QRcode.png")

        #PDF
        pdf_w=210
        pdf_h=297

        #Load MainBackGroundImage
        pic = path + "\\ticket-bg.png"

        #PDF MAKER
        pdf = FPDF(orientation='L')
        pdf.add_page()
        pdf.image(pic,0,0,w = 297)
        pdf.image("QRcode.png",190,60, w = 80)
        ##pdf.set_line_width(1.0)
        ##pdf.rect(5,5,287,200)
        pdf.set_font("Courier",size = 45)
        pdf.text(30, 32,txt = self.pdf_airline)
        pdf.set_font("Courier",size = 20)
        pdf.text(30,60,txt = "Ticket Number: " + self.pdf_ticketnumber)
        pdf.text(30,75,txt = "Flight ID: " + self.pdf_flightID)
        pdf.text(30,90,txt = "Name: " + self.pdf_username)
        pdf.text(30,105,txt = "Passport Number: " + self.pdf_passport_numb)
        pdf.text(30,120,txt = "Class: " + self.pdf_class)
        pdf.text(30,135,txt = "Seat Number: " + self.pdf_seatNumber)
        pdf.text(30,150,txt = "From: " + self.pdf_departure)
        pdf.text(30,165,txt = "To: " + self.pdf_arrival)

        pdf.output(path + "\\tickets\\" + self.pdf_name,'F')

#Switch Window        

class SwitchWindows():

    def openPassengerWindow(self):
        self.passenger = PassengerWindow()
        self.passenger.show()
        self.close()
    
    def openFlightWindow(self):
        self.flight = FlightWindow()
        self.flight.show()
        self.close()
    
    def openAircraftWindow(self):
        self.aircraft = AircraftWindow()
        if usertype:
            self.aircraft.actionFlight_Details.setEnabled(False)
            self.aircraft.actionPassenger_Details_2.setEnabled(False)
        self.aircraft.show()
        self.close()
    
    def openAirportWindow(self):
        self.airport = AirportWindow()
        if usertype:
            self.airport.actionFlight_Details.setEnabled(False)
            self.airport.actionPassenger_Details_2.setEnabled(False)
        self.airport.show()
        self.close()

    def openLoginWindow(self):
        self.login = LoginWindow()
        self.login.show()
        self.close()

#Airport Class

class AirportWindow(QtWidgets.QMainWindow):
     def __init__(self):
        super(AirportWindow,self).__init__()
        uic.loadUi(path +"//UI//airportdetails.ui",self)
        self.actionFlight_Details.triggered.connect(self.flightMenuSelected)
        self.actionAircraft_Details_2.triggered.connect(self.aircraftMenuSelected)
        self.actionPassenger_Details_2.triggered.connect(self.passengerMenuSelected)

        self.actionAdmin_Logout.triggered.connect(self.backtoLogin)
        

     def passengerMenuSelected(self,checked):
        SwitchWindows.openPassengerWindow(self)

     def flightMenuSelected(self,checked):
        SwitchWindows.openFlightWindow(self)

     def aircraftMenuSelected(self,checked):
        SwitchWindows.openAircraftWindow(self)

     def backtoLogin(self,checked):
        SwitchWindows.openLoginWindow(self)

#Aircraft Class
class AircraftWareHouse(QtWidgets.QMainWindow):
     registrationNumber = ""
     def __init__(self,registrationfrommain):
        self.registrationNumber = registrationfrommain
        super(AircraftWareHouse,self).__init__()
        uic.loadUi(path+"//UI//warehouse.ui",self)
        self.updatewarehousedata()

     def updatewarehousedata(self):
        cursor.callproc('GiveTable_ViewAircraftWarehouse',[self.registrationNumber])
        res = cursor.stored_results()
        for i in res:
            j = i.fetchall()
        info = j[0]
        self.warehousenumber.setText("Warehouse Number: "+info[0])
        self.supervisingengineer.setText("Supervisor ID: "+info[1])
        self.capacityengineer.setText("Engineers Capacity: "+str(info[2]))
        self.capacityplane.setText("Aircraft Capacity: "+str(info[3]))
        

class AircraftModelDetails(QtWidgets.QMainWindow):
     registrationNumber = ""
     def __init__(self,registrationfrommain):
        self.registrationNumber = registrationfrommain
        super(AircraftModelDetails,self).__init__()
        uic.loadUi(path+"//UI//airplanemodel.ui",self)
        self.updatemodeldata()

     def updatemodeldata(self):
        cursor.callproc('GiveTable_ViewAircraftModelInfo',[self.registrationNumber])
        res = cursor.stored_results()
        for i in res:
            j = i.fetchall()
        info = j[0]
        self.manufacturer.setText("Manufacturer: "+info[0])
        self.purpose.setText("Purpose: "+info[1])
        self.manufactured_in.setText("Manufactured In: "+info[2])
        self.seating_capacity.setText("Seating Capacity: "+str(info[3]))
        self.luggage_weight.setText("Luggage Weight(kg): " +str(info[4]))
        self.price.setText("Price($): "+str(info[5]))

class AircraftHealthWindow(QtWidgets.QMainWindow):
     registrationNumber = ""
     def __init__(self,registrationfrommain):
        self.registrationNumber = registrationfrommain
        super(AircraftHealthWindow,self).__init__()
        uic.loadUi(path+"//UI//airplanehealth.ui",self)
        self.updatehealthdata()

     def updatehealthdata(self):
        cursor.callproc('GiveTable_AircraftHealthStatus',[self.registrationNumber])
        res = cursor.stored_results()
        for i in res:
            j = i.fetchall()
        info = j[0]
        self.leftengine.setText("Left Engine: "+ info[1])
        self.rightengine.setText("Right Engine: "+info[2])
        self.landinggear.setText("Landing Gear: " + info[4])
        self.fuselage.setText("Fuselage: "+info[3])
        self.flapcondition.setText("Flap: "+info[5])
        self.overallstatus.setText("Overall Status: "+info[6])



class AircraftWindow(QtWidgets.QMainWindow):
    registrationNumber = ""
    def __init__(self):
        super(AircraftWindow,self).__init__()
        uic.loadUi(path +"//UI//aircraftdetails.ui",self)

        self.actionPassenger_Details_2.triggered.connect(self.passengerMenuSelected)
        self.actionFlight_Details.triggered.connect(self.flightMenuSelected)
        self.actionAirport_Details_2.triggered.connect(self.airportMenuSelected)

        self.actionAdmin_Logout.triggered.connect(self.backtoLogin)

        self.modeldetailsbutton.clicked.connect(self.modeldetailpressed)
        self.airplanehealthbutton.clicked.connect(self.healthbuttonpressed)
        self.warehousebutton.clicked.connect(self.warehousebuttonpressed)

        self.registrationNumberinput.editingFinished.connect(self.entersRegistration)
    
    def entersRegistration(self):
        self.registrationNumber = self.registrationNumberinput.text()
        cursor.callproc('GiveTable_ViewAircraft',[self.registrationNumber])
        res = cursor.stored_results()
        for i in res:
            j = i.fetchall()
            info = j[0]

        self.modelnumber.setText("Model Number: " + info[0])
        self.ownerairline.setText("Owner Airline " + info[1])

    def modeldetailpressed(self,checked):
        self.aircraftmodel = AircraftModelDetails(self.registrationNumber)
        self.aircraftmodel.show()

    def healthbuttonpressed(self,checked):
        self.aircrafthealth = AircraftHealthWindow(self.registrationNumber)
        self.aircrafthealth.show()
        

    def warehousebuttonpressed(self,checked):
        self.aircraftwarehouse = AircraftWareHouse(self.registrationNumber)
        self.aircraftwarehouse.show()

    def flightMenuSelected(self,checked):
        SwitchWindows.openFlightWindow(self)

    def airportMenuSelected(self,checked):
        SwitchWindows.openAirportWindow(self)
    
    def passengerMenuSelected(self,checked):
        SwitchWindows.openPassengerWindow(self)

    def backtoLogin(self,checked):
        SwitchWindows.openLoginWindow(self)


#Flight Class

class viewFlightPassengersWindow(QtWidgets.QMainWindow):
    flightid = ""
    def __init__(self,flightidfrommain):
        self.flightid = flightidfrommain
        super(viewFlightPassengersWindow,self).__init__()
        uic.loadUi(path + "//UI//viewflightpassengers.ui",self)
        self.loadPassengerData()
    def loadPassengerData(self):
        tablerow = 0
        mycursor.execute("select t.TicketNumber,t.PassportNumber,p.FirstName,t.Class,t.SeatNumber,t.Disability from ticket t join passengers p on t.PassportNumber = p.PassportNumber where t.FlightID = " + "'"+  self.flightid + "'")
        passresult = mycursor.fetchall()
        global maxRows
        maxRows = 10
        self.tablePassengerFlight.setRowCount(maxRows)
        for row in passresult:
            for i in range(6):
                self.tablePassengerFlight.setItem(tablerow,i,QtWidgets.QTableWidgetItem(row[i]))
                maxRows = maxRows+1
            tablerow = tablerow+1

class viewMealServedWindow(QtWidgets.QMainWindow):
    flightid = ""
    def __init__(self,flightidfrommain):
        self.flightid = flightidfrommain
        super(viewMealServedWindow,self).__init__()
        uic.loadUi(path + "//UI//viewflightmeals.ui",self)
        self.loadMealData()
    def loadMealData(self):
        tablerow = 0
        mycursor.execute('select  seatnumber,firstname,MealName,hALAL,Vegetarian,FoodManufacturer from passengers natural join ticket natural join mealforticket natural join mealinfo where flightid = "'+self.flightid+'";')
        Mealresult = mycursor.fetchall()
        maxRows = 10
        self.tableMealFlight.setRowCount(maxRows)
        for row in Mealresult:
            for i in range(6):
                self.tableMealFlight.setItem(tablerow,i,QtWidgets.QTableWidgetItem(row[i]))
                maxRows = maxRows+1
            tablerow = tablerow+1

class viewCrewMemberWindow(QtWidgets.QMainWindow):
    flightid = ""
    def __init__(self,flightidfrommain):
        self.flightid = flightidfrommain
        super(viewCrewMemberWindow,self).__init__()
        uic.loadUi(path + "//UI//viewflightcrewmembers.ui",self)

        self.loadCrewData()
    
    def loadCrewData(self):
        tablerow = 0
        mycursor.execute('select crewid,name,DateOfBirth,designation,WorksForAirlineIATA,origin from crewmembers natural join crewonflight where flightid = "'+ self.flightid + '";')
        crewresult = mycursor.fetchall()
        maxRows = 10
        self.tableCrewFlight.setRowCount(maxRows)
        for row in crewresult:
            for i in range(6):
                self.tableCrewFlight.setItem(tablerow,i,QtWidgets.QTableWidgetItem(row[i]))
                maxRows = maxRows+1
            tablerow = tablerow+1

class FlightWindow(QtWidgets.QMainWindow):
    flightid = ""
    def __init__(self):
        super(FlightWindow,self).__init__()
        uic.loadUi(path + "//UI//flightdetails.ui",self)

        self.actionPassenger_Details_2.triggered.connect(self.passengerMenuSelected)
        self.actionAircraft_Details_2.triggered.connect(self.aircraftMenuSelected)
        self.actionAirport_Details_2.triggered.connect(self.airportMenuSelected)

        self.actionAdmin_Logout.triggered.connect(self.backtoLogin)

        self.flightnumberinput.editingFinished.connect(self.entersFlight)

        #buttonsFunctionality
        self.ViewPassengers.clicked.connect(self.viewFlightPassengers)
        self.ViewMealServed.clicked.connect(self.viewFlightMeal)
        self.ViewFlightCrew.clicked.connect(self.viewCrewMembers)

    def entersFlight(self):
        self.flightid = self.flightnumberinput.text()
        cursor.execute('select * from flight where flightid = "'+self.flightid+'";')
        res = cursor.fetchall()
        if res == []:
            return
        tup = ViewFlightRecord(self.flightid)
        print(tup)
        self.Airline.setText("Airline: " + tup[0][1])
        if tup[1] == 'a':
            prnt = "Estimated Time of Arrival: " + tup[0][2]
            strng = "From: " + tup[0][3]
        else:
            prnt = "Estimated Time of Departure: " + tup[0][2]
            strng = "To: " + tup[0][3]
        self.EstimatedTime.setText(prnt)
        self.FromTo.setText(strng)
        lugg = FetchLuggageCount(self.flightid)
        self.luggageCount.setText("Number of Luggage Bags: " + str(lugg))
        banday = FetchPassengerOnFlightCount(self.flightid)
        self.passengerCount.setText("Number of Passengers: " + str(banday))

    def viewFlightPassengers(self,checked):
        self.viewPassengersonPlane = viewFlightPassengersWindow(self.flightid)
        self.viewPassengersonPlane.show()

    def viewFlightMeal(self,checked):
        self.viewMealsonPlane = viewMealServedWindow(self.flightid)
        self.viewMealsonPlane.show()

    def viewCrewMembers(self,checked):
        self.viewCrewOnPlane = viewCrewMemberWindow(self.flightid)
        self.viewCrewOnPlane.show()

    def passengerMenuSelected(self,checked):
        SwitchWindows.openPassengerWindow(self)

    def airportMenuSelected(self,checked):
        SwitchWindows.openAirportWindow(self)
    
    def aircraftMenuSelected(self,checked):
        SwitchWindows.openAircraftWindow(self)

    def backtoLogin(self,checked):
        SwitchWindows.openLoginWindow(self)


#Passenger Class

class ViewLuggageWindow(QtWidgets.QMainWindow):
    passportNo = ""
    def __init__(self,passportNofrommain):
        self.passportNo = passportNofrommain
        super(ViewLuggageWindow,self).__init__()
        uic.loadUi(path+ "//UI//viewluggage.ui",self)
        self.luggagedata()

    def luggagedata(self):
        cursor.callproc('SelectPassengerLuggage',[self.passportNo])
        res = cursor.stored_results()
        for x in res:
            y = x.fetchall()
        info = y[0]
        self.TicketNo.setText("Ticket Number: "+info[0])
        self.NumberofPieces.setText("Number of Pieces: "+str(info[1]))
        self.Weight.setText("Total Weight(kg): "+str(info[2]))
        self.ExcessLuggageCost.setText("Excess Luggage Cost($): "+str(info[3]))

class UpdatePassenger(QtWidgets.QMainWindow):
     def __init__(self):
        super(UpdatePassenger,self).__init__()
        uic.loadUi(path + "//UI//updatepassenger.ui",self)
        self.emailcheckbox.toggled.connect(self.EmailCheckBoxToggled)
        self.contactcheckbox.toggled.connect(self.ContactCheckBoxToggled)
        self.updatePassengerButton.clicked.connect(self.updateButtonPressed)
     
     def allfilled(self):
        if self.updatepassportinput.text() == "":
            return False
        if self.emailcheckbox.isChecked():
            if self.emailtextbox.text() == "":
                return False
        if self.contactcheckbox.isChecked():
            if self.contacttextbox.text() == "":
                return False
        if (not self.emailcheckbox.isChecked()) and (not self.contactcheckbox.isChecked()):
            return False
        return True

     def updateButtonPressed(self):
        if self.allfilled():
            NewEmail = ""
            NewPhone = ""
            if self.emailcheckbox.isChecked():
                NewEmail = self.emailtextbox.text()
            if self.contactcheckbox.isChecked():
                NewPhone = self.phonetextbox.text()

            UpdatePassengerRecord(self.updatepassportinput.text(),NewPhone,NewEmail)
            self.close()
        else:
            
            self.dialog = infoDialog()
            self.dialog.show()
            

     def EmailCheckBoxToggled(self):
        if self.emailcheckbox.isChecked():
            self.emailtextbox.setEnabled(True)
        else:
            self.emailtextbox.setEnabled(False)

     def ContactCheckBoxToggled(self):
        if self.contactcheckbox.isChecked():
            self.contacttextbox.setEnabled(True)
        else:
            self.contacttextbox.setEnabled(False)
    

class DeletePassenger(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(DeletePassenger,self).__init__()
        uic.loadUi(path + "//UI//deletepassenger.ui",self)
        self.deletePassengerButton.clicked.connect(self.deletebuttonpressed)

    def deletebuttonpressed(self):
        if self.deletePassportInput.text() != "":
            passportNo = self.deletePassportInput.text()
            DeletePassengerRecord(passportNo)
            
            self.close()
        else:
            self.dialog = infoDialog()
            self.dialog.show()

            

class InsertNewPassengerDetails(QtWidgets.QMainWindow):
    def __init__(self):
        super(InsertNewPassengerDetails,self).__init__()
        uic.loadUi(path + "//UI//insertnewpassenger.ui",self)

        options = ["Male","Female","Other"]
        for option in options:
            self.comboGenderBox.addItem(option)

        options = []
        cursor.execute("select distinct(BasedInCity) from airport join departures where airport.airportiata = departures.departureairportiata")
        result = cursor.fetchall()

        for x in result:
            for y in x:
                self.jouneryCombobox.addItem(y)

        

        self.Save.clicked.connect(self.saveButtonclicked)
        self.hasluggagecheckbox.toggled.connect(self.luggagecheckboxtoggled)
        

    def luggagecheckboxtoggled(self):
        if self.hasluggagecheckbox.isChecked():
            self.Insertnumberofbags.setEnabled(True)
            self.InsertWeight.setEnabled(True)
            self.Insertextraluggagecost.setEnabled(True)
        else:
            self.Insertnumberofbags.setEnabled(False)
            self.InsertWeight.setEnabled(False)
            self.Insertextraluggagecost.setEnabled(False)

    def allfilled(self):
        if self.InsertPassportNumber.text() == "":
            return False
        if self.InsertFname.text() == "":
            return False
        if self.InsertLname.text() == "":
            return False
        if self.comboGenderBox.currentText() == "":
            return False
        if self.InsertCity.text() == "":
            return False
        if self.InsertCountry.text() == "":
            return False
        if self.InsertEmail.text() == "":
            return False
        if self.InsertPhoneNumber.text() == "":
            return False
        if self.InsertTicketNumber.text() == "":
            return False
        if self.jouneryCombobox.currentText() == "":
            return False
        if self.InsertClass.text() == "":
            return False
        if self.InsertDisability.text() == "":
            return False
        if self.InsertSeatNumber.text() == "":
            return False
        if self.InsertSeatNumber.text() == "":
            return False
        if self.hasluggagecheckbox.isChecked():
            if self.Insertnumberofbags.text() == "":
                return False
            if self.InsertWeight.text() == "":
                return False
            if self.Insertextraluggagecost.text() == "":
                return False
        return True

    def saveButtonclicked(self,checked):
        if self.allfilled():
            self.newPassenger =[]
            self.newPassenger.append(self.InsertPassportNumber.text())
            self.newPassenger.append(self.InsertFname.text())
            self.newPassenger.append(self.InsertLname.text())

            datelist = str(self.dateEdit.date()).split(',')
            day = datelist[2][1:-1]
            month = datelist[1][1:]
            year = datelist[0][19:]
            date = month +"/"+day+ "/" + year

            self.newPassenger.append(date)
            self.newPassenger.append(self.comboGenderBox.currentText())
            self.newPassenger.append(self.InsertCity.text())
            self.newPassenger.append(self.InsertCountry.text())
            self.newPassenger.append(self.InsertEmail.text())
            self.newPassenger.append(self.InsertPhoneNumber.text())  
            self.newPassenger.append(self.InsertTicketNumber.text()) 

            cursor.execute('select flightid from departures where departureairportiata in(select airportiata from airport where basedincity ="'+self.jouneryCombobox.currentText()+'" )')  
            res = cursor.fetchall()
            x = res[0][0]
            self.newPassenger.append(x)


            self.newPassenger.append(self.InsertClass.text())   
            self.newPassenger.append(self.InsertDisability.text())   
            self.newPassenger.append(self.InsertSeatNumber.text())

            if (self.hasluggagecheckbox.isChecked()):
                self.newPassenger.append(self.Insertnumberofbags.text())
                self.newPassenger.append(self.InsertWeight.text())
                self.newPassenger.append(self.Insertextraluggagecost.text())
            
            InsertPassengerRecord(self.newPassenger)

            self.close()

        else:
            self.dialogbox = infoDialog()
            self.dialogbox.show()
        
class infoDialog(QtWidgets.QDialog):
    def __init__(self):
        super(infoDialog,self).__init__()
        uic.loadUi(path + "//UI//infoDialog.ui",self)
        self.retrybutton.clicked.connect(self.retry_pressed)

    def retry_pressed(self,checked):
        self.close()

class PassengerWindow(QtWidgets.QMainWindow):
    passportNo = ""
    def __init__(self):
        super(PassengerWindow,self).__init__()
        uic.loadUi(path + "\\UI\\passengerdetails.ui",self)

        self.actionFlight_Details.triggered.connect(self.flightMenuSelected)
        self.actionAircraft_Details_2.triggered.connect(self.aircraftMenuSelected)
        self.actionAirport_Details_2.triggered.connect(self.airportMenuSelected)

        self.actionInsert_New_Record_s.triggered.connect(self.insertNewPassengerRecord)

        self.actionUpdate_Existing_Record_s.triggered.connect(self.updatePassengerRecord)

        self.actionDelete_Record_s_.triggered.connect(self.deletePassengerRecord)

        self.actionAdmin_Logout.triggered.connect(self.backtoLogin)
        

        self.inputPassport = self.findChild(QtWidgets.QLineEdit,"PassportInput")
        self.inputPassport.editingFinished.connect(self.entersPassport)
        

        self.ViewLuggage = self.findChild(QtWidgets.QPushButton,"ViewLuggage")
        self.ViewLuggage.clicked.connect(self.ViewLuggageDetails)
        
        self.GenerateTicket.clicked.connect(self.GenerateTicketFunction)
    

    def ViewLuggageDetails(self,checked):
        self.ViewLuggage = ViewLuggageWindow(self.passportNo)
        self.ViewLuggage.show()
    
    def GenerateTicketFunction(self):
        self.dialog = ticketDialog()
        self.dialog.show()
        ticket = ticketmaker(self.passportNo)
        ticket.makepdf()
        self.dialog.setWindowTitle("DONE")

    def entersPassport(self):
        self.passportNo = self.inputPassport.text()
        tup = ViewPassengerRecord(self.passportNo)
        self.Name.setText("Name: "+ tup[0] + " " + tup[1])
        self.Gender.setText("Gender: "+ tup[3])
        self.dateOfBirth.setText("Date of Birth: "+ tup[2])
        self.Country.setText("Country: "+ tup[4])
        self.City.setText("City: "+ tup[5])
        self.PhoneNumber.setText("Phone Number: "+ tup[6])
        self.EmailAddress.setText("Email Address: "+ tup[7])

    def flightMenuSelected(self,checked):
        SwitchWindows.openFlightWindow(self)

    def airportMenuSelected(self,checked):
        SwitchWindows.openAirportWindow(self)
    
    def aircraftMenuSelected(self,checked):
        SwitchWindows.openAircraftWindow(self)

    def backtoLogin(self,checked):
        SwitchWindows.openLoginWindow(self)

    def insertNewPassengerRecord(self,checked):
        self.newPassenger = InsertNewPassengerDetails()
        self.newPassenger.show()

    def deletePassengerRecord(self,checked):
        self.deletePassenger = DeletePassenger()
        self.deletePassenger.show()
    
    def updatePassengerRecord(self,checked):
        self.updatePassenger = UpdatePassenger()
        self.updatePassenger.show()


# MAIN MENU CLASS

class MainMenu(QtWidgets.QMainWindow):
    def __init__(self,adminfrommain,guestuser):
        self.admin= adminfrommain
        self.guestuser = guestuser

        global usertype
        usertype = guestuser

        super(MainMenu,self).__init__()
        uic.loadUi(path + "//UI//mainmenu.ui",self)

        self.passengerButton = self.findChild(QtWidgets.QPushButton,"PassengerDetails_2")
        self.flightButton = self.findChild(QtWidgets.QPushButton,"FlightDetails_2")
        self.aircraftButton = self.findChild(QtWidgets.QPushButton,"AircraftDetails_2")
        self.airportButton = self.findChild(QtWidgets.QPushButton,"AirportDetails_2")

        self.passengerButton.clicked.connect(self.passengerButtonPressed)
        self.flightButton.clicked.connect(self.flightButtonPressed)
        self.aircraftButton.clicked.connect(self.aircraftButtonPressed)
        self.airportButton.clicked.connect(self.airportButtonPressed)

        self.adminname.setText("Admin: " + self.admin)

    def passengerButtonPressed(self,checked):
        SwitchWindows.openPassengerWindow(self)

    def flightButtonPressed(self,checked):
        SwitchWindows.openFlightWindow(self)

    def airportButtonPressed(self,checked):
        SwitchWindows.openAirportWindow(self)

    def aircraftButtonPressed(self,checked):
        SwitchWindows.openAircraftWindow(self)


#LOGIN CLASS

class LoginWindow(QtWidgets.QMainWindow):
    adminname = "Guest"
    def __init__(self):
        super(LoginWindow,self).__init__()
        uic.loadUi(path + "//UI//loginwindow.ui",self)

        self.username = self.findChild(QtWidgets.QLineEdit,"username")
        self.password = self.findChild(QtWidgets.QLineEdit,"password")

        self.button = self.findChild(QtWidgets.QPushButton,"Login")
        self.button.clicked.connect(self.loginPressed)

        self.guest.clicked.connect(self.guestpressed)

    def guestpressed(self,checked):
        self.mainmenu = MainMenu(self.adminname,True)
        self.mainmenu.show()
        self.mainmenu.passengerButton.setEnabled(False)
        # self.mainmenu.airportButton.setEnabled(False)
        # self.mainmenu.aircraftButton.setEnabled(False)
        self.mainmenu.flightButton.setEnabled(False)
        self.close()

    def loginPressed(self,checked):

        username = self.username.text()
        password = self.password.text()

        mycursor.execute("select * from admin_user")
        myresult = mycursor.fetchall()
        authenticated = False
        
        for x in myresult:
            if (x[0] == username) and (x[1] == password):
                authenticated = True
                self.adminname = x[2]
                break
        
        if (authenticated):
            self.mainmenu = MainMenu(self.adminname,False)
            self.mainmenu.show()
            self.close()
        else:
            self.wrongpassword = WrongPasswordDialog()
            self.wrongpassword.show()

class WrongPasswordDialog(QtWidgets.QDialog):
    def __init__(self):
        super(WrongPasswordDialog,self).__init__()
        uic.loadUi(path + "//UI//dialogwrongpassword.ui",self)
        self.retrybutton.clicked.connect(self.retry_pressed)

    def retry_pressed(self,checked):
        self.close()





#MAIN
global mydb 
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="fruity",
database = "airportproject"
)

global mycursor
mycursor = mydb.cursor()

app = QtWidgets.QApplication(sys.argv)
window = LoginWindow()
window.show()
app.exec_()