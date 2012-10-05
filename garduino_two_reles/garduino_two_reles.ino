/*
 Two-entries moisture sensure and reactive watering prototype. 
 */

const int analogInPin1 = A0; // Analog input pin to the potentiometer #1
const int analogInPin2 = A2; // Analog input pin to the potentiometer #2
const int digitalOutPin1 = 2; // Rele-Electrovalve output #1
const int digitalOutPin2 = 3; // Rele-Electrovalve output #2
const int minSensorValue1 = 400; // Minimun value from the potentiometer #1 to trigger watering
const int minSensorValue2 = 500; // Minimun value from the potentiometer #2 to trigger watering

int sensorValue = 0; // value read from the potentiometer

void SendToSerial (int number, int sensorValue)
{
  // print the results to the serial monitor:
  Serial.print("#");
  Serial.print(number);
  Serial.print("#");
  Serial.print(sensorValue);
  Serial.print("#");
  Serial.print("\n");
}

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
  pinMode(digitalOutPin1, OUTPUT);   
  pinMode(digitalOutPin2, OUTPUT);   
}

void loop() {
  int sensorValue1, sensorValue2 = 0;
  // read the analog in value
  sensorValue1 = analogRead(analogInPin1);
  SendToSerial(1, sensorValue1);
  sensorValue2 = analogRead(analogInPin2);
  SendToSerial(2, sensorValue2);
  
  if (sensorValue1 <= minSensorValue1) {
     digitalWrite(digitalOutPin1, HIGH); 
  }
  else {
     digitalWrite(digitalOutPin1, LOW);
  }  

  if (sensorValue2 <= minSensorValue2) {
     digitalWrite(digitalOutPin2, HIGH); 
  }
  else {
     digitalWrite(digitalOutPin2, LOW);
  }  
     
  // wait 10 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(1000);                     
}
