import socket
import cv2
import pickle
import struct
import tkinter as tk
from tkinter import *

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

    def testing(self):
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
            print("Emotion",pickle.loads(emotion))

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

            cv2.namedWindow('Testing', cv2.WINDOW_NORMAL)
            cv2.imshow('Testing', frame)

            key = cv2.waitKey(7) % 0x100
            if key == 27:
                break
        cv2.destroyAllWindows()

    def learning(self):
        option = pickle.dumps(0)
        self.soc.sendto(option, self.addr)
        self.top.destroy()
        cap = cv2.VideoCapture(0)
        cap.set(3, 500)
        cap.set(4, 260)
        i = 0
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
                #Store data in file
                print(emotions[1])
                print(emotions[2])

            wait_key = cv2.waitKey(1) % 0x100

            if wait_key == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    def start(self):
        self.top = tk.Tk()
        self.top.title("ASGM Software")
        self.top.geometry('600x300')
        frame = tk.Frame(self.top, width=50, height=50)
        frame.place(x=100, y=10)
        w1 = tk.Label(frame, text="Choose your option to Start.", font=("Helvetica", 16),
                      fg="BLACK")
        w1.pack(fill=X, pady=10)
        w2 = tk.Label(frame, text="Not to move Your Face. Sit in proper LIGHT", font=("Helvetica", 16), fg="BLACK")
        w2.pack(fill=X, pady=10)
        B = tk.Button(frame, text="Start Testing", command= self.testing, bd=1, width=30, pady=10, padx = 10,  bg="BLUE")
        B.pack(fill=X, pady=10)
        B1 = tk.Button(frame, text="Start Learning", command= self.learning, bd=1, width=30, pady=10, padx= 10, bg="GREEN")
        B1.pack(fill=X, pady=10)
        self.top.mainloop()
#Add feature of Check Users
    def createDirectory(self,type,input, input2):
        print("Fuck")

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
            self.top.mainloop()
        elif type == 2:
            self.top = tk.Tk()
            self.top.title("ASGM Software")
            self.top.geometry('600x300')
            frame = tk.Frame(self.top, width=50, height=50)
            frame.place(x=100, y=10)
            w1 = tk.Label(frame, text="Add new user.", font=("Helvetica", 16),
                          fg="BLACK")
            w1.pack(fill=X, pady=10)
            var = StringVar(frame)
            #var.set("one")
            users_data = []
            file_path_users = self.newpath + "/users/users.txt"
            with open(file_path_users) as f:
                lines = f.readlines()
                users_data.append(str(lines))

            option = tk.OptionMenu(frame, var, *users_data)
            option.pack()
            B1 = tk.Button(frame, text="Submit", command=lambda: self.createDirectory(2, var.get(), ""), bd=1, width=30,
                           pady=10,
                           padx=10, bg="GREEN")
            B1.pack(fill=X, pady=10)
            self.top.mainloop()

    def choose_user(self):
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
    client.choose_user()

