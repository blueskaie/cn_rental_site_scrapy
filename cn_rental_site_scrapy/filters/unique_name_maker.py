import csv

# in_names_file = 'Entire China_GADM Level 3 & GADM - gadm36_CHN_3.csv'
in_names_file = 'Entire China_GADM Level 3 & GADM - gadm36_CHN_3.csv'
out_names_file = "new.csv"

out_rows = []

fieldnames = ["NAME_0", "NAME_1", "NAME_2", "NAME_3", "Unique"]

with open(in_names_file, encoding="utf8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_row = {}
        new_row['NAME_0'] = row['NAME_0']
        new_row['NAME_1'] = row['NAME_1']
        new_row['NAME_2'] = row['NAME_2']
        new_row['NAME_3'] = row['NAME_3']
        new_row['Unique']   = row['NAME_3'] + ', ' + row['NAME_2']
        out_rows.append(new_row)

with open('new.csv', 'w', encoding='utf8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in out_rows:
        writer.writerow(row)