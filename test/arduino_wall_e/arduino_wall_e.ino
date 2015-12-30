
#include <Servo.h>

Servo servoYaw;
Servo servoPitch;
Servo servoRoll;

int yawCenter = 40;
int yawLeft = 60;
int yawRight = 20;

int rollCenter = 100;
int rollLeft = 75;
int rollRight = 150;

// pitch depend on roll
int pitchDown = 120;
int pitchCenter = 100; // 75 if roll != center
int pitchUp = 50;

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

int pitch = 0;
int roll = 0;
int yaw = 0;

void setup()
{
  Serial.begin(9600);
  servoYaw.attach(8);  
  servoPitch.attach(9);
  servoRoll.attach(10);
}

void loop()
{
  serialEvent();
  /*
  SERIAL PROTOCOL
    p20 => pitch 20
    r-10 => roll -10
  
  */
  if (stringComplete) {
    if (inputString.startsWith("r") ) {
      Serial.println("roll");
      String sub = inputString.substring(1);
      Serial.println(sub); 
      roll = sub.toInt();
    } else if (inputString.startsWith("p") ) {
      Serial.println("pitch");  
      String sub = inputString.substring(1);
      pitch = sub.toInt();
    } else if (inputString.startsWith("y") ) {
      Serial.println("yaw");  
      String sub = inputString.substring(1);
      yaw = sub.toInt();
    } 
    
    // clear the string:
    inputString = "";
    stringComplete = false;
    
  }
   /*
  servoRoll.write(rollRight);
  delay(500);
  servoRoll.write(rollCenter);
  delay(500);
  servoRoll.write(rollLeft);
  delay(500);
  servoRoll.write(rollCenter);
  delay(500);
  return;
  */
  /*
  servoYaw.write(20);
  servoPitch.write(pitchCenter);
  delay(5);
  */
  // pitch, roll, yaw
  // wallE(0, 20, 0);
  wallE(pitch, roll, yaw);
  
  //range(servoPitch, pitchUp, pitchDown);
  //range(servoRoll, rollLeft, rollRight);
  //range(servoYaw, yawRight, yawLeft);
  
  return;

}

void wallE(int pitch, int roll, int yaw) {
    pitch = pitch + 90;
    roll = roll + 90;
    yaw = yaw + 90;
   
    // servoRoll.write(rollCenter);
    
    int v;
    v = map(roll, -20, 20, rollLeft, rollRight);
    
    // pitch depends on roll for construction
    // pitch = pitch + (-roll*0.7);
    
    v = map(pitch, 30, -40, pitchUp, pitchDown);
    
    servoRoll.write(roll);
    servoPitch.write(pitch);
    servoYaw.write(yaw);
}

void range(Servo servo, int start, int end) {
  int pos = 0;
  for (pos = start; pos <= end; pos += 1) {
    servo.write(pos);
    delay(10);
  }
  for (pos = end; pos >= start; pos -= 1) {
    servo.write(pos);
    delay(10);
  }  
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

