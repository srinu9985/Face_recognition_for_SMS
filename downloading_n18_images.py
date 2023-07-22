import os.path
import requests

# id = 180001
# not_downloaded = []
# while id<=181191:
#     url = "https://intranet.rguktn.ac.in/SMS/usrphotos/user/N"+str(id)+".jpg"
#     response = requests.get(url,verify=False)
#     if requests.codes.ok == response.status_code:
#         folder_name = "n18_batch_images"
#         base_name = os.path.basename(url)
#         if os.path.exists(folder_name):
#             output_file_location = os.path.join(folder_name,base_name)
#         else:
#             os.makedirs(folder_name)
#             output_file_location = os.path.join(folder_name,base_name)
#         f = open(output_file_location, 'wb')
#         f.write(response.content)
#         print(f"Image of {base_name} saved in folder {folder_name}. So, actual location is {output_file_location}")
#     else:
#         print("Response not ok")
#         print(base_name)
#         not_downloaded.append(base_name)
#     id+=1
#
# print(not_downloaded)
# print(len(not_downloaded))
# f = open(r'n18_batch_images\not_downloaded.txt', 'wb')
# for i in not_downloaded:
#     f.write(i)

#below code is to download n18_batch_images normally(i.e.,url_only)-no_200_check
#it only worked to download all IDs images...

id = 180001
while id<=181191:
    url = "https://intranet.rguktn.ac.in/SMS/usrphotos/user/N"+str(id)+".jpg"
    response = requests.get(url)
    folder_name = "n18_batch_images"
    base_name = os.path.basename(url)
    if os.path.exists(folder_name):
        output_file_location = os.path.join(folder_name,base_name)
    else:
        os.makedirs(folder_name)
        output_file_location = os.path.join(folder_name,base_name)
    f = open(output_file_location, 'wb')
    f.write(response.content)
    print(f"Image of {base_name} saved in folder {folder_name}. So, actual location is {output_file_location}")
    id+=1