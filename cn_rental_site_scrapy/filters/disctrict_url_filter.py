import csv

# in_names_file = 'Entire China_GADM Level 3 & GADM - gadm36_CHN_3.csv'
in_names_file = 'district_result1.csv'
out_names_file = "district_result_filtered.csv"

out_rows = []

fieldnames = ["disctrictname", "link"]

with open(in_names_file, encoding="utf8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['districname'] != '不限' and row['districname'] != '其他':
            new_row = {}
            new_row['disctrictname'] = row['districname']
            new_row['link'] = 'http:' + row['link']
            out_rows.append(new_row)

with open(out_names_file, 'w', encoding='utf8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in out_rows:
        writer.writerow(row)