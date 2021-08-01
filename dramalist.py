
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from openpyxl import load_workbook
import csv
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()

page=1
dramaLinks=[]
movieDatas=[]

finalDF=pd.DataFrame(columns=["ID","Title","Released","Episode","ImageLinks","drakorid","Sypnosis","Page"])

while(True):
    driver.get("https://dramacool.fm/released-in-2021.html"+"?page="+str(page))
    
    time.sleep(10)
    year=driver.current_url.split(".html")[0].split("in-")[1].strip()
    imgLinks=driver.find_elements_by_class_name("img")
    if(len(imgLinks)==0):
        break

    for link in imgLinks:
        a=link.get_attribute("href")
        dramaLinks.append([a,page])
    page+=1
ID=1
for drama in dramaLinks:
    driver.get(drama[0])
    
    time.sleep(10)
    
    try:
        imgLink=driver.find_element_by_class_name("img")
        imgLink=imgLink.find_element_by_css_selector("img")
        imgLink=imgLink.get_attribute("src")
    except:
        imgLink=""
    mainDiv=driver.find_element_by_class_name("info")
    
    paras=mainDiv.find_elements_by_css_selector("p")
    
    director=""
    country=""
    status=""
    released=""
    genre=""
    description=""
    
    description=mainDiv.text.split("Description:")[1].split(":")[0].split("\n")[:-1]
    description=" ".join(description).strip()
    
    for para in paras:
        
        
        
        if("Director:" in para.text):
            director=para.text.replace("Director:","").strip()
            
        if("Country:" in para.text):
            country=para.text.replace("Country:","").strip()
       
        if("Status:" in para.text):
            status=para.text.replace("Status:","").strip()
            
        if("Released:" in para.text):
            released=para.text.replace("Released:","").strip()
            
        if("Genre:" in para.text):
            genre=para.text.replace("Genre:","").strip()
       
            
    
    
    title=mainDiv.find_element_by_css_selector("h1").text
    drakorid=""

    words=title.split(" ")
    
    for word in words:
        try:
            int(word[0])
            drakorid+=word
      
        except:
            drakorid+=word[0]
      
    drakorid+=year
    drac=""
    for i in drakorid:
        if(i.isalpha() or i.isdigit()):
            drac+=i
    drac=drac.upper().replace(released+released,released)
    rating=""
    finalDF=finalDF.append(pd.DataFrame([[ID,title,released,status,imgLink,drac,country,drama[1]]],columns=["ID","Title","Released","Episode","ImageLinks","drakorid","Sypnosis","Page"]))
    finalDF.to_excel("MovieDB-2.xlsx",index=False)
    ID+=1    
      