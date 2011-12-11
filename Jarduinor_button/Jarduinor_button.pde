/*
 Second moisture sensure prototype. 
 
 Arduino connected electric signal amplifying circuit and two cabled nails as conductivity
 (~moisture) sensor, and a button indicated when sand is watered.
 
 It reads value from analog in pin and print it to serial formatted as "#<value>#". 
 Value is (0, 1024), although maximium empiric value is 893. So 100% moisture can be
 considered at 900. 
 If button is pressed, a "#-1#" value is sent.


 The circuit:
    * Sensor: two nails connected to an circuit amplifying electric signal to analog pin,
 <TDB>
 
 created 7 Dec. 2011
 by Antonio Barcia
 
 This code is in the public domain.
 */

const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int buttonPin = 2;     // the number of the pushbutton p

int sensorValue = 0;        // value read from the pot
int buttonState = LOW
; 

void SendToSerial (int id, int sensorValue)
{
  // print the results to the serial monitor:
  Serial.print("#");
  Serial.print(sensorValue);
  Serial.print("#");
  Serial.print("\n");
}

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(buttonPin, INPUT); 
}

void loop() {
  // read the analog in value
  
  sensorValue = analogRead(analogInPin);  
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);
  
  if (buttonState == HIGH) {
     sensorValue = -1;
  }
  SendToSerial(1,sensorValue);
 
  delay(1000);                     
}
