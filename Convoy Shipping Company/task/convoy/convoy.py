import csv
import json
import pandas as pd
import re
import sqlite3
from dicttoxml import dicttoxml


print("Input file name")
filename = input()
csv_name = filename.split('.')[-2] + '.csv'
checked_name = filename.split('.')[-2].replace("[CHECKED]", "") + '[CHECKED].csv'
db_name = filename.split('.')[-2].replace("[CHECKED]", "") + '.s3db'
json_name = filename.split('.')[-2].replace("[CHECKED]", "") + '.json'
xml_name = filename.split('.')[-2].replace("[CHECKED]", "") + '.xml'
step = 1
if filename.endswith(".csv"):
    step = 2
if filename.endswith("[CHECKED].csv"):
    step = 3
if filename.endswith(".s3db"):
    step = 4
# Create CSV
if step == 1:
    my_df = pd.read_excel(filename, sheet_name='Vehicles', dtype=str)
    rows, cols = my_df.shape

    my_df.to_csv(csv_name, header=True, index=None)
    if rows == 1:
        print("1 line was added to {}".format(csv_name))
    else:
        print("{} lines were added to {}".format(rows, csv_name))
    step += 1
# Correct CSV
if step == 2:
    with open(csv_name, newline='') as vehicle:
        with open(checked_name, "w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
            file_reader = csv.reader(vehicle, delimiter=",")
            count = 0
            cells = 0
            for line in file_reader:
                if count == 0:
                    file_writer.writerow(line)
                    count += 1
                else:
                    new_list = []
                    for x in line:
                        if x.isdigit():
                            new_list.append(x)
                        else:
                            new_list.append(re.sub(r"\D", "", x))
                            cells += 1
                    file_writer.writerow(new_list)
                    count += 1
            if cells == 1:
                print("1 cell was corrected in {}".format(checked_name))
            else:
                print("{} cells were corrected in {}".format(cells, checked_name))
    step += 1
# Create database
if step == 3:
    conn = sqlite3.connect(db_name)
    cursor_name = conn.cursor()
    cursor_name.execute('''CREATE TABLE if not exists convoy  
                   (vehicle_id INT PRIMARY KEY,
                    engine_capacity INT NOT NULL,
                    fuel_consumption INT NOT NULL,
                    maximum_load INT NOT NULL,
                    score INT NOT NULL)
                ''')
    records = 0
    with open(checked_name) as vehicle:
        file_reader = csv.reader(vehicle, delimiter=",")
        count = 0
        for line in file_reader:
            if count == 0:
                count += 1
            else:
                score = 0
                fuel_consumption = int(line[2])
                engine_capacity = int(line[1])
                maximum_load = int(line[3])
                pit_stops = 4.5 // (engine_capacity / fuel_consumption)
                if pit_stops == 0:
                    score += 2
                elif pit_stops == 1:
                    score += 1

                if maximum_load >= 20:
                    score += 2
                if fuel_consumption * 4.5 <= 230:
                    score += 2
                else:
                    score += 1
                line.append(str(score))
                sql = "INSERT INTO convoy VALUES ({})".format(",".join(line))
                records += 1
                cursor_name.execute(sql)
    conn.commit()
    conn.close()
    if records == 1:
        print("1 record was inserted into {}".format(db_name))
    else:
        print("{} records were inserted into {}".format(records, db_name))
    step += 1
# Export to JSON and XML
if step == 4:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM convoy;")
    names = [description[0] for description in cursor.description]
    all_rows = cursor.fetchall()
    conn.close()
    data = [dict(zip(names[:4], all_row[:4])) for all_row in all_rows if all_row[4] > 3]
    data_xml = [dict(zip(names[:4], all_row[:4])) for all_row in all_rows if all_row[4] < 4]
    vehicles = len(data)
    with open(json_name, "w") as final:
        json.dump({'convoy': data}, final)
    if vehicles == 1:
        print("1 vehicle was saved into {}".format(json_name))
    else:
        print("{} vehicles were saved into {}".format(vehicles, json_name))

    my_item_func = lambda val: 'vehicle'
    xml = dicttoxml({'convoy': data_xml}, item_func=my_item_func, attr_type=False, root=False)
    xml_decode = xml.decode()
    xml_file = open(xml_name, "w")
    xml_file.write(xml_decode)
    xml_file.close()
    xml_vehicles = len(data_xml)
    if not data_xml:
        print("0 vehicles were saved into {}".format(xml_name))
    elif xml_vehicles == 1:
        print("1 vehicle was saved into {}".format(xml_name))
    else:
        print("{} vehicles were saved into {}".format(xml_vehicles, xml_name))
