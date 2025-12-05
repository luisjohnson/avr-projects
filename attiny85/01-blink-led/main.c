#ifdef __AVR_ATtiny85__
#include <avr/io.h>
#else
#error "This example requires -mmcu=attiny85 or __AVR_ATtiny85__ defined"
#endif
#include <util/delay.h>

int main()
{
  // set PB3 to be output
  DDRB = 0b00001000;
  while (1) {  
    // flash# 1:
    // set PB3 high
    PORTB = 0b00001000; 
    _delay_ms(20);
    // set PB3 low
    PORTB = 0b00000000;
    _delay_ms(20);

    // flash# 2:
    // set PB3 high
    PORTB = 0b00001000; 
    _delay_ms(200);
    // set PB3 low
    PORTB = 0b00000000;
    _delay_ms(200);
  }
 
  return 1;
}
