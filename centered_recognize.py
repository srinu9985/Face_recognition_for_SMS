# to exit from program
import sys

#To generate key and perform password encryption and decryption
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#base64 for url safe encoding
from base64 import urlsafe_b64encode

#for mailing
from smtplib import SMTP
from email.message import EmailMessage

#to generate random otp
from random import randint

#To connect to mongodb
from pymongo import MongoClient

#for face recognition
import face_recognition

#for video capturing and naming the identified faces
import cv2

#to set time for videocapturing and to sleep while showing identified data
import time

#for showing information message
import tkinter

#for GUI
from customtkinter import *

#for browser automation
from selenium import webdriver

#generating key using a passphrase for unique generation of key and adding salt for uniqueness of key
key_generate_passphrase = "mini_project@143"
kdf = PBKDF2HMAC(length=32,salt='2018_batch'.encode(),algorithm=SHA256,iterations=100000, backend=default_backend())
key = kdf.derive(key_generate_passphrase.encode())
key = urlsafe_b64encode(key).decode()
fernet = Fernet(key)

window = CTk()  #creating customtkinter window
screen_width = window.winfo_screenwidth()   #to take screen width
screen_height = window.winfo_screenheight() #to take screen height
window.withdraw()   #now main window of customtkinter is hidden

set_appearance_mode("System")       #appearance mode of dialog boxes/toplevels created from customtkinter
set_default_color_theme('blue')     #color theme for widgets of dialog boxes

recognized_images = []      #to store identified images
encodings_n18 = []  #to store encodings taken from MongoDB
collection = [] #to store collection of MongoDB
#function to set toplevel window position
def set_window_position(top_level):

    #finding window width of toplevels
    window_width = top_level.winfo_width()
    window_height = top_level.winfo_height()

    #finding screen width and height
    screen_width = top_level.winfo_screenwidth()
    screen_height = top_level.winfo_screenheight()

    #finding center at desktop
    position_x = int((screen_width-window_width)/2)
    position_y = int((screen_height - window_height)/ 2)
    top_level.geometry(f"+{position_x}+{position_y}")   #positioning toplevels at center
    # top_level.geometry("+500+250")    #directly setting position with numeric values
    top_level.resizable(False, False)  # toplevel not resizable

#function which exits user from program when he clicked on top right cancel button in toplevels
def exit_program(top_level):
    result = tkinter.messagebox.askyesno("CONFIRM","Are you sure to exit the application?") #to show confirmation message to exit
    if result:
        top_level.destroy()     #destroys toplevel window
        sys.exit()
    else:
        return

#function to show options whether to recognize single person(solo person available) or multiple persons(in crowd)
def which_login():
    top_level_1 = CTkToplevel()     #creating toplevel
    set_window_position(top_level_1)
    top_level_1.protocol("WM_DELETE_WINDOW",lambda: exit_program(top_level_1))  #function to take action while clicking on cancel button of toplevels - WM_DELETE_WINDOW is a window manager protocol message i.e., sent to a window when the user tries to close it(clicking on cancel button)
    top_level_1.title("ONE|MANY")   #setting title for toplevel
    def which_login_result():
        top_level_1.destroy()
        if(r1_var.get() == "one"):  #fetching data stored in the widget's variable
            recognizing_one_face()
        else:
            recognizing_faces()
    def enable_button():
        CTkButton(top_level_1, text="OK", command=which_login_result).grid(pady=20,padx=20,row=2,column=0)
    r1_var = StringVar()
    r1 = CTkRadioButton(top_level_1,text="one_person_recognize",variable=r1_var,value = "one",command=enable_button).grid(pady=20,padx=40,row=0,column=0)
    r2 = CTkRadioButton(top_level_1,text="many_persons_recognize",variable=r1_var,value="many",command=enable_button).grid(pady=20,padx=40,row=1,column=0)
    button_which_login = CTkButton(top_level_1,text="OK",state=DISABLED).grid(pady=20,padx=20,row=2,column=0)
    top_level_1.mainloop()

IDs_matched = []

#to recognize single face
def recognizing_one_face():
    start_time = time.time()
    duration = 20
    var = False
    video_capture_object = cv2.VideoCapture(0)  #creating video capture object
    #set camera frame dimensions to fit screen resolution
    # video_capture_object.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)      #It's nice to use these to show images of webcam but it takes time to open webcam after including these statements
    # video_capture_object.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)
    cv2.namedWindow('RECOGNIZING', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('RECOGNIZING', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while((time.time()-start_time)<=duration):
        ret, frame = video_capture_object.read()    #reading webcam data
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  #converting BGR format to RGB format as face_recognition module works with RGB format
        face_loacations_in_frame = face_recognition.face_locations(rgb_frame)   #finding face locations --> returns list of tuples
        face_encodings_in_frame = face_recognition.face_encodings(rgb_frame, face_loacations_in_frame)  #finding face encodings at identified locations -->returns list of arrays(an array of 128 values)
        # for (top, right, left, bottom), face_encodings_of_frame in zip(face_loacations_in_frame,face_encodings_in_frame):
        for face_encodings_of_frame in face_encodings_in_frame:
            threshold = 0.4
            matched = face_recognition.compare_faces(encodings_n18, face_encodings_of_frame,threshold)  #comparing encodings of webcam with saved MongoDB data. It gives index of recognized images
            name = "Stranger"
            if True in matched:
                recognized_images.append('N'+str(180001+matched.index(True)))   #appending identified images
                name = recognized_images[0]
                cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0, 0, 0),2)
                var = True
                break
            else:
                # cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)    #to draw rectangle over detected face
                cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,(0, 0, 0), 2)  #showing name at position 50 px down from top and 50px right from left end
        cv2.imshow("RECOGNIZING", frame)
        if cv2.waitKey(1) == 32:    # waitkey returns ASCII value of pressed key and also wait for 1 millisecond for input i.e., to stop showing videocapturing when user clicked on "space bar"(32 is ASCII value of space bar)
            break
        if(var==True):
            break
    video_capture_object.release()  #releasing video capture object
    cv2.destroyAllWindows()     #destroying all windows opened by opencv module i.e., cv2
    if var==True:
        # check_0(recognized_images[0])
        fetch(recognized_images[0])
    else:
        time_out()

#to recognize multiple images in the given time
def recognizing_faces():
    id = 180001
    start_time = time.time()
    duration = 20
    video_capture_object = cv2.VideoCapture(0)
    cv2.namedWindow('RECOGNIZING', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('RECOGNIZING', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while (time.time() - start_time <= duration):
        ret, frame = video_capture_object.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_loacations_in_frame = face_recognition.face_locations(rgb_frame)
        face_encodings_in_frame = face_recognition.face_encodings(rgb_frame, face_loacations_in_frame)
        # for (top, right, left, bottom), face_encodings_of_frame in zip(face_loacations_in_frame,face_encodings_in_frame):
        for face_encodings_of_frame in face_encodings_in_frame:
            threshold=0.4
            matched = face_recognition.compare_faces(encodings_n18, face_encodings_of_frame,threshold)
            name = "Stranger"
            if True in matched:
                IDs_matched = ['N'+str(id+i) for i, match in enumerate(matched) if match]
                for i in IDs_matched:
                    cv2.putText(frame, i, (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (0, 0, 0),2)
                    if i not in recognized_images:
                        recognized_images.append(i)
            else:
                cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,(0, 0, 0), 2)
        cv2.imshow("RECOGNIZING", frame)
        if cv2.waitKey(1) == 32:
            break
    video_capture_object.release()
    cv2.destroyAllWindows()
    check_1()

def time_out():
    def time_out_result():
        top_level_4.destroy()
        recognizing_one_face()
    top_level_4 = CTkToplevel()
    set_window_position(top_level_4)
    top_level_4.protocol("WM_DELETE_WINDOW", lambda: exit_program(top_level_4))
    top_level_4.title("NONE")
    CTkLabel(top_level_4,text="No one recognized").pack(padx=40,pady=20)
    CTkButton(top_level_4,text="Retry",command=time_out_result).pack(padx=40)
    CTkButton(top_level_4, text="Exit", command=sys.exit).pack(pady=20)
    top_level_4.mainloop()
def direct_login(id, passwd):
    if os.path.isfile("chromedriver.exe") == False:
        tkinter.messagebox.showerror('NO_DRIVER','please place chrome driver in path i.e., in the same location of python script')
        sys.exit()
    try:
        options = webdriver.ChromeOptions()  # to set options
        options.add_experimental_option("detach",True)  # setting chrome option to detatch opened browser window from program, so that browser won't be closed even if we exit the program
        browser = webdriver.Chrome(options=options)
        browser.maximize_window()
        browser.get("https://intranet.rguktn.ac.in/SMS/")  # opening browser to this url
        browser.implicitly_wait(10)  # maximum time to wait to identify each element in browser
        user_name = browser.find_element(by="id", value="user1")  # finding elements
        password = browser.find_element(by="id", value="passwd1")
        user_name.send_keys(id)  # sending keys
        password.send_keys(passwd)
        password.submit()  # clicking on submit
        sys.exit()
    except Exception:
        try:
            title_browser = browser.title   #checking whether is opened or closed
            browser.quit()  #closing the browser and also it's sessions
            top_level_7 = CTkToplevel()
            set_window_position(top_level_7)
            top_level_7.protocol("WM_DELETE_WINDOW", lambda: exit_program(top_level_7))
            top_level_7.title('LOGIN ISSUE')
            def exception_dl_result_1():
                top_level_7.destroy()
                direct_login(id, passwd)
            CTkLabel(top_level_7,text="Some error occured\n\n Check your internet connection then click on Retry\n\n To exit the program click on Exit").pack(padx=20,pady=20)
            CTkButton(top_level_7,text='Retry',command=exception_dl_result_1).pack()
            CTkButton(top_level_7, text='Exit', command=sys.exit).pack(pady=20)
            top_level_7.mainloop()
        except Exception:
            top_level_9 = CTkToplevel()
            set_window_position(top_level_9)
            top_level_9.protocol("WM_DELETE_WINDOW", lambda: exit_program(top_level_9))
            top_level_9.title('LOGIN ISSUE')
            def exception_dl_result_2():
                top_level_9.destroy()
                direct_login(id, passwd)
            CTkLabel(top_level_9,text="Browser closed\n\n click on retry to again retry\n\n To exit the program click on Exit").pack(padx=20, pady=20)
            CTkButton(top_level_9, text='Retry', command=exception_dl_result_2).pack()
            CTkButton(top_level_9, text='Exit', command=sys.exit).pack(pady=20)
            top_level_9.mainloop()
def retry():
    top_level_2 = CTkToplevel()
    set_window_position(top_level_2)
    top_level_2.protocol("WM_DELETE_WINDOW", lambda: exit_program(top_level_2))
    top_level_2.title("RETRY")
    def retry_result():
        top_level_2.destroy()
        recognizing_faces()
    CTkLabel(top_level_2,text="No one recognized. \n\nClick on retry to again recognize or click on Exit to exit program").pack(padx=10)
    CTkButton(top_level_2,text="Retry",command=retry_result).pack(pady=20)
    CTkButton(top_level_2, text="Exit", command=sys.exit).pack(pady=20)
    top_level_2.mainloop()

#function to verify random_top generated and user inputted otp
def enter_otp(id,random_otp):
    def verify_otp_result():
        if otp_data.get() == str(random_otp):
            top_level_6.destroy()
            fetch(id)
        else:
            tkinter.messagebox.showerror('Invalid','Invalid OTP')
    top_level_6 = CTkToplevel()
    set_window_position(top_level_6)
    top_level_6.protocol("WM_DELETE_WINDOW", lambda : exit_program(top_level_6))
    top_level_6.title("VERIFY")
    otp_info = CTkLabel(top_level_6, text='\nEnter OTP sent to mail for confirmation of your login').pack(padx=20)
    otp_data = CTkEntry(top_level_6, placeholder_text='Enter OTP').pack(padx=40,pady=20)
    ok_otp = CTkButton(top_level_6, text='VERIFY', command=verify_otp_result).pack(padx=40)
    CTkButton(top_level_6, text='EXIT', command=sys.exit).pack(padx=40,pady=20)
    top_level_6.mainloop()
def email_send(id):
    try:
        server = SMTP('smtp.gmail.com', 587)    #to create a SMTP session
        server.starttls()   #starts TLS for security
        server.login('pavansankar9@gmail.com', 'ivmqxbgptzzynalq')  #Authetication purpose
        em = EmailMessage()     #base class for core email object model for creating or modifying structured messages
        em['To'] = id+'@rguktn.ac.in'
        em['From'] = 'pavansankar9@gmail.com'
        em['Subject'] = 'SMS login'
        body = 'The below IDs also recognized while trying to log into your SMS:\n\n'
        for i in recognized_images:
            if i!=id:
                body += i + '\n'
        random_otp = randint(1000, 9999)
        body += '\nSo enter OTP '+str(random_otp)+' to proceed to your SMS'
        em.set_content(body)    #setting body to message
        server.sendmail('pavansankar9@gmail.com', id+'@rguktn.ac.in', em.as_string())
        enter_otp(id, random_otp)
    except Exception:
        top_level_8 = CTkToplevel()
        set_window_position(top_level_8)
        top_level_8.protocol("WM_DELETE_WINDOW", lambda: exit_program(top_level_8))
        top_level_8.title('VERIFY ISSUE')
        def exception_es_result():
            top_level_8.destroy()
            email_send(id)
        CTkLabel(top_level_8, text="May be some network error\n\n Check your internet connection then click on Retry\n\n To exit the program click on Exit").pack(padx=20, pady=20)
        CTkButton(top_level_8, text='Retry', command = exception_es_result).pack()
        CTkButton(top_level_8, text='Exit', command=sys.exit).pack(pady=20)
        top_level_8.mainloop()

#shows recognized images as options
def show_option_to_login(recognized_images):
    top_level_5 = CTkToplevel()
    set_window_position(top_level_5)
    top_level_5.protocol("WM_DELETE_WINDOW", lambda: exit_program(top_level_5))
    top_level_5.title("IDENTIFIED")
    def show_option_to_login_result():
        top_level_5.destroy()
        email_send(id_to_log.get())
    id_to_log = StringVar()
    CTkLabel(top_level_5,text="Many people recognized").pack(pady=20)
    for i in recognized_images:
        CTkRadioButton(top_level_5, text = i, variable=id_to_log, value=i).pack(pady=20,padx=60)
    CTkButton(top_level_5, text="submit",command=show_option_to_login_result).pack(pady=20,padx=60)
    top_level_5.mainloop()

# def check_0(id):
#     def check_0_result_1():
#         top_level_3.destroy()
#         fetch(id)
    # def check_0_result_2():
    #     top_level_3.destroy()
    #     recognized_images.clear()
    #     recognizing_one_face()
    # top_level_3 = CTkToplevel()
    # set_window_position(top_level_3)
    # top_level_3.protocol("WM_DELETE_WINDOW", lambda: exit_program(top_level_3))
    # top_level_3.title("RECOGNIZED")
    # CTkButton(top_level_3,text="Log_to_"+id,command=check_0_result_1).pack(pady=20,padx=60)
    # CTkButton(top_level_3, text="Retry", command=check_0_result_2).pack()
    # CTkButton(top_level_3, text="exit_program", command=sys.exit).pack(pady=20)
    # top_level_3.mainloop()
def decrypt_password(encrypted_password):
    password = fernet.decrypt(encrypted_password).decode()      #decrypt password
    return password
def fetch(id):
    encrypted_password = collection.find({'_id':id},{'password':1,'_id':0})[0]['password']
    if encrypted_password != None:
        password = decrypt_password(encrypted_password)
        direct_login(id,password)
    else:
        tkinter.messagebox.showinfo("NO_DATA",f"Hey {id}, Your password is not available in database")
        sys.exit()
def check_1():
    if (len(recognized_images) == 1):
        fetch(recognized_images[0])
    elif (len(recognized_images) > 1):
        show_option_to_login(recognized_images)
    else:
        retry()

if __name__  == '__main__':
    def mongo_connection():
        try:
            # #for localhost connection to fetch data stored in local mongodb
            # client = MongoClient("mongodb://localhost:27017")
            # db = client["sms_login_details"]
            # collection = db["sms_login_details_n18"]
            # making MongoDB atlas connection to fetch data stored in atlas for face recognition
            mongo_atlas = MongoClient("mongodb+srv://mini_project:2018_batch@cluster0.8dutogq.mongodb.net/")
            db = mongo_atlas["sms_login_details"]
            global collection
            collection = db["sms_login_details_n18"]
            n18_encodings = collection.find({}, {"_id": 0, "face_encoding": 1})  # Assume as it returns a list of dictionaries which only has 'face_encoding' as a key and it's encoding as a value. But in general n18_encodings is a cursor object which has dictionaries of our face encodings
            global  encodings_n18
            encodings_n18 = [i['face_encoding'] for i in n18_encodings]  # It only has encodings stored in a list
        except:
            top_level_9 = CTkToplevel()
            set_window_position(top_level_9)
            top_level_9.protocol("WM_DELETE_WINDOW", lambda: exit_program(top_level_9))
            top_level_9.title('CONNECTION ISSSUE')
            def exception_mc_result():
                top_level_9.destroy()
                mongo_connection()
            CTkLabel(top_level_9,text="Some error occured\n\n Check your internet connection then click on Retry\n\n To exit the program click on Exit").pack(padx=20, pady=20)
            CTkButton(top_level_9, text='Retry', command=exception_mc_result).pack()
            CTkButton(top_level_9, text='Exit', command=sys.exit).pack(pady=20)
            top_level_9.mainloop()
        else:
            which_login()
    mongo_connection()