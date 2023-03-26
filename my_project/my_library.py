import base64
import mysql.connector
from datetime import date
import time
import numpy as np
from keras.models import load_model
from keras.utils import load_img, img_to_array
from io import BytesIO

def predict_value(bytes_data):
    model = load_model("E:/APASD/predimg.h5")
    # Create a binary buffer from the bytes object
    buffer = BytesIO(bytes_data)

    image = load_img(buffer, target_size=(150,150))
    image = img_to_array(image)
    image = np.expand_dims(image,axis=0)
    val = model.predict(image)
    if val>0.5:
        return "Signature"
    else:
        return "Photograph"

def insertIMAGEDATA(image):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            database="mydatabase",
            password="P@ssword1"
            )
        
        cursor = connection.cursor()
        query = """ INSERT INTO IMAGEDATA
                (UPLOADED_DATE, DATE, UPLOADED_TIME, TIME, IMAGE, PREDICTED_VALUE) 
                VALUES (%s,%s,%s,%s,%s,%s)"""
        
        uploaded_date = date.today()
        r_date = uploaded_date.strftime("%d %B, %Y")
        uploaded_time = time.strftime("%I:%M:%S",time.localtime())
        r_time = time.strftime("%I:%M %p",time.localtime())
        predicted_value = predict_value(image)
        insert_tuple = (uploaded_date, r_date, uploaded_time, r_time, image, predicted_value)
        cursor.execute(query, insert_tuple)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed inserting data into MySQL table {}".format(error))

    except Exception as e:
        print(e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def retrieveIMAGEDATA():
    final_array = []
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            database="mydatabase",
            password="Deepak@973"
            )

        cursor = connection.cursor()
        query = """SELECT DATE, TIME, IMAGE, PREDICTED_VALUE FROM IMAGEDATA ORDER BY UPLOADED_DATE DESC,UPLOADED_TIME DESC LIMIT 5"""
        cursor.execute(query)
        record = cursor.fetchall()
        for row in record:
            sub_dict = dict()
            sub_dict["uploaded_date"] = str(row[0])
            sub_dict["uploaded_time"] = str(row[1])
            sub_dict["image"] = base64.b64encode(row[2]).decode('utf-8')
            sub_dict["predicted_value"] = str(row[3])
            final_array.append(sub_dict)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed inserting data into MySQL table {}".format(error))

    except Exception as e:
        print(e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return final_array
