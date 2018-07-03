from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import csv
import re
import time

class rental_site_scraper:

    #current_process
    cur_process = None
    
    #log_file
    log_filename = 'log.txt'

    #city_url_relative_vals
    out_city_url_fieldnames = ["link", "cityname", "cityname_pinyin"]
    out_city_url_filename = "city_urls.csv"
    city_urls = []

    #district_url_relative_vals
    out_district_url_fieldnames = ["NAME0", "NAME1", "NAME1_pinyin","NAME2", "NAME2_pinyin", "NAME3","LINK"]    
    out_district_url_filename = "district_urls.csv" 
    district_urls = []

    #district_all_propertys_vals
    out_all_propertys_fieldnames = ["NAME0", "NAME1", "NAME1_pinyin","NAME2", "NAME2_pinyin", "NAME3","BEDROOMS","PRICE","LINK","DESCRIPTION"]    
    out_all_propertys_filename = "all_propertys.csv" 
    
    def __init__(self):
        print("This is rental_site_scraper created by isopooh")
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.PhantomJS()
        self.log_file = open('log.txt','a')

    def log(self, note):
        note = self.cur_process + "," + note + '\n'
        print(note)
        self.log_file.write(note)

    def read_city_urls(self):
        print("read_city_urls")
        self.cur_process = "read_city_url"
        try:
            with open(self.out_city_url_filename, encoding="utf8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.city_urls.append(row)
                f.close()
        except FileNotFoundError:
            self.log("FileNotFoundError")
        except:
            self.log("UnknownError")

    def save_district_urls(self):
        print("save_district_urls")
        self.cur_process = "save_district_urls"
        with open(self.out_district_url_filename, 'w', encoding='utf8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.out_district_url_fieldnames)
            writer.writeheader()
            for row in self.district_urls:
                writer.writerow(row)

    def read_district_urls(self):
        print("read_district_urls")
        self.cur_process = "read_district_urls"
        with open(self.out_district_url_filename, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.district_urls.append(row)
 

    def get_district_urls(self):
        print("get_district_urls")
        self.cur_process = "get_district_urls"
        self.read_city_urls()
        
        for city in self.city_urls:
            url = city['link']
            print(url)
            try:
                self.browser.get(url)
            except TimeoutError:
                self.log(url+':TimeoutError')
            except:
                self.log(url+':UnknownError')
                continue
            citypage = self.browser.page_source
            citypage = BeautifulSoup(citypage, "html5lib")
            
            try:
                districs_element = citypage.find("div",{"class":"dt-line"})
                if districs_element is None:
                    districs_element = citypage.find("div",{"class":"dt_line clearfix"})
                districs_element = districs_element.findAll("a")
                
                for distric in districs_element:
                    if '不限' == distric.getText():
                        continue
                    item = {}
                    item['NAME0'] = "China"
                    item['NAME1'] = city['cityname']
                    item['NAME1_pinyin'] = city['cityname_pinyin']
                    item['NAME2'] = distric.getText()
                    item['NAME2_pinyin'] = "None"
                    item['NAME3'] = "None"
                    item['LINK'] = distric['href']
                    self.district_urls.append(item)
                    # print(item)
            except:
                self.log(url+", UnknownError")
                continue            
        return



    #========================================================
    # store the result into csv file
    #========================================================    
    def save_property_infos(self, property_infos):
        writer = csv.DictWriter(self.outfile, fieldnames=self.out_all_propertys_fieldnames)
        for info in property_infos:
            writer.writerow(info)      
    
    def filter_url(self, url):
        try:
            if url.split(":")[0] != 'http':
                url = "http:"+url
            return url
        except:
            self.log(self.curr_url+":filter_urlError")
    
    def get_property_infos(self, url):
        
        try: 
            self.browser.get(url)
        except TimeoutException:
            self.log(url+":TimeoutError")
            return True
            
        page = BeautifulSoup(self.browser.page_source, "html5lib")
        styles = [
            ["houseList_item_in clearfix","house_info clearfix","price","title_in"],
            ["grid-s5m0e5-in ","house-info","one","house-title"],
            ["grid-s5m0e5-in ","house-info txt-cut","one","house-title"]
        ]
        
        for style in styles:
            houselist = page.findAll("div", {"class":style[0]})
            if houselist:
                properties = []
                for house in houselist:
                    item = {}
                    house_property = house.find("div",{"class":"col-main"}).find("div",{"class":style[1]})
                    if house_property:
                        house_property = house_property.getText()
                        if '室' in house_property:
                            house_property = house_property.split('室')[0][-1]
                            if not house_property in ['1','2','3']:
                                continue
                        else:
                            house_property = "Studio"
                    else:
                        continue

                    price = house.find("div",{"class":"col-extra"}).find("div",{"class":style[2]}).find("span")
                    if price:
                        price = price.getText()
                        price = float(price)
                    else:
                        continue
                    
                    linkstyles = ['div', 'h3']
                    link = None
                    for ls in linkstyles:
                        link = house.find(ls,{"class":style[3]})
                        if link:
                            link = link.find("a")
                            break 
                    des = "None"
                    if link:
                        des = link.getText()
                        link = self.filter_url(link['href'])
                    else:
                        link = "None"
                    
                    item['NAME0'] = self.curr_distric_info['NAME0']
                    item['NAME1'] = self.curr_distric_info['NAME1']
                    item['NAME1_pinyin'] = self.curr_distric_info['NAME1_pinyin']
                    item['NAME2'] = self.curr_distric_info['NAME2']
                    item['NAME2_pinyin'] = self.curr_distric_info['NAME2_pinyin']
                    item['NAME3'] = self.curr_distric_info['NAME3']
                    item['BEDROOMS'] = house_property
                    item['PRICE'] = price
                    item['LINK'] = link
                    item['DESCRIPTION'] = des
                    # print(link+":"+house_property+":"+str(price))
                    properties.append(item)
                self.save_property_infos(properties)
        try:
            nextpagination = page.find("div",{"class":"p"}).find("div",{"class":"page"}).find("a", {"class":"next"})
            if nextpagination:
                nexturl = self.filter_url(nextpagination['href'])            
                print("-----"+nexturl)
                self.get_property_infos(nexturl)
        except:
            self.log(url+":NextButton")
            pass
        return


 
    def filters_property_by_unique_names_and_same_links(self):
        # uniquenames = []    
        links = []   
        # with open("result/new_Entire.csv", encoding="utf8") as f:
        #     reader = csv.DictReader(f)
        #     for row in reader:
        #         uniquenames.append(row['Unique'])
        
        out = open("fitered_all_propertys_by_duplicated_link.csv", 'w',encoding="utf8")
        writer = csv.DictWriter(out, fieldnames=self.out_all_propertys_fieldnames)
        writer.writeheader()
        
        with open("advan_all_propertys.csv", 'r',encoding="utf8") as f:
            reader = csv.DictReader(f)
            i = 0
            for row in reader:
                i = i+1
                if i%1000==0:
                    print(i)
                if row['LINK'] in links:
                    continue
                else:
                    links.append(row['LINK']) 
                # if row['NAME3'] in uniquenames:
                writer.writerow(row)    
        out.close()

    def get_coordinate(self):
        self.cur_process = "get_coordinate"
        out_fieldnames = ["NAME0", "NAME1", "NAME1_pinyin","NAME2", "NAME2_pinyin", "NAME3","BEDROOMS","PRICE","LINK","DESCRIPTION", "LATITUDE", "LONGITUDE"]    
 
        out = open("get_all_propertys_with_location_1_10000.csv", 'w',encoding="utf8")
        writer = csv.DictWriter(out, fieldnames=out_fieldnames)
        writer.writeheader()
        
        with open("fitered_all_propertys_by_duplicated_link_1_10000.csv", 'r',encoding="utf8") as f:
            reader = csv.DictReader(f)
            i = 0
            for row in reader:
                i = i + 1
                if i%50==0:
                    print(i)
                    time.sleep(1)
                try:
                    self.browser.get(row['LINK'])
                except:
                    self.log(row['LINK']+":TimeOutError")
                try:
                    # location = WebDriverWait(self.browser, 1).until(EC.presence_of_element_located((By.ID, "h-address")))
                    location = self.browser.find_element_by_id("h-address")
                    location = location.get_attribute("data-coordinate")
                    location = location.split(",")
                    if location[0]:
                        row['LATITUDE'] = location[0]
                    else:
                        row['LATITUDE'] = "None"
                    if location[1]:
                        row['LONGITUDE'] = location[1]
                    else:
                        row['LONGITUDE'] = "None"
                except TimeoutException:
                    self.log(row['LINK']+":TimeOutError")
                    row['LATITUDE'] = "None"
                    row['LONGITUDE'] = "None"
                except:    
                    row['LATITUDE'] = "None"
                    row['LONGITUDE'] = "None"
                writer.writerow(row)
    # =====================================================
    # Main code : Start to crawl
    # =====================================================     
    def run_parser(self):

        print("Start to run parser...")

        self.outfile = open(self.out_all_propertys_filename, 'w', encoding='utf8')
        writer = csv.DictWriter(self.outfile, fieldnames=self.out_all_propertys_fieldnames)
        writer.writeheader()        
        
        for district in self.district_urls:
            self.curr_url = self.filter_url(district['LINK'])
            print("Scrapying about "+self.curr_url)
            self.curr_distric_info = district
            self.get_property_infos(self.curr_url)

        self.outfile.close()
            

def main():
    s = rental_site_scraper()
    # s.get_district_urls()
    # s.save_district_urls()
    # s.read_district_urls()
    # s.run_parser()
    # s.filters_property_by_unique_names_and_same_links()
    s.get_coordinate()
if __name__ == "__main__":
    main()