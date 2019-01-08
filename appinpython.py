import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='data')
cursor = mydb.cursor()

#csv_data = csv.reader(file('soh.csv'))

sql = """INSERT INTO appdata(code, item, price ) VALUES(%s, %s, %s)"""

with open('/root/soh.csv') as csvfile:
    reader = csv.DictReader(csvfile,delimiter = ',')
    for row in reader:
         sku = row['code']
         name = row['item']
         price = row['price']
         values = (code, item, price)
         print(values)
         cursor.execute(sql,values)

mydb.commit()
cursor.close()
