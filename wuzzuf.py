## 1th import module  

import requests
from bs4 import BeautifulSoup
import csv 
from itertools import zip_longest
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriver, ChromeDriverManager
from selenium import webdriver

job_title = []
company_name = []
location_name = []
job_skill = [] 
links = []
salary = []
responsibilities = []
date = []
page_num = 0


while True:
    try:
        ## 2th step use requests to fetch the url
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")

        ## 3th step save contant/markup
        src = result.content

        ## 4th step create soup object to parse content 
        soup = BeautifulSoup(src, "lxml")

        page_limit = int(soup.find("strong").text)
        page_limit = 5

        if (page_num > page_limit // 15): # // intger divition 16.5 ~ 16
            print ("pages ended")
            break

        ## 5th step find the elements containing info we need 
        job_titles = soup.find_all("h2",{"class":"css-m604qf"})
        company_names = soup.find_all("a",{"class":"css-17s97q8"})
        locations_names = soup.find_all("span",{"class":"css-5wys0k"})
        job_skills = soup.find_all("div",{"class":"css-y4udm8"})
        posted_new = soup.find_all("div", {"class":"css-4c4ojb"})
        posted_old = soup.find_all("div", {"class":"css-do6t5g"})
        posted = [*posted_new, *posted_old] # * for unpaking 

        ## 6th step loob over returned lists to extract needed info into other lists
        for i in range (len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs["href"])
            company_name.append(company_names[i].text)
            location_name.append(locations_names[i].text)
            job_skill.append(job_skills[i].text)
            date_text = posted[i].text.replace("-", "").strip()
            date.append(date_text)

        page_num += 1
        print ("page switched")

    except:
        print ("error occured")
        break


for link in links:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(link)

    page = driver.page_source
    soup = BeautifulSoup(page, "lxml")

    salaries_div = soup.find_all("div",{"class":"css-rcl8e5"})
    sal = salaries_div[3].select_one("span.css-4xky9y").text
    salary.append(sal)
    requirements = soup.find("div",{"class":"css-1t5f0fr"}).ul 
    respon_text = ""
    for li in requirements.find_all("li"):
        respon_text += li.text + "| "
    respon_text = respon_text[ : -2]
    responsibilities.append(respon_text)
    driver.quit()
    


## 7th step create csv file and fill it with values
file_list = [job_title, company_name, date, location_name, job_skill, links, salary, responsibilities]
exported = zip_longest(*file_list)

with open ("wuzzuf.csv","w") as myfile:
    wr  = csv.writer(myfile)
    wr.writerow(["job title", "company name", "date", "location", "skills", "link", "salary", "responsibilities"])
    wr.writerows(exported)

print ("Done!")