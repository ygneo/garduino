/*
 Two-entries moisture sensure prototype. 
 
 */


const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int digitalOutPin1 = 2;
const int digitalOutPin2 = 7;

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

void blink(int pin) {
  static int state;
  if (state) {
    digitalWrite(pin, HIGH);   // set the LED on
  }
  else {
    digitalWrite(pin, LOW);   // set the LED on
  }
  state = !state;
}

void loop() {
  // read the analog in value
  sensorValue = analogRead(analogInPin);            
  SendToSerial(1, sensorValue);

  pinMode(digitalOutPin1, OUTPUT);   
  pinMode(digitalOutPin2, OUTPUT);   
  
  if (sensorValue < 400) {
     digitalWrite(digitalOutPin1, HIGH); 
  }
  else {
     digitalWrite(digitalOutPin1, LOW);
  }  
  blink(digitalOutPin2);
     
  // wait 10 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(1000);                     
}
