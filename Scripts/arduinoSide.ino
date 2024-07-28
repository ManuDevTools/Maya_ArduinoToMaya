const int potPin = A2;

void setup() {
  // Iniciar la comunicación serie a 9600 baudios
  Serial.begin(115200);
}

void loop() {
  // Enviar un mensaje cada segundo

  
  int potValue = analogRead(potPin);
  Serial.println(potValue);

  // Verificar si hay datos entrantes
  if (Serial.available() > 0) {
    String incomingData = Serial.readStringUntil('\n'); // Leer datos hasta el final de la línea
    Serial.print("Mensaje recibido: ");
    Serial.println(incomingData);
  }
  
  delay(100);
}