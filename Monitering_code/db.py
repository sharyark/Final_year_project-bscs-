import mysql.connector
import time
from datetime import datetime,timedelta
class DBhelper:

    try:
        def __init__(self):
            # enter database server ip username password and databasename
            self.conn = mysql.connector.connect(host='192.168.182.112',user='fyp',password='',database='FYP')
            self.mycursor = self.conn.cursor()
            self.chk = 0
    except:
        print("some error occured")

    else:
        print("connected successfully")
        

    def entrance(self,I_D=2):
        print(I_D)
        # checking the user are registered or not
        # self.mycursor.execute("SELECT id , department,date_of_birth,joining_date,user_id FROM attendance_app_employee WHERE user_id = '{}'".format(I_D))
        self.mycursor.execute("SELECT id , department,date_of_birth,joining_date,user_id FROM attendance_app_employee WHERE id = '{}'".format(I_D))
        obj = self.mycursor.fetchall()
        if len(obj):
            self.mark_attendanc(obj)
        else:
            print('person is not registered... call the capture one')       

    def mark_attendanc(self,obj):
        e_id = obj[0][0]
        date = time.strftime("%Y-%m-%d")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(e_id)
        #-----------------
        self.mycursor.execute("SELECT * FROM attendance_app_attendance WHERE date = '{}' AND employee_id ='{}'".format(date,e_id))
        obj = self.mycursor.fetchall()
        if len(obj): # if already exist on same day
            d_t = self.time_difference_Entry(obj)
            d_h = d_t[0]
            # if time is one hour or more then one hour then update it
            if d_h >=1 or d_t[1] >1:
                self.mycursor.execute("""UPDATE `attendance_app_attendance`
                                      SET  `entrance_time` = '{}', `status` = '{}'
                                      WHERE `date` = '{}' AND `employee_id` = '{}' """.format(current_time, 'live', date,e_id))
                self.conn.commit()
            print(d_t)
        else:
            self.mycursor.execute("""INSERT INTO `attendance_app_attendance` ( `date`, `entrance_time`, `employee_id`,`status`)
                         VALUES ('{}', '{}', '{}', '{}');""".format(date,current_time,e_id,'live'))
            self.conn.commit()

    def time_difference_Entry(self,data):
        p_time = data[0][2]
        p_time = str(p_time).split(':')
        p_h,p_m = int(p_time[0]),int(p_time[1])
        now = datetime.now()
        n_time = now.strftime("%H:%M:%S")
        n_time = str(n_time).split(':')
        n_h,n_m = int(n_time[0]),int(n_time[1])
        d_h = n_h - p_h
        d_m = n_m - p_m
        if d_m <0:
            d_m  = d_m+60
        return (d_h,d_m)
    def time_difference_Exit(self,data):
        if len(data) == 0: # if entered without marking attendance so skip it
            return (0,0)
        previous_time_str = str(data[0][2])
        total_time = str(data[0][4])

        print("total time :",total_time)
        # Convert the previous time string to a datetime object with the current date
        current_date = datetime.now().date()
        previous_time = datetime.combine(current_date, datetime.strptime(previous_time_str, "%H:%M:%S").time())

        # Get the current time
        current_time = datetime.now()

        # Calculate the time difference
        time_difference = current_time - previous_time

        # Extract hours and minutes from the time difference
        hours = time_difference // timedelta(hours=1)
        minutes = (time_difference // timedelta(minutes=1)) % 60

        return (hours,minutes)

    def exit(self,I_D):
        # checking the user are registered or not
        self.mycursor.execute("SELECT id , department,date_of_birth,joining_date,user_id FROM attendance_app_employee WHERE id = '{}'".format(I_D))
        obj = self.mycursor.fetchall()
        if len(obj):
            self.leaving(obj)
            # print(obj)
        else:
            print('person is not registered... call the capture one') 
    def leaving(self,obj):
        e_id = obj[0][0]
        date = time.strftime("%Y-%m-%d")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.mycursor.execute("SELECT * FROM attendance_app_attendance WHERE date = '{}' AND employee_id ='{}'".format(date,e_id))
        obj = self.mycursor.fetchall() 
        t_d = self.time_difference_Exit(obj)
        d_h = str(t_d[0])
        d_m = str(t_d[1])
        total_time = d_h+':'+d_m
        if len(obj):
            # print(self.chk,'------')
            # print(d_m,'-----')
            print(int(d_m) - self.chk > 2)
            if self.chk == 0 or int(d_m) - self.chk > 2:
                # print("time difference logic ",end="")
                # print("self chk ",self.chk)
                # print("dm ",d_m)
                # print(int(d_m)-self.chk)
                self.chk = int(d_m)
                self.mycursor.execute("""UPDATE `attendance_app_attendance` 
                SET `exit_time` = '{}',`total_time` = '{}',`status` = 'dead'
                WHERE date like '{}' AND employee_id LIKE '{}';""".format(current_time,total_time,date,e_id))
                self.conn.commit()
        else:
            pass





