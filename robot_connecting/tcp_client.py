import os
import socket
import cv2
import glob
import numpy
import time
import base64
import sys
import threading
import sys
import termios
import tty 

class ClientSocket:
    def __init__(self, ip, port):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.createImageDir()
        self.folder_num = 0
        self.cnt = 0
        self.cnt_str = ''
        self.connectCount = 0
        self.connectServer()
        self.command()

    def command(self):
        buf = ""
        # Configure keystroke capture.
        stdin = sys.stdin.fileno()
        tattr = termios.tcgetattr(stdin)

        try:
            tty.setcbreak(stdin, termios.TCSANOW)
            sys.stdout.flush()
            # Read command from keyboard.
            while True:
                buf += sys.stdin.read(1)
                if (buf[-1] == "a"): 
                    data = "TurnLeft"
                elif (buf[-1] == "d"):  
                    data = "TurnRight"
                elif (buf[-1] == "w"):  
                    data = "Forward"
                elif (buf[-1] == "s"):  
                    data = "Backward"
                elif (buf[-1] == "x"):
                    data = "Stop"
                elif (buf[-1] == "p"):
                    data = "Photo"
                elif (buf[-1] == "+"):
                    data = "Increase"
                elif (buf[-1] == "-"):
                    data = "Decrease"
                elif (buf[-1] == "q"):
                    data = "Quit"
                    self.sock.sendall(bytes(data, "utf-8"))
                    break
                else:
                    print("Unknown command.\n")
                    continue
                print(data)
                self.sock.sendall(bytes(data, "utf-8"))
                self.receiveImage()

        finally:
            termios.tcsetattr(stdin, termios.TCSANOW, tattr)

    def connectServer(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')
            self.connectCount = 0
        except Exception as e:
            print(e)
            self.connectCount += 1
            if self.connectCount == 10:
                print(u'Connect fail %d times. exit program'%(self.connectCount))
                sys.exit()
            print(u'%d times try to connect with server'%(self.connectCount))
            self.connectServer()

    def receiveImage(self):
        # Get data from robot.
        action = self.sock.recv(64)
        action = action.decode('utf-8')
        if action == "no_photos":
            return
        try:
            # Assign photo id.
            if (self.cnt < 10):
                self.cnt_str = '000' + str(self.cnt)
            elif (self.cnt < 100):
                self.cnt_str = '00' + str(self.cnt)
            elif (self.cnt < 1000):
                self.cnt_str = '0' + str(self.cnt)
            else:
                self.cnt_str = str(self.cnt)
            self.cnt += 1

            length = self.recvall(self.sock, 64)
            length1 = length.decode('utf-8')
            stringData = self.recvall(self.sock, int(length1))
            stime = self.recvall(self.sock, 64)


            data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)
            decimg = cv2.imdecode(data, 1)

            cv2.imwrite('./' + str(self.TCP_SERVER_PORT) + '_images' + str(self.folder_num) + '/img' + self.cnt_str + '.jpg', decimg)

            cv2.waitKey(1)

        except Exception as e:
            print(e)
            self.convertImage( self.cnt)
            self.sock.close()
            time.sleep(1)
            self.connectServer()

            

    def createImageDir(self):
        folder_name = str(self.TCP_SERVER_PORT) + "_images0"
        try:
            if not os.path.exists(folder_name):
                os.makedirs(os.path.join(folder_name))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("Failed to create " + folder_name +  " directory")
                raise
        
    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf    

    def convertImage(self, count):
        img_array = []
        self.cnt = 0
        for filename in glob.glob('./' + str(self.TCP_SERVER_PORT) + '_images' + '/*.jpg'):
            if (self.cnt == count):
                break
            self.cnt = self.cnt + 1
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)

def main():
    TCP_IP = '192.168.0.15' # Robot Ip address in Wi-Fi network got through linux console
    TCP_SERVER_PORT = 9997  # Free port (must be the same as on the robot).
    client = ClientSocket(TCP_IP, TCP_SERVER_PORT)


if __name__ == "__main__":
    main()
