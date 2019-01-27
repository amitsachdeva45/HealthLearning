import socket
import cv2
import os
import pickle
import struct
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import tkinter as tk
import random
class server:
    port = 50081
    addr = 0.0
    conn = ''
    headers = ""
    params = ""
    newpath = r'X:\Masters of Applied computer Science\ConcHacks\FinalProject'
    tk=""
    def __init__(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ""
        self.addr = (host, self.port)
        soc.bind((host, self.port))
        soc.listen(5)
        self.conn, self.addr = soc.accept()
        self.headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': 'cfd53222bf084a459d88d3cca0fe522a',
        }

        self.params = urllib.parse.urlencode({
            # Request parameters
            'returnFaceId': 'false',
            'returnFaceRectangle': 'false',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'emotion'
        })

    def emotionDetection(self, path):
        image_path = path
        image_data = open(image_path, "rb").read()
        try:
            conn = http.client.HTTPSConnection('canadacentral.api.cognitive.microsoft.com')
            conn.request("POST", "/face/v1.0/detect?%s" % self.params, image_data, self.headers)
            response = conn.getresponse()
            data = response.read()
            fetch_data = json.loads(data.decode())
            final_data = fetch_data[0]['faceAttributes']['emotion']
            max_val = -1
            max_index = ""
            for list in final_data:
                if final_data[list] > max_val:
                    max_val = final_data[list]
                    max_index = list
            conn.close()
            return max_index
        except Exception as e:
            return "neutral"

    #Show Emotions on Video
    def testing(self):
        if not os.path.exists(self.newpath+"\sample"):
            os.makedirs(self.newpath+"\sample")
        cap = cv2.VideoCapture(0)
        cap.set(3, 500)
        cap.set(4, 260)
        i=0
        emotion="neutral"
        expected_emotion = ""
        folders = []
        name_of_file = []
        number_of_images = []
        emotion_array = []
        with open(self.newpath + "/emotionsDataSet.txt") as f:
            for line in f:
                temp = line.split(" ")
                folders.append(temp[0])
                name_of_file.append(temp[1])
                number_of_images.append(temp[2])

        i = 0
        while True:
            emotion_array = []
            ret, frame = cap.read()
            if i % 100 == 0:
                index = random.randint(0, len(folders)-1)
                expected_emotion = folders[index]
                image_value = random.randint(1,int(number_of_images[index]))
                image_path = self.newpath +"/" + folders[index] + "/"+ name_of_file[index] + str(image_value) + ".jpg"
                testing_image = cv2.imread(image_path)
                cv2.namedWindow('Testing Image', cv2.WINDOW_NORMAL)
                cv2.imshow('Testing Image', testing_image)
            i=i+1
            if i%50 == 0:
                file = self.newpath + "/sample/imageimage" + str(i) + ".png"
                cv2.imwrite(file, frame)
                emotion = self.emotionDetection(file)
            data = pickle.dumps(frame)
            size = len(data)
            self.conn.sendall(struct.pack(">L", size) + data)

            (useless, addr) = self.conn.recvfrom(1024)
            emotion_array.append(emotion)
            emotion_array.append(expected_emotion)
            send_emotion = pickle.dumps(emotion_array)
            self.conn.sendto(send_emotion, self.addr)

            wait_key = cv2.waitKey(1) % 0x100

            if wait_key == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    def showchoice(self):
        self.tk.destroy()

    def questionnaire(self, person_emotion):
        self.tk = tk.Tk()
        v = tk.IntVar()
        v.set(1)
        emotions = [
            ("Anger", 1),
            ("Contempt", 2),
            ("Disgust", 3),
            ("Fear", 4),
            ("Happiness", 5),
            ("Neutral", 6),
            ("Sadness",7),
            ("Surprise", 8)
        ]
        tk.Label(self.tk,
                 text="""What's the mood:""",
                 justify=tk.LEFT,
                 padx=20).pack()

        for val, emotion in enumerate(emotions):
            tk.Radiobutton(self.tk,
                  text=emotion[0],
                  indicatoron = 0,
                  width = 20,
                  padx = 20,
                  variable=v,
                  command = self.showchoice,
                  value=val).pack(anchor=tk.W)

        self.tk.mainloop()
        testemotion = ""
        for val, emotion in enumerate(emotions):
            if val == v.get():
                testemotion = emotion[0]
                break

        if testemotion.lower() == person_emotion.lower():
            return 1
        else:
            return 0


    def learning(self):
        data = b""
        payload_size = struct.calcsize(">L")
        i = 0
        while True:
            emotion_response = []
            emotion_response.append("useless")
            emotion_response.append("")
            emotion_response.append(2)
            i = i + 1
            while len(data) < payload_size:
                data += self.conn.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.conn.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            if i%100 == 0:
                file = self.newpath + "/sample/testing" + str(i) + ".png"
                cv2.imwrite(file, frame)
                emotion = self.emotionDetection(file)
                cv2.destroyAllWindows()
                response = self.questionnaire(emotion)
                emotion_response = []
                emotion_response.append("emotion")
                emotion_response.append(emotion)
                emotion_response.append(response)

            emotion_data = pickle.dumps(emotion_response)
            self.conn.sendto(emotion_data, self.addr)

            cv2.namedWindow('Learning Patient', cv2.WINDOW_NORMAL)
            cv2.imshow('Learning Patient', frame)

            key = cv2.waitKey(7) % 0x100
            if key == 27:
                break
        cv2.destroyAllWindows()

    def start(self):
        (data, addr) = self.conn.recvfrom(1024)
        data = pickle.loads(data)
        if data == 1:
            self.testing()
        else:
            self.learning()
if __name__ == '__main__':
    server = server()
    server.start()

