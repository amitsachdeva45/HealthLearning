import socket
import cv2
import pickle
import struct
import tkinter as tk
from tkinter import *
import os
import matplotlib.pyplot as plt
import numpy as np
class client:
    port = 50081
    addr = 0.0
    host = "127.0.0.1"
    soc = ""
    top = ""
    newpath = r'X:\Masters of Applied computer Science\ConcHacks\FinalProject'
    def __init__(self):
        self.addr = (self.host, self.port)
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(self.addr)

    def testing(self, folder_path):
        option = pickle.dumps(1)
        self.soc.sendto(option, self.addr)
        self.top.destroy()
        data = b""
        payload_size = struct.calcsize(">L")
        i=0
        while True:
            i=i+1
            while len(data) < payload_size:
                data += self.soc.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.soc.recv(4096)


            frame_data = data[:msg_size]
            data = data[msg_size:]

            useless = pickle.dumps(1)
            self.soc.sendto(useless, self.addr)

            (emotion, addr) = self.soc.recvfrom(1024)
            emotion_list = pickle.loads(emotion)
            if i%100 == 0:
                file = open(folder_path + "/testing.txt", "a+")
                file.write(str(emotion_list[0]) + " " + str(emotion_list[1]) + "\n")
                file.close()

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

            cv2.namedWindow('Testing', cv2.WINDOW_NORMAL)
            cv2.imshow('Testing', frame)

            key = cv2.waitKey(7) % 0x100
            if key == 27:
                break
        cv2.destroyAllWindows()

    def learning(self, folder_path):
        option = pickle.dumps(0)
        self.soc.sendto(option, self.addr)
        self.top.destroy()
        cap = cv2.VideoCapture(0)
        cap.set(3, 500)
        cap.set(4, 260)
        i = 0
        j=0
        with open(folder_path + "/file_name.txt") as f:
            for line in f:
                j = j + 1
        file = open(folder_path + "/file_name.txt", "a+")
        file.write("test" + str(j+1) + ".txt"+"\n")
        file.close()


        while True:
            ret, frame = cap.read()
            i = i + 1
            data = pickle.dumps(frame)
            size = len(data)
            cv2.namedWindow('Learning Doctor', cv2.WINDOW_NORMAL)
            cv2.imshow('Learning Doctor', frame)
            self.soc.sendall(struct.pack(">L", size) + data)
            (emotion_data, addr) = self.soc.recvfrom(1024)
            emotions = pickle.loads(emotion_data)
            if emotions[0] == "emotion":
                file = open(folder_path + "/test" + str(j + 1) + ".txt", "a+")
                file.write(str(emotions[1]) + " " +str(emotions[2])+"\n")
                file.close()

            wait_key = cv2.waitKey(1) % 0x100

            if wait_key == 27:
                break
        cap.release()
        cv2.destroyAllWindows()


    def start(self, folder_path, user_folder):
        self.top = tk.Tk()
        self.top.title(user_folder)
        self.top.geometry('600x300')
        frame = tk.Frame(self.top, width=50, height=50)
        frame.place(x=100, y=10)
        w1 = tk.Label(frame, text="Choose your option to Start.", font=("Helvetica", 16),
                      fg="BLACK")
        w1.pack(fill=X, pady=10)
        w2 = tk.Label(frame, text="Not to move Your Face. Sit in proper LIGHT", font=("Helvetica", 16), fg="BLACK")
        w2.pack(fill=X, pady=10)
        B = tk.Button(frame, text="Start Testing", command=lambda: self.testing(folder_path), bd=1, width=30, pady=10, padx = 10,  bg="BLUE")
        B.pack(fill=X, pady=10)
        B1 = tk.Button(frame, text="Start Learning", command=lambda: self.learning(folder_path), bd=1, width=30, pady=10, padx= 10, bg="GREEN")
        B1.pack(fill=X, pady=10)
        B2 = tk.Button(frame, text="Back", command=lambda: self.choose_user(2), bd=1, width=30,
                       pady=10, padx=10, bg="RED")
        B2.pack(fill=X, pady=10)
        self.top.mainloop()


    def createDirectory(self,type,input, input2):
        self.top.destroy()
        file_path = self.newpath + "/users/"
        if type == 1:
            i=0
            with open(file_path + "users.txt") as f:
                for line in f:
                    i=i+1
            folder_name = str(1000 + i) + input[:2]+ str(input2)
            if not os.path.exists(file_path + folder_name):
                os.makedirs(file_path + folder_name)
            file = open(file_path + "users.txt", "a+")
            file.write(folder_name + " "+ input + " "+ input2 + "\n")
            file.close()
            file = open(file_path + folder_name + "/file_name.txt", "w+")
            file.close()
            self.start(file_path + folder_name, folder_name)
        elif type == 2:
            folder_name = input.split(" ")
            self.start(file_path + folder_name[0], folder_name[0])

    def showGraph(self, emotion_array, emotion_array_percentage):
        index = np.arange(len(emotion_array))
        plt.bar(index, emotion_array_percentage)
        plt.xlabel('Emotions', fontsize=10)
        plt.ylabel('Response Rate', fontsize=10)
        plt.xticks(index, emotion_array, fontsize=5, rotation=30)
        plt.title('Patients response rate over the period.')
        plt.show()
    def startAnalyzing(self, users):
        folder_path = self.newpath +"/users/"+users
        file_exists = os.path.isfile(folder_path+"/file_name.txt")
        corr_dict = dict()
        total_dict = dict()
        if file_exists:
            with open(folder_path+"/file_name.txt") as f:
                for line in f:
                    with open(folder_path +"/" + line.replace("\n","")) as f1:
                        for line1 in f1:
                            line_split = line1.replace("\n","").split(" ")
                            if line_split[0] in corr_dict:
                                if line_split[1] == '1':
                                    corr_dict[line_split[0]] = corr_dict[line_split[0]] + 1
                                total_dict[line_split[0]] = total_dict[line_split[0]] + 1
                            else:
                                if line_split[1] == '1':
                                    corr_dict[line_split[0]] = 1
                                else:
                                    corr_dict[line_split[0]] = 0
                                total_dict[line_split[0]] =  1
        else:
            self.choose_user(1)

        test_exists = os.path.isfile(folder_path + "/testing.txt")
        if test_exists:
            with open(folder_path+"/testing.txt") as f:
                for line in f:
                    line_split = line.replace("\n","").split(" ")
                    if line_split[0] in corr_dict:
                        if line_split[0] == line_split[1]:
                            corr_dict[line_split[0]] = corr_dict[line_split[0]] + 1
                        total_dict[line_split[0]] = total_dict[line_split[0]] + 1
                    else:
                        if line_split[1] == line_split[0]:
                            corr_dict[line_split[0]] = 1
                        else:
                            corr_dict[line_split[0]] = 0
                        total_dict[line_split[0]] = 1

        i=0
        emotion_array_data = []
        emotion_percentage_data = []
        for key in total_dict:
            emotion_array_data.append(key)
            emotion_percentage_data.append(float(corr_dict[key])/total_dict[key])

        self.showGraph(emotion_array_data, emotion_percentage_data)

    def createUser(self, type):
        self.top.destroy()
        if type == 1:
            self.top = tk.Tk()
            self.top.title("ASGM Software")
            self.top.geometry('600x300')
            #frame = tk.Frame(self.top, width=50, height=50)
            #frame.place(x=100, y=10)
            Label(self.top, text="Add new user.", font=("Helvetica", 16), fg="BLACK").grid(row=0, column = 2)
            Label(self.top, text="Name" , font=("Helvetica", 16), fg="BLACK").grid(row=1)
            e1 = Entry(self.top)
            Label(self.top, text="Age" , font=("Helvetica", 16), fg="BLACK").grid(row=2)
            e2 = Entry(self.top)

            e1.grid(row=1, column=2)
            e2.grid(row=2, column=2)
            Button(self.top, text="Submit", command=lambda: self.createDirectory(1,e1.get(),e2.get()), bd=1, width=30, pady=10,
                           padx=10, bg="GREEN").grid(row=3, column = 2)
            Button(self.top, text="Back", command=lambda: self.choose_user(2), bd=1, width=30, pady=10,padx=10, bg="RED").grid(row=4, column=2)
            self.top.mainloop()
        elif type == 2:
            self.top = tk.Tk()
            self.top.title("ASGM Software")
            self.top.geometry('600x300')
            frame = tk.Frame(self.top, width=50, height=50)
            frame.place(x=100, y=10)
            w1 = tk.Label(frame, text="Select existing users.", font=("Helvetica", 16),
                          fg="BLACK")
            w1.pack(fill=X, pady=10)
            var = StringVar(frame)

            users_data = []
            file_path_users = self.newpath + "/users/users.txt"
            with open(file_path_users) as f:
                lines = f.read().splitlines()
            i=0
            while i<len(lines):
                users_data.append(lines[i])
                i=i+1
            var.set(lines[0])
            option = tk.OptionMenu(frame, var, *users_data)
            option.pack()
            B1 = tk.Button(frame, text="Start Learning", command=lambda: self.createDirectory(2, var.get(), ""), bd=1, width=30,
                           pady=10,
                           padx=10, bg="GREEN")
            B1.pack(fill=X, pady=10)
            B2 = tk.Button(frame, text="Start Analyzing Users", command=lambda: self.startAnalyzing(var.get().split(" ")[0]), bd=1,
                           width=30,
                           pady=10,
                           padx=10, bg="YELLOW")
            B2.pack(fill=X, pady=10)
            B3 = tk.Button(frame, text="Back", command=lambda: self.choose_user(2), bd=1, width=30,
                           pady=10,
                           padx=10, bg="RED")
            B3.pack(fill=X, pady=10)
            self.top.mainloop()

    def choose_user(self, type):
        if type == 2:
            self.top.destroy()
        self.top = tk.Tk()
        self.top.title("ASGM Software")
        self.top.geometry('600x300')
        frame = tk.Frame(self.top, width=50, height=50)
        frame.place(x=100, y=10)
        w1 = tk.Label(frame, text="Choose your option to Start.", font=("Helvetica", 16),
                      fg="BLACK")
        w1.pack(fill=X, pady=10)
        B = tk.Button(frame, text="Add new patient", command=lambda: self.createUser(1), bd=1, width=30, pady=10, padx=10, bg="BLUE")
        B.pack(fill=X, pady=10)
        B1 = tk.Button(frame, text="Already Existing", command=lambda: self.createUser(2), bd=1, width=30, pady=10, padx=10, bg="GREEN")
        B1.pack(fill=X, pady=10)
        self.top.mainloop()

if __name__ == '__main__':
    client = client()
    client.choose_user(1)

