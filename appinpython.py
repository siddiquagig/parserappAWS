import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='data')
cursor = mydb.cursor()

#csv_data = csv.reader(file('soh.csv'))

sql = """INSERT INTO appdata(sku, name, price ) VALUES(%s, %s, %s)"""

with open('/root/soh.csv') as csvfile:
    reader = csv.DictReader(csvfile,delimiter = ',')
    for row in reader:
         sku = row['sku']
         name = row['name']
         price = row['price']
         values = (code, item, price)
         print(values)
         cursor.execute(sql,values)

mydb.commit()
cursor.close()
