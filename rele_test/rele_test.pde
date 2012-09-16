/*
 Enciende y apaga una bombilla de 220V, cada 2 segundos, mediante
 un relé conectado al PIN 8 de Arduino 
 */
 int relayPin = 8;                 // PIN al que va conectado el relé
 void setup(){
   pinMode(relayPin, OUTPUT);      
 }
 void loop() {
   digitalWrite(relayPin, HIGH);   // ENCENDIDO
   delay(2000);                   
   digitalWrite(relayPin, LOW);    // APAGADO
   delay(2000);                  
 }
