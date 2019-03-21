from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time

userid = 'ajayrathore80069@yahoo.com'
password = 'xxxxxxxxxxxx'

driver = webdriver.Firefox()


def login():
    driver.get('https://linkedin.com')
    driver.find_element_by_xpath("""//*[@id="login-email"]""").send_keys(userid)
    driver.find_element_by_xpath("""//*[@id="login-password"]""").send_keys(password)
    driver.find_element_by_xpath("""//*[@id="login-submit"]""").click()


def getCsv(filename):
    companylist = []
    with open(filename) as com_nam:
        csvreader = csv.reader(com_nam)
        for row in csvreader:
            companylist.append((row[0],row[1]))
    return companylist

def openCompany(name,link):
    print('fetching : ',name)
    driver.get(link)
    time.sleep(5)
    try:
        elem = driver.find_element_by_xpath("//a[@data-control-name='topcard_see_all_employees']")
        employee_list_href = elem.get_attribute('href')
        saveLink(name,employee_list_href)
    except:
        print("no employees found in : ",name)

def saveLink(name,link):
    with open('employee_link.csv','a') as emp_lin_ls:
        csvwriter = csv.writer(emp_lin_ls)
        csvwriter.writerow([name,link])

def fetchAllEmployeeListLink():
    for i in getCsv()[1:]:
        openCompany(i[0],i[1])

def retrieveAll(name,elem1,elem2,elem3):
    with open('./employee_det.csv','a') as emp_ls:
        csvwriter = csv.writer(emp_ls)
        for i,k in enumerate(elem1):
            print(elem3[i])
            csvwriter.writerow([name,elem1[i].text,elem2[i].text,elem3[i].text])
def fetchAllEmployee(name,link):
    i =1
    while(1):
        try:
            fetchPage(name,link,i)
            i=i+1
        except:
            print('No results')
            break

def fetchPage(name,link,i):
    driver.get(link+'&page='+str(i))
    time.sleep(5)
    #check for no more results
    elem1 = driver.find_elements_by_xpath("//li[@class='search-result search-result__occluded-item ember-view']//p[@class='subline-level-1 t-14 t-black t-normal search-result__truncate']")
    elem2 = driver.find_elements_by_xpath("//li[@class='search-result search-result__occluded-item ember-view']//p[@class='subline-level-2 t-12 t-black--light t-normal search-result__truncate']")
    elem3 = driver.find_elements_by_xpath("//li[@class='search-result search-result__occluded-item ember-view']//a")
    if(len(elem1) is 0):
        raise ValueError('No more results')
    retrieveAll(name,elem1,elem2,elem3)
    #print(elem1)

def organiseData():
    company_list={}
    with open('./company_name.csv') as emp_det:
        csvreader = csv.reader(emp_det)
        for row in csvreader:
            company_list.setdefault(row[0],row[1])
    employee_det=[]
    with open('./employee_det.csv') as emp_det:
        csvreader = csv.reader(emp_det)
        for row in csvreader:
            employee_det.append((row[0],row[1],row[2],row[3]))
    with open('./Data_Format.csv','w') as data:
        csvwriter = csv.writer(data)
        for i in employee_det:
            temp = []
            temp.append(i[0])
            temp.append(company_list[i[0]])
            if i[3] is '' :
                temp.append('Linkedin')
                temp.append('Member')
            else:
                name = i[3].split(' ')
                temp.append(name[0])
                if len(name)>1:
                    temp.append(name[1])
                else:
                    temp.append('')
            temp.append('')
            temp.append(i[1])
            temp.append(i[2])
            csvwriter.writerow(temp)

# Login 
login()
# This will fetch associated employees page links and save them to employee_link.csv
fetchAllEmployeeListLink()
# This will fetch all employees details and save them to employee_det.csv
for i in  getCsv('./employee_link.csv'):
    fetchAllEmployee(i[0],i[1])
# Organise retrieved data in the required format
organiseData()
