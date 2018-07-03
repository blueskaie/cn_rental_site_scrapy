import csv

# in_names_file = 'Entire China_GADM Level 3 & GADM - gadm36_CHN_3.csv'
city_url_file = 'china_rental_scrapy/cityurl.csv'
district_url_file = "district_result_filtered.csv"
district_pinyin_file = "district_name_filtered.csv"
out_file = "mytemplate.csv"


fieldnames = ["NAME0", "NAME1", "NAME1_pinyin", "NAME2", "NAME2_pinyin", "NAME3", "LINK"]

city_urls = []          #link,cityname,cityname_pinyin
district_urls = []      #disctrictname,link
district_pinyins = []   #disctrictname,pinyin
out_rows = []

def get_city_info(link):
    mylink = link.split('/')[2]
    for city in city_urls:
        if mylink == city['link'].split('/')[2]:
            pinyin = city['cityname_pinyin'][0].upper() + city['cityname_pinyin'][1:]
            return [city['cityname'], pinyin]
    return ["None", "None"]

def get_district_name_pinyin(name):
    for item in district_pinyins:
        if name == item['disctrictname']:
            return item['pinyin']
    return "None"

with open(city_url_file, encoding="utf8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_row = {}
        new_row['cityname'] = row['cityname']
        new_row['cityname_pinyin'] = row['cityname_pinyin']
        new_row['link'] = row['link']
        city_urls.append(new_row)

with open(district_pinyin_file, encoding="utf8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_row = {}
        new_row['disctrictname'] = row['disctrictname']
        new_row['pinyin'] = row['pinyin']
        district_pinyins.append(new_row)

with open(district_url_file, encoding="utf8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_row = {}
        new_row['NAME0'] = "China"
        cityinfo = get_city_info(row['link'])                                                               #Country
        new_row['NAME1'] = cityinfo[0]                                            #City_NAME
        new_row['NAME1_pinyin'] = cityinfo[1]                              #City_NAME_PINYIN        
        new_row['NAME2'] = row['disctrictname']                                                  #DistrictName_Pinyin
        new_row['NAME2_pinyin'] = get_district_name_pinyin(row['disctrictname'])                 #DistrictName_Pinyin        
        new_row['NAME3'] = new_row['NAME2_pinyin'] + ', ' + new_row['NAME1_pinyin']
        new_row['LINK'] = row['link']
        
        out_rows.append(new_row)


with open(out_file, 'w', encoding='utf8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in out_rows:
        writer.writerow(row)