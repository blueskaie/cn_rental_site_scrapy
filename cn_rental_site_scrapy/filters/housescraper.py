from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import csv
import re
import time

# function for getting text of any element
def get_element_text(element=''):
    if element is None:
        return "None"
    else:
        return element.getText() 


class housesscraper:

    housetypes = ['1', '2', '3', 'Studio']
    out_fieldnames = ["NAME0", "NAME1", "NAME1_pinyin","NAME2", "NAME2_pinyin", "NAME3","LINK","BEDROOMS","PRICE","COUNT"]    
    result = {} #'type' 'price' 'count' 
    log_file = None
    curr_url = None
    out_file = None
    writer = None
    curr_distric_info = None
    distric_info_array = []
    def __init__(self):
        print("This is matrixscraper created by isopooh")
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.PhantomJS()
        self.log_file = open('log.txt','a')
        with open('finallresult.csv', 'w') as self.out_file:
            writer = csv.DictWriter(self.out_file, fieldnames=self.out_fieldnames)
            writer.writeheader()

    def reset_result(self):
        for item in self.housetypes:
            self.result[item] = {}
            self.result[item]['totalprice'] = 0
            self.result[item]['count'] = 0            

    def get_browser(self):
        return self.browser

    def stop_browser(self):
        self.browser.close()

    def log(self, note):
        self.log_file.write(note + '\n')

    #========================================================
    # store the result into csv file
    #========================================================    
    def store_csv(self, result):
        try:
            with open('finallresult.csv', 'a', encoding="utf8") as self.out_file:
                writer = csv.DictWriter(self.out_file, fieldnames=self.out_fieldnames)        
                for item in self.housetypes:
                    out = {}
                    if result[item]['count'] == 0:
                        avg_price = 0
                    else:
                        avg_price = result[item]['totalprice'] / result[item]['count']
                    out['NAME0'] = self.curr_distric_info['NAME0']
                    out['NAME1'] = self.curr_distric_info['NAME1']
                    out['NAME1_pinyin'] = self.curr_distric_info['NAME1_pinyin']
                    out['NAME2'] = self.curr_distric_info['NAME2']
                    out['NAME2_pinyin'] = self.curr_distric_info['NAME2_pinyin']
                    out['NAME3'] = self.curr_distric_info['NAME3']
                    out['LINK'] = self.curr_url
                    out['BEDROOMS'] = item
                    out['PRICE'] = avg_price
                    out['COUNT'] = result[item]['count']
                    writer.writerow(out)
                return True
            return False
        except:
            self.log(self.curr_url+":SaveError")

    def initurls(self):
        print("Getting URLS...")
        url_source_file = "result/mytemplate.csv"
        with open(url_source_file, encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.distric_info_array.append(row)
        return True

    def producturl(self, url):
        try:
            if url.split(":")[0] != 'http':
                url = "http:"+url
            return url
        except:
            self.log(self.curr_url+":ProductURLError")
    # =====================================================
    # Main code : Start to scrape
    # =====================================================    
    def getdistrictinfo(self, url):
        # try:
            try: 
                self.browser.get(url)
            except TimeoutException:
                self.log(url+":TimeoutError")
                return True
            page = BeautifulSoup(self.browser.page_source, "html5lib")
            styles = [
                ["houseList_item_in clearfix","house_info clearfix","price"],
                ["grid-s5m0e5-in ","house-info","one"],
                ["grid-s5m0e5-in ","house-info txt-cut","one"]
                ]
            for style in styles:
                houselist = page.findAll("div", {"class":style[0]})
                if houselist:
                    for house in houselist:
                        house_property = house.find("div",{"class":"col-main"}).find("div",{"class":style[1]}).find("span")
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

                        self.result[house_property]['totalprice'] = self.result[house_property]['totalprice'] + price
                        self.result[house_property]['count'] = self.result[house_property]['count'] + 1
                        print(house_property+":"+str(price))
                        # print(self.result)
            # nextpagination=WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH,'//a[@class="next"]')))
            try:
                nextpagination = page.find("div",{"class":"p"}).find("div",{"class":"page"}).find("a", {"class":"next"})
                if nextpagination:
                    nexturl = self.producturl(nextpagination['href'])            
                    print(nexturl)
                    self.getdistrictinfo(nexturl)
            except:
                self.log(url+":NextButton")
                pass

        # except:
        #     self.log(url+":UnknownError")
        #     pass


    # =====================================================
    # Main code : Start to scrape
    # =====================================================    
    def getpropertyinfo(self, url):
        # try:
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
                    for house in houselist:
                        house_property = house.find("div",{"class":"col-main"}).find("div",{"class":style[1]}).find("span")
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

                        link = house.find("*",{"class":style[4]}).find("a")
                        if link:
                            link = self.producturl(link['href'])
                        else:
                            link = "None"

                        print(link+":"+house_property+":"+str(price))
                        # print(self.result)
            # nextpagination=WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH,'//a[@class="next"]')))
            try:
                nextpagination = page.find("div",{"class":"p"}).find("div",{"class":"page"}).find("a", {"class":"next"})
                if nextpagination:
                    nexturl = self.producturl(nextpagination['href'])            
                    print(nexturl)
                    self.getdistrictinfo(nexturl)
            except:
                self.log(url+":NextButton")
                pass

        # except:
        #     self.log(url+":UnknownError")
        #     pass



    # =====================================================
    # Main code : Start to crawl
    # =====================================================     
    def run_parser(self):
        print("Start to run parser...")
        print(self.result)
        for district in self.distric_info_array:
            self.curr_url = district['LINK']
            print("Scrapying about "+self.curr_url)
            self.curr_distric_info = district
            self.reset_result()
            self.getdistrictinfo(self.curr_url)
            print(self.result)
            self.store_csv(self.result)
            
def main():
    s = housesscraper()
    s.initurls()
    s.run_parser()

if __name__ == "__main__":
    main()