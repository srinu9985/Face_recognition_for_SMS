import pymongo
from mail_ids_n18 import *
from password_extract_from_file import *
from listing_out_files_in_folder import *
import numpy as np

#Mongodb_connection
client = pymongo.MongoClient("mongodb://localhost:27017")
#mongo_atlas = pymongo.MongoClient("mongodb+srv://mini_project:2018_batch@cluster0.8dutogq.mongodb.net/")

db = mongo_atlas['sms_login_details']
collection = db["sms_login_details_n18"]
print("Client: ",mongo_atlas)

id = 180001
i=0
while(id<=181191):
    inserting = collection.insert_one({'_id':'N'+str(id),"name":list_of_names[i],
                           "password":encrypted_passwords_n18['N'+str(id)],
                           "face_encoding":face_encodings_of_photo['N'+str(id)],
                           "image":binary_data_of_photo['N'+str(id)]})
    print("Inserted_id: ",inserting.inserted_id)
    id+=1
    i+=1
