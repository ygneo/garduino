/*
 Two-entries moisture sensure and reactive watering prototype. 
 */
const int analogInPin1 = A0; // Analog input pin from moisture sensor #1
const int analogInPin2 = A2; // Analog input pin from moisture sensor #2
const int digitalOutPin1 = 2; // Rele-Electrovalve output #1
const int digitalOutPin2 = 3; // Rele-Electrovalve output #2
const int minSensorValue1 = 400; // Minimun value from the potentiometer #1 to trigger watering
const int minSensorValue2 = 500; // Minimun value from the potentiometer #2 to trigger watering
const int wateringTime[] = {3000, 6000}; // Watering time for every plant
const int checkingDelay = 1000; // Delay between checks (for the analog-to-digital converter to settle after last reading)
const int checkAfterWateringInterval = 300000; // 5 min, for testing
unsigned long int lastCheck[] = {0, 0}; // Last time moisture sensors was checked


void sendToSerial (int number, int sensorValue)
{
  Serial.print("#");
  Serial.print(number);
  Serial.print("#");
  if (sensorValue == -1) {
    Serial.print("w");
  }
  else {
    Serial.print(sensorValue);
  }
  Serial.print("#");
  Serial.print("\n");
}

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(digitalOutPin1, OUTPUT);
  pinMode(digitalOutPin2, OUTPUT);
  digitalWrite(digitalOutPin1, LOW);
  digitalWrite(digitalOutPin2, LOW);
}

void loop() {
  int sensorValue1, sensorValue2;

  sensorValue1 = analogRead(analogInPin1);
  sendToSerial(1, sensorValue1);
  Serial.print("lc1:\n");
  Serial.print(lastCheck[0]);
  Serial.print("\n");

  sensorValue2 = analogRead(analogInPin2);
  sendToSerial(2, sensorValue2);
  Serial.print("lc2:\n");
  Serial.print(lastCheck[1]);
  Serial.print("\n");
    
  if (sensorValue1 <= minSensorValue1 && lastCheck[0] >= checkAfterWateringInterval) {
     digitalWrite(digitalOutPin1, HIGH);
     sendToSerial(1, -1);
     delay(wateringTime[0]);
     digitalWrite(digitalOutPin1, LOW);
     lastCheck[0] = 0;
  }

  if (sensorValue2 <= minSensorValue2 && lastCheck[1] >= checkAfterWateringInterval) {
     digitalWrite(digitalOutPin2, HIGH);
     sendToSerial(2, -1);
     delay(wateringTime[1]);
     digitalWrite(digitalOutPin2, LOW);
     lastCheck[1] = 0;
  }
  
  delay(checkingDelay);
  lastCheck[0] += checkingDelay;
  lastCheck[1] += checkingDelay;
}
