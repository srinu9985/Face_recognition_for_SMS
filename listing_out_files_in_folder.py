import os,re,face_recognition,pymongo,numpy


photo_files = os.listdir(r"D:\Project-mini\n18_batch_images")
# print(photo_files)

binary_data_of_photo = {}
face_encodings_of_photo = {}

regex = re.compile('\w+')
not_inserted_encodings = []

i=0
while i<=1190:

    with open("D:\\Project-mini\\n18_batch_images\\"+photo_files[i],'rb') as f:
        binary_photo_data = f.read()
    binary_data_of_photo[regex.search(photo_files[i]).group()] = binary_photo_data

    try:
    #Some images were unable to load so i used try block i.e., giving error as cannot identify image file 'D:\\Project-mini\\n18_batch_images\\person_id.jpg'
        load_image = face_recognition.load_image_file("D:\\Project-mini\\n18_batch_images\\" + photo_files[i])
        encoding = face_recognition.face_encodings(load_image)[0]
        face_encodings_of_photo[regex.search(photo_files[i]).group()] = encoding.tolist()
        print(regex.search(photo_files[i]).group(), "inserted")
    except Exception as e:
        face_encodings_of_photo[regex.search(photo_files[i]).group()] = numpy.zeros(128).tolist()
        print(regex.search(photo_files[i]).group(), "not inserted",e)
        not_inserted_encodings.append(regex.search(photo_files[i]).group())
    i=i+1
# print(not_inserted_encodings)




#Below I am checking to insert encodings of photo..
#We cannot insert encodings of some photos as they were giving error as cannot encode object
#So I changed the type of face encodings of photo from numpy.ndarray to str then all photos are inserted to mongodb


"""
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['trail_db']
collection = db["trail_collection"]

photo_files = os.listdir(r"D:\Project-mini\n18_batch_images")
# print(photo_files)

binary_data_of_photo = {}
face_encodings_of_photo = {}

regex = re.compile('\w+')

encodings_list = []
i=0
while i<=1190:
    with open("D:\\Project-mini\\n18_batch_images\\"+photo_files[i],'rb') as f:
        binary_photo_data = f.read()
    binary_data_of_photo[regex.search(photo_files[i]).group()] = binary_photo_data

    try:
    #Some images were unable to load so i used try block i.e., giving error as cannot identify image file 'D:\\Project-mini\\n18_batch_images\\person_id.jpg'
        load_image = face_recognition.load_image_file("D:\\Project-mini\\n18_batch_images\\" + photo_files[i])
        encoding = face_recognition.face_encodings(load_image)[0]
        encodings_list.append(encoding)
        # a = collection.insert_one({"encoding":encoding})
        # face_encodings_of_photo[regex.search(photo_files[i]).group()] = encoding
        # print(regex.search(photo_files[i]).group(),"inserted")
    except Exception as error:
        # face_encodings_of_photo[regex.search(photo_files[i]).group()] = None
        # print(regex.search(photo_files[i]).group(),"not inserted",error)
        encodings_list.append(None)
    i=i+1
print(encodings_list)
"""

'''

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['trail_db']
collection = db["trail_collection"]

import cv2


V_C = cv2.VideoCapture(0)

list = []
encode_1 = face_recognition.face_encodings(face_recognition.load_image_file("N180616.jpg"))[0]
encode_2 = face_recognition.face_encodings(face_recognition.load_image_file("N180109.jpg"))[0]
encode_3 = face_recognition.face_encodings(face_recognition.load_image_file('Chinni.jpg'))[0]

list.append(encode_1.tolist())
list.append(encode_2.tolist())
list.append(encode_3.tolist())


while True:
    ret, frame = V_C.read()
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    a = face_recognition.face_locations(rgb_frame)
    b = face_recognition.face_encodings(rgb_frame,a)
    for (t,r,l,b), face_encoding in zip(a,b):
        match = face_recognition.compare_faces(list,face_encoding)
        print(match)


knencd=[]
known_encoded_1 = face_recognition.face_encodings(face_recognition.load_image_file('N180109me.jpg'))[0]
knencd.append(known_encoded_1)
knencd.append(face_recognition.face_encodings(face_recognition.load_image_file('Chinni.jpg'))[0])
match = face_recognition.compare_faces(knencd,list)  #--> unsupported operand type(s) for -: 'list' and 'list'
print(match)

# a = collection.insert_one({"face_encodings":list})
# print(a.inserted_id)
'''
