import threading
import time
import serial
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

serial_port = "/dev/cu.usbmodem1421";
serial_baudrate = 9600
websocket_port = 9000

class TestWebSocket(WebSocket):
  def handleMessage(self):
    print "handleMessage " + str(self.data)
    arduino.write(str(self.data))

  def handleConnected(self):
    print self.address, 'connected'

  def handleClose(self):
    print self.address, 'closed'

def startWebSocketServer():
  socketServer = SimpleWebSocketServer('', websocket_port, TestWebSocket)
  socketServer.serveforever()

if __name__ == "__main__":
  
  arduino = serial.Serial(serial_port, serial_baudrate, timeout=500, dsrdtr=False)
  arduino.setDTR(True)
  
  threadWebSocket = threading.Thread(target=startWebSocketServer)
  threadWebSocket.daemon = True
  threadWebSocket.start()

  while True:
    time.sleep(1)

