const int potPin = A2;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int portValue = analogRead(potPin);

  Serial.println(portValue);

  if (Serial.available() > 0) {
    String incomingData = Serial.readStringUntil('\n');
    Serial.print("received message: ");
    Serial.println(incomingData);
  }
  
  delay(100);
}