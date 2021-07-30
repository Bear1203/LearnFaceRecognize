import MySQLdb


database = MySQLdb.connect(host="yourIP", user="userName",
                           passwd="password", db="facenet", charset="utf8", use_unicode=True)
cursor = database.cursor()
your_name = "Rubyr1008"
fp = open(your_name + ".jpg", 'rb')
img = fp.read()
fp.close()
sql = "INSERT INTO face_name_images VALUES  (%s, %s);"
args = (your_name, img)
cursor.execute(sql, args)
database.commit()
cursor.close()
database.close()
print("Insert success")
