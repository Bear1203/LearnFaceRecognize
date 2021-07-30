import MySQLdb
from PIL import Image
import io
import cv2
import numpy as np


def database_output():
    all_image = []
    all_name = []
    database = MySQLdb.connect(host="yourIP", user="userName",
                               passwd="password", db="facenet", charset="utf8", use_unicode=True)
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM face_name_images")
    result = cursor.fetchall()

    for row in result:
        data = row["Image"]
        name = row["Name"]
        piimage = Image.open(io.BytesIO(data))
        cvimage = cv2.cvtColor(np.asarray(piimage), cv2.COLOR_RGB2BGR)
        all_name.append(name)
        all_image.append(cvimage)

    cursor.close()
    database.close()

    return all_name, all_image
