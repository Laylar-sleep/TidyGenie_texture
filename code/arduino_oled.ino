
#include <Arduino.h>
#include <U8g2lib.h>

#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

U8G2_SSD1306_128X32_UNIVISION_F_SW_I2C u8g2(U8G2_R0, /* clock=*/ SCL, /* data=*/ SDA, /* reset=*/ U8X8_PIN_NONE);  

const char numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];    
boolean newData = false;

void setup(void) {
  Serial.begin(9600);
  u8g2.begin();
  u8g2.setFont(u8g2_font_VCR_OSD_tf); 
 
}

void loop(void) {
  u8g2.clearBuffer();          // clear the internal memory
  
  recvchar();
   if (newData == true) {
        strcpy(tempChars, receivedChars);
}
        // choose a suitable font
        showinfo();
  newData = false;
}


void recvchar(){
  static boolean recvInProgress = false;
    static int ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc=' ';
    
   while (Serial.available() > 0 && newData == false) {
   rc = Serial.read();        
       if (recvInProgress == true) {
       
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                 
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                //i=ndx;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }

}
void showinfo(){
 u8g2.drawStr(0,25,receivedChars);  // write something to the internal memory
  u8g2.sendBuffer();          // transfer internal memory to the display
  delay(1000);  
}
