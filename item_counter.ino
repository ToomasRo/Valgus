#include <Arduino.h>
#include <U8g2lib.h>
#include <SPI.h>
#include <Wire.h>
char* myChar;
String myString;
int sensorPin = A0;    // select the input pin for the potentiometer
int ledPin = 13;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor
int state =0;
int count = 0;



U8G2_SSD1306_128X32_UNIVISION_F_HW_I2C u8g2(U8G2_R0); 

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  u8g2.begin();
}

void loop() {
  sensorValue = analogRead(sensorPin);
  Serial.print(sensorValue);
  Serial.print("; ");
  Serial.println(count);
  
  if(state == 0){
    if(sensorValue <= 900){
      state = 1;
      count++;
    }
  }
  if(state == 1){
    if(sensorValue > 900){
      state = 0;
    }
  }
  
  myString = String(count);
  const char *text2 = myString.c_str();


   u8g2.clearBuffer();          // clear the internal memory
   u8g2.setFont(u8g2_font_logisoso28_tr);  // choose a suitable font at https://github.com/olikraus/u8g2/wiki/fntlistall
   u8g2.drawStr(8,29, text2);  // write something to the internal memory
   u8g2.sendBuffer();         // transfer internal memory to the display
   delay(1);
}