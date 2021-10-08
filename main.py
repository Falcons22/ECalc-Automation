from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd
import csv
from check import thrust_at_750
 
USERNAME = "falconsofficial@gmail.com"
PASSWORD = "lg7x6ie"
propeller_range = list(range(18, 24))  # in inches
pitch_range = list(range(8, 15))
blade_range = list(range(2,4))
 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
 
driver = webdriver.Chrome(options=chrome_options)
 
 
def login():
    driver.get(
        "https://www.ecalc.ch/calcmember/login.php?https://www.ecalc.ch/calcmember/signup.php")
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    submit = driver.find_element_by_id("myButton")
    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    alert = Alert(driver)
    submit.send_keys(Keys.RETURN)
    sleep(1)
    alert.accept()
    print("Logged in using Falcons id")
 
 
login()
driver.get("https://www.ecalc.ch/motorcalc.php")
sleep(3)
 
 
modelweight = driver.find_element_by_id("inGWeight")
for i in range(3):
    modelweight.send_keys(Keys.BACKSPACE)
modelweight.send_keys('18000')
 
wingspan = driver.find_element_by_id("inGWingSpan")
for i in range(4):
    wingspan.send_keys(Keys.BACKSPACE)
wingspan.send_keys('2540')
 
wingarea = driver.find_element_by_id("inGWingArea")
for i in range(2):
    wingarea.send_keys(Keys.BACKSPACE)
wingarea.send_keys('210')
 
fieldelevation = driver.find_element_by_id("inGElevation")
for i in range(3):
    fieldelevation.send_keys(Keys.BACKSPACE)
fieldelevation.send_keys('199')
 
batterytype = driver.find_element_by_id("inBCell")
batteryfile = open('battery.txt')
batterylist = batteryfile.read().split('\n')
 
batteryconfig = driver.find_element_by_id("inBS")
for i in range(1):
    batteryconfig.send_keys(Keys.BACKSPACE)
batteryconfig.send_keys('6')
 
esctype = driver.find_element_by_id("inEType")
esctype.send_keys('max 120A')
 
batteryextensionwire = driver.find_element_by_id("inEBatLength")
batteryextensionwire.send_keys(Keys.BACKSPACE)
batteryextensionwire.send_keys('150')
 
motorextensionwire = driver.find_element_by_id("inEMotLength")
motorextensionwire.send_keys(Keys.BACKSPACE)
motorextensionwire.send_keys('50')
 
motormanufacturer = driver.find_element_by_id("inMManufacturer")
 
motorcooling = driver.find_element_by_id("inGMotorCooling")
motorcooling.send_keys("good")
 
motortype = driver.find_element_by_id("inMType")
 
 
proptype = driver.find_element_by_id("inPType")
proptype.send_keys("APC Electric E")
propdiameter = driver.find_element_by_id("inPDiameter")
proppitch = driver.find_element_by_id("inPPitch")
flightspeed = driver.find_element_by_id("inPSpeed")
flightspeed.send_keys(Keys.BACKSPACE)
flightspeed.send_keys("47.8")
bladeCount=driver.find_element_by_id("inPBlades") 



motorlist = []
with open('prop1.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        motorlist.append((row[0], row[1]))
 
 
list_header = ['Propeller','Throttle','Current (DC)','Voltage (DC)','el. Power','Efficiency','Thrust','Spec. Thrust','Pitch Speed','Speed (level)','Motor Run Time']
sleep(2) 
for motor in motorlist:
    data = []
    motormanufacturer.send_keys(motor[0])
    motortype.send_keys(motor[1])
    motortype.send_keys(Keys.RETURN)
    for battery in batterylist:
        batterytype.send_keys(battery)
        for diameter in propeller_range:
            propdiametercurrvalue = propdiameter.get_attribute('value')
            for i in range(len(propdiametercurrvalue)):
                propdiameter.send_keys(Keys.BACKSPACE)
            propdiameter.send_keys(str(diameter))
            for pitch in pitch_range:
                for blade in blade_range:
                    bladeCount.send_keys(Keys.BACKSPACE)
                    bladeCount.send_keys(str(blade))
                    data = []
                    proppitchcurrvalue = proppitch.get_attribute('value')
                    for i in range(len(proppitchcurrvalue)):
                        proppitch.send_keys(Keys.BACKSPACE)
                    proppitch.send_keys(str(pitch))
                    calculatebtn = driver.find_element_by_name('btnCalculate')
                    calculatebtn.send_keys(Keys.RETURN)
                    sleep(0.25)
                    with open("tmp.html", "w") as f:
                        f.write(driver.page_source.encode('utf-8').decode('ascii', 'ignore'))
                    with open("tmp.html") as f:
                        soup = BeautifulSoup(f, 'html.parser')
                        html = soup.find('table', {'id': 'rpmTable'}).find_all("tr")[2:]
                        for element in html:
                            sub_data = []
                            for sub_element in element:
                                try:
                                    sub_data.append(sub_element.get_text())
                                except:
                                    continue
                            del sub_data[7]
                            del sub_data[8]
                            del sub_data[9]
                            del sub_data[10]
                            data.append(sub_data)
                    batteryname='-'.join(battery.split('/'))      
                    dataFrame = pd.DataFrame(data = data, columns = list_header)
                    thrust = thrust_at_750(dataFrame)
                    thrust_to_weight=thrust/18000
                    if(thrust_to_weight<0.28):
                        print(f'Rejected: results/{motor[1]}_{batteryname}_{diameter}_{pitch}_{blade}.csv, thrust={thrust}, t:w={thrust_to_weight}')
                    else:
                        print(f'Accepted: results/{motor[1]}_{batteryname}_{diameter}_{pitch}_{blade}.csv, thrust={thrust}, t:w={thrust_to_weight}')
                        dataFrame.to_csv(f'results/{motor[1]}_{batteryname}_{diameter}_{pitch}_{blade}.csv')
                
                
 
sleep(10)
driver.quit()
