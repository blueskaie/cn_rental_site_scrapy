import csv

# in_names_file = 'Entire China_GADM Level 3 & GADM - gadm36_CHN_3.csv'
all_properties_file = "all_propertys.csv"
district_pinyin_file = "district_name_pinyins.csv"
out_file = "advan_all_propertys.csv"

fieldnames = ["NAME0", "NAME1", "NAME1_pinyin", "NAME2", "NAME2_pinyin", "NAME3","BEDROOMS","PRICE","LINK","DESCRIPTION"]    

city_urls = []          #link,cityname,cityname_pinyin
district_urls = []      #disctrictname,link
district_pinyins = []   #disctrictname,pinyin
out_rows = []

def get_district_name_pinyin(name):
    for item in district_pinyins:
        if name == item['disctrictname']:
            return item['pinyin']
    return "None"


with open(district_pinyin_file, encoding="utf8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_row = {}
        new_row['disctrictname'] = row['disctrictname']
        new_row['pinyin'] = row['pinyin']
        district_pinyins.append(new_row)

with open(all_properties_file, encoding="utf8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_row = row
        new_row['NAME1_pinyin'] = new_row['NAME1_pinyin'][0].upper() + new_row['NAME1_pinyin'][1:]
        new_row['NAME2_pinyin'] = get_district_name_pinyin(row['NAME2'])
        new_row['NAME3'] = new_row['NAME2_pinyin'] + ', ' +new_row['NAME1_pinyin']
        out_rows.append(new_row)


with open(out_file, 'w', encoding='utf8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in out_rows:
        writer.writerow(row)