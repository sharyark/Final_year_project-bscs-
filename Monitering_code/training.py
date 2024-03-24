import cv2
import face_recognition as FR
import os
import pickle as pk
import mysql.connector
font=cv2.FONT_HERSHEY_SIMPLEX

# connector = mysql.connector.connect(host='localhost',user='root',password='BimsCS@8A',database='Testing')
# connector = mysql.connector.connect(host='192.168.43.112',user='fyp',password='',database='FYP')
connector = mysql.connector.connect(host='192.168.182.112',user='fyp',password='',database='FYP')

cursor  = connector.cursor()
cursor.execute(""" select e.db_picture,e.id FROM attendance_app_employee e INNER JOIN auth_user u on u.id = e.user_id; """)
data  = cursor.fetchall()

for data in data:
    image = data[0]
    username = data[1]
    # print(f"image: {image}")
    # print(f"username: {username}")

    # Save the image with the username as filename in the current working directory
    with open(f'{os.getcwd()}/known/{username}.jpg', 'wb') as f:
        f.write(image)

print(data)


cursor.close()
connector.close()

# def insert_known():
#     # connecting to database
#     db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="image_demo"
#     )
#     # making object of database and fetching the data
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM images WHERE 1=1")
#     result = cursor.fetchall()
#     # pasting data in known folder
#     for i in list(result):
#         with open("./known/"+str(i[0])+".jpg", "wb") as image_file:
#             image_file.write(i[2])

# insert_known()
# import os
# os.chdir('/path/to/your/directory')

imgDirs = ('./known')
names = []
knownEncodings = []
for root,dirs,filesz in os.walk(imgDirs):
    for nm in filesz:
        print(root)
        print(filesz)
        objFace=FR.load_image_file(os.path.join(root,nm))
        print(objFace)
        faceLoc=FR.face_locations(objFace)
        objEncoded = FR.face_encodings(objFace,faceLoc)
        objEncoded = objEncoded[0]
        knownEncodings.append(objEncoded)
        nm1 = nm.strip('.jpg')
        nm1 = nm1.strip('.jpeg')
        nm1 = nm1.strip('.png')
        names.append(nm1)
with open('/home/sharyar_khan/Desktop/newFyp/train.pkl','wb') as f:
    pk.dump(names,f)
    pk.dump(knownEncodings,f)










