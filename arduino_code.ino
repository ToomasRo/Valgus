#define redR1 13
#define greenR1 12
#define redR2 11
#define greenR2 10
int state = 0;
String text;
void setup() {
  pinMode(redR1, OUTPUT);
  pinMode(greenR1, OUTPUT);
  pinMode(redR2, OUTPUT);
  pinMode(greenR2, OUTPUT);
  
  Serial.begin(9600); // Default communication rate of the Bluetooth module
  digitalWrite(redR1, HIGH);
  digitalWrite(greenR1, LOW);
  digitalWrite(redR2, HIGH);
  digitalWrite(greenR2, LOW);

}

void loop() {
  if(Serial.available() > 0){ 
    text = Serial.readStringUntil('\n'); 
    text.trim();
 }
 

 if (text == "S1_R1_OFF") {
  digitalWrite(redR1, HIGH);
  digitalWrite(greenR1, LOW);
  digitalWrite(redR2, HIGH);
  digitalWrite(greenR2, LOW);
  //Serial.println("LED1: OFF");
  text = "";
 }
 else if (text == "S1_R1_ON") {
  digitalWrite(redR1, LOW);
  digitalWrite(greenR1, HIGH);
  digitalWrite(redR2, HIGH);
  digitalWrite(greenR2, LOW);
  //Serial.println("LED1: ON");
  text = "";
 } 
 else if (text.equals("S1_R2_OFF")) {
  digitalWrite(redR1, HIGH);
  digitalWrite(greenR1, LOW);
  digitalWrite(redR2, HIGH);
  digitalWrite(greenR2, LOW);
  //Serial.println("LED2: OFF");
  text = "";
 } 
 else if (text.equals("S1_R2_ON")) {
  digitalWrite(redR1, HIGH);
  digitalWrite(greenR1, LOW);
  digitalWrite(redR2, LOW);
  digitalWrite(greenR2, HIGH);
  //Serial.println("LED2: ON");
  text = "";
 } 
}