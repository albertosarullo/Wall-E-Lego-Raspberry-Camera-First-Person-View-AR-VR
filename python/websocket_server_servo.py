#!/usr/bin/python
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from subprocess import call, Popen, PIPE
import thread, threading
import time
import pigpio

websocket_port = 9000

GPIO_LEFT  = 26
GPIO_RIGHT = 19
GPIO_PITCH = 06
GPIO_ROLL  = 13
GPIO_YAW   = 05
GPIO_DOOR  = 22
GPIO_EYES  = 27

pitchValue = 1500
rollValue  = 1500
yawValue   = 1500
leftValue  = 1500
rightValue = 1500
doorValue  = 1500
eyesValue  = 1500
userData   = 0

class TestWebSocket(WebSocket):

  def intToServo(value):
    return 1500 + int(value) * 10

  def servoToInt(value):
    return (int(value) - 1500) / 10

  def handleMessage(self):
    global  leftValue, rightValue, pitchValue, rollValue, yawValue, doorValue, eyesValue, userData
    print "handleMessage " + str(self.data)
    message = str(self.data).strip()
    command = message[0]
    if command == "L":
        value = message[1:]
        leftValue = 1500 + (int(value) * 10 * 1)
        pi.set_servo_pulsewidth(GPIO_LEFT, leftValue)
    elif command == "R":
        value = message[1:]
        rightValue = 1500 + (int(value) * 10 * -1)
        pi.set_servo_pulsewidth(GPIO_RIGHT, rightValue)
    elif command == "p":
        value = message[1:]
        pitchValue = 1500 + (int(value) * 10 * 1)
        pi.set_servo_pulsewidth(GPIO_PITCH, pitchValue)
    elif command == "r":
        value = message[1:]
        rollValue = 1500 + (int(value) * 10 * 1)
        pi.set_servo_pulsewidth(GPIO_ROLL, rollValue)
    elif command == "y":
        value = message[1:]
        yawValue = 1500 + (int(value) * 10 * 1)
        pi.set_servo_pulsewidth(GPIO_YAW, yawValue)
    elif command == "d":
        value = message[1:]
        doorValue = 1500 + (int(value) * 10 * 1)
        pi.set_servo_pulsewidth(GPIO_DOOR, doorValue)
    elif command == "e":
        value = message[1:]
        eyesValue = 1500 + (int(value) * 10 * 1)
        pi.set_servo_pulsewidth(GPIO_EYES, eyesValue)
    elif command == "u":
        value = message[1:]
        userData = value
    elif command == "w":
        p = Popen(['iwconfig', 'wlan0'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        cmdOutput, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        print(str(cmdOutput))
        self.sendMessage(str(cmdOutput))
    elif command == "s":
        print('s')
        leftNormalized  = str((leftValue  - 1500) / 10);
        rightNormalized = str((rightValue - 1500) / 10);
        pitchNormalized = str((pitchValue - 1500) / 10);
        rollNormalized  = str((rollValue  - 1500) / 10);
        yawNormalized   = str((yawValue   - 1500) / 10);
        doorNormalized  = str((doorValue  - 1500) / 10);
        eyesNormalized  = str((eyesValue  - 1500) / 10);

        status = 's='
        status += leftNormalized  + ',' + rightNormalized + ','
        status += pitchNormalized + ',' + rollNormalized  + ',' + yawNormalized + ','
        status += doorNormalized + ',' + eyesValue
        status += str(userData)

        print(status)
        self.sendMessage(status)
        

  def handleConnected(self):
    print self.address, 'connected'

  def handleClose(self):
    print self.address, 'closed'

def startWebSocketServer():
  socketServer = SimpleWebSocketServer('', websocket_port, TestWebSocket)
  socketServer.serveforever()


if __name__ == "__main__":

  print "WALL-E"
  pi = pigpio.pi()

  pi.set_mode(GPIO_LEFT, pigpio.OUTPUT);
  pi.set_mode(GPIO_RIGHT, pigpio.OUTPUT);
  pi.set_mode(GPIO_PITCH, pigpio.OUTPUT);
  pi.set_mode(GPIO_ROLL, pigpio.OUTPUT);
  pi.set_mode(GPIO_YAW, pigpio.OUTPUT);
  
  threadWebSocket = threading.Thread(target=startWebSocketServer)
  threadWebSocket.daemon = True
  threadWebSocket.start()

  while True:
    time.sleep(1)



