#include <wiringPi.h>
#include <stdio.h>
int main (void)
{
 wiringPiSetupGpio();
 pinMode(16,OUTPUT) ;
 for (;;)
 {
 digitalWrite(16,HIGH);
 printf("LED ON\n");
 delay(100);
 digitalWrite(16,LOW);
 printf("LED OFF\n");
 delay(100);
 }
 return 0 ;
}