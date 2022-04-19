#include <Mouse.h>
#include <SPI.h>

// Signed char can be between -128 to 127
int delta[2];
int deltaX;
int deltaY;

int negMax = -125;
int posMax = 125;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0)
  {
    // Read Data
    String data = Serial.readStringUntil('x');

    // Gets demarcation between deltaX and DeltaY
    int ohHiMarc = data.indexOf(':');

    // DeltaX & DeltaY
    delta[0] = data.substring(0, ohHiMarc).toInt();
    delta[1] = data.substring(ohHiMarc + 1).toInt();
    
    handleX(delta[0]);

    if (ohHiMarc != -1)
    {
      handleY(delta[1]);
    }
  }
}

// Handle Moving of x 
void handleX(int dx){
  
  int spawns; 
  int remainder;
  
  if(dx < negMax)
  {
    // How many times we move mouse
    spawns = int(dx / negMax); 
    
    // How much we move after for loop
    remainder = int(dx % negMax);

    // Because we can only move 125 at a time,
    // we need a for loop to spawn multiple mouse events.
    for(int i = 0; i < spawns; i++)
    {
      Mouse.move(negMax , 0, 0);
    }
    // Move Remainder
    Mouse.move(remainder, 0, 0);
  } 
  else if (dx >= negMax && dx <= posMax)
  {
    Mouse.move(dx, 0, 0);
  }
  else if (dx > posMax)
  {
    // How many times we move mouse
    spawns = int(dx / posMax); 
    
    // How much we move after for loop
    remainder = int(dx % posMax);
    
    for(int i = 0; i < spawns; i++)
    {
      Mouse.move(posMax , 0, 0);
    }
    // Move Remainder
    Mouse.move(remainder, 0, 0);
  }
  
}

// Handle Moving of x 
void handleY(int dy){
  
  int spawns; 
  int remainder;
  // MindTrip, Neg is pos & Pos is Neg for move, hence the inverted pos & Neg
  if(dy < negMax)
  {
    // How many times we move mouse
    spawns = int(dy / negMax); 
    
    // How much we move after for loop. -1 converts to correct direction on arduino (pos,neg,neg,pos)
    remainder = int(dy % negMax);
    remainder *= -1;
    // Because we can only move 125 at a time,
    // we need a for loop to spawn multiple mouse events.
    for(int i = 0; i < spawns; i++)
    {
      Mouse.move(0, posMax, 0);
    }
    // Move Remainder
    Mouse.move(0, remainder, 0);
  } 
  else if (dy >= negMax && dy <= posMax)
  {
    dy *= -1;
    Mouse.move(0, dy, 0);
  }
  else if (dy > posMax)
  {
    // How many times we move mouse
    spawns = int(dy / posMax); 
    
    // How much we move after for loop
    remainder = int(dy % posMax);
    remainder *= -1;
    
    for(int i = 0; i < spawns; i++)
    {
      Mouse.move(0, negMax, 0);
    }
    // Move Remainder
    Mouse.move(0, remainder, 0);
  }
  
}
