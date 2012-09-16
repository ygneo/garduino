/*
 First moisture sensure prototype. 
 
 Arduino connected electric signal amplifying circuit and two cabled nails as conductivity
 (~moisture) sensor.
 
 It reads value from analog in pin and print it to serial formatted as "#<value>#". 
 Value is (0, 1024), although maximium empiric value is 893. So 100% moisture can be
 considered at 900.

 The circuit:
    * Sensor: two nails connected to an circuit amplifying electric signal to analog pin,
 <TDB>
 
 created 7 Dec. 2011
 by Antonio Barcia
 
 This code is in the public domain.
 */

const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to

int sensorValue = 0;        // value read from the pot

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
}

void loop() {
  // read the analog in value
  sensorValue = analogRead(analogInPin);            

  SendToSerial(1, sensorValue);
 
  // wait 10 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(1000);                     
}
