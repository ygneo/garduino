/*
 First moisture sensure prototype:
    * Sensor: two nails connected to an circuit amplifying electric signal to analog pin,
    * Read sensor value in analog pin and send JSOnN in ducksboa
 
 Reads an analog input pin, maps the result to a range from 0 to 255
 and uses the result to set the pulsewidth modulation (PWM) of an output pin.
 Also prints the results to the serial monitor.
 
 The circuit:
 * potentiometer connected to analog pin 0.
   Center pin of the potentiometer goes to the analog pin.
   side pins of the potentiometer go to +5V and ground
 * LED connected from digital pin 9 to ground
 
 created 29 Dec. 2008
 Modified 4 Sep 2010
 by Tom Igoe
 
 This example code is in the public domain.

 */

// These constants won't change.  They're used to give names
// to the pins used:
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int analogOutPin = 9; // Analog output pin that the LED is attached to

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // 





void SendToSerial (int id, int sensorValue)
{
  // print the results to the serial monitor:
  Serial.print(sensorValue);
  Serial.print("\n");
}

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
}

void loop() {
  // read the analog in value
  sensorValue = analogRead(analogInPin);            

  // change the analog out value:
  analogWrite(analogOutPin, outputValue);           

  SendToSerial(1, sensorValue);
 
  // wait 10 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(1000);                     
}
