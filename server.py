import socket
import cv2
import os
import pickle
import struct
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
class server:
    port = 50081
    addr = 0.0
    conn = ''
    headers = ""
    params = ""
    newpath = r'X:\Masters of Applied computer Science\ConcHacks\FinalProject'
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

    def emotionDetection(self, path, type):
        image_path = path
        image_data = open(image_path, "rb").read()
        print("Hello")
        try:
            conn = http.client.HTTPSConnection('canadacentral.api.cognitive.microsoft.com')
            conn.request("POST", "/face/v1.0/detect?%s" % self.params, image_data, self.headers)
            response = conn.getresponse()
            data = response.read()
            fetch_data = json.loads(data.decode())
            final_data = fetch_data[0]['faceAttributes']['emotion']
            if type == 1:
                return final_data
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

    #Add Random Photos inside this
    #Show Emotion on Tkinter
    #Set emotion detection loop
    def testing(self):
        if not os.path.exists(self.newpath+"\sample"):
            os.makedirs(self.newpath+"\sample")
        cap = cv2.VideoCapture(0)
        cap.set(3, 500)
        cap.set(4, 260)
        i=0
        emotion="neutral"
        while True:
            ret, frame = cap.read()
            i=i+1
            if i == 3 or i == 20:
                file = self.newpath + "/sample/imageimage" + str(i) + ".png"
                cv2.imwrite(file, frame)
                emotion = self.emotionDetection(file,0)
            data = pickle.dumps(frame)
            size = len(data)
            self.conn.sendall(struct.pack(">L", size) + data)

            (useless, addr) = self.conn.recvfrom(1024)

            send_emotion = pickle.dumps(emotion)
            self.conn.sendto(send_emotion, self.addr)

            wait_key = cv2.waitKey(1) % 0x100

            if wait_key == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    #Add Test
    #Send result back
    #Database
    #Data visulization
    #Loop Set
    def learning(self):
        data = b""
        payload_size = struct.calcsize(">L")
        i = 0
        while True:
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
            if i == 50:
                file = self.newpath + "/sample/testing" + str(i) + ".png"
                cv2.imwrite(file, frame)
                emotion = self.emotionDetection(file,1)
                print(emotion)


            useless = pickle.dumps(1)
            self.conn.sendto(useless, self.addr)

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

