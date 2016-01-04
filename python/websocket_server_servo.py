#!/usr/bin/python
# sudo pip install websocket-client
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
from subprocess import call, Popen, PIPE
import thread, threading
import time
import pigpio

websocket_port = 9000

GPIO_LEFT  = 20
GPIO_RIGHT = 21
GPIO_PITCH = 19
GPIO_ROLL  = 13
GPIO_YAW   = 26
GPIO_DOOR  = 16

pitchValue = 1500
rollValue  = 1500
yawValue   = 1500
leftValue  = 1500
rightValue = 1500
doorValue  = 1500

class TestWebSocket(WebSocket):

  def handleMessage(self):
    global  leftValue, rightValue, pitchValue, rollValue, yawValue, doorValue
    print "handleMessage " + str(self.data)
    message = str(self.data).strip()
    command = message[0]
    if command == "p":
        value = message[1:]
        pitchValue = 1500 + (int(value) * 10 * 1)
        pi.set_servo_pulsewidth(GPIO_PITCH, pitchValue)
    if command == "r":
        value = message[1:]
        rollValue = 1500 + (int(value) * 10 * 1)
        pi.set_servo_pulsewidth(GPIO_ROLL, rollValue)
    if command == "y":
        value = message[1:]
        yawValue = 1500 + (int(value) * 10 * 1)
        pi.set_servo_pulsewidth(GPIO_YAW, yawValue)
    if command == "L":
        value = message[1:]
        leftValue = 1500 + (int(value) * 10 * 1)
        pi.set_servo_pulsewidth(GPIO_LEFT, leftValue)
    if command == "R":
        value = message[1:]
        rightValue = 1500 + (int(value) * 10 * -1)
        pi.set_servo_pulsewidth(GPIO_RIGHT, rightValue)
    if command == "d":
        value = message[1:]
        doorValue = 1500 + (int(value) * 10 * 1)
        pi.set_servo_pulsewidth(GPIO_DOOR, doorValue)
    if command == "s":
        print('s')
        leftNormalized  = str((leftValue  - 1500) / 10);
        rightNormalized = str((rightValue - 1500) / 10);
        pitchNormalized = str((pitchValue - 1500) / 10);
        rollNormalized  = str((rollValue  - 1500) / 10);
        yawNormalized   = str((yawValue   - 1500) / 10);
        doorNormalized  = str((doorValue  - 1500) / 10);

        status = 's='
        status += leftNormalized  + ',' + rightNormalized + ','
        status += pitchNormalized + ',' + rollNormalized  + ',' + yawNormalized + ','
        status += doorNormalized
        print(status)
        self.sendMessage(status)
        
        '''
        status = "s=" + str((pitchValue - 1500)/10) + ',' + str(rollValue - 16) + ',' + str(yawValue) + ',' + str(leftValue) + ',' + str(rightValue) + ',' + str(doorValue)
        print(status)
        p = Popen(['iwconfig', 'wlan0'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        cmdOutput, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
        print(str(cmdOutput))
        self.sendMessage(str(status))
        self.sendMessage(str(cmdOutput))
        '''
        

  def handleConnected(self):
    print self.address, 'connected'

  def handleClose(self):
    print self.address, 'closed'

def startWebSocketServer():
  socketServer = SimpleWebSocketServer('', websocket_port, TestWebSocket)
  socketServer.serveforever()


if __name__ == "__main__":

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



