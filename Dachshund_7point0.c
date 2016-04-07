#define LEFT_SENSOR_PIN A2
#define FRONT_SENSOR_PIN A5
#define RIGHT_SENSOR_PIN A0

#define DIR_PIN_1 3
#define STEPPER_PIN_1 2
#define DIR_PIN_2 7
#define STEPPER_PIN_2 6

#define A_BIT 30
#define NINETY_TO_STEPS 635 // was 660
#define ROOM_TO_STEPS 1770

#define LED_PIN 13

/*
	Each character holds the following information:
		North wall? (1) -- Bit 7
		East wall? (1) -- Bit 6
		South wall? (1) -- Bit 5
		West wall? (1) -- Bit 4
		Back pointer (2) -- Bits 3, 2
		Visited? (1) -- Bit 1
		Exhastively visited? (1) -- Bit 0
*/
char maze[16][16];

/*
	Directions: 0 = North
				1 = East
				2 = South
				3 = West
*/
char curDir = 1;
int row = 0, col = 0;

void setup() {
	pinMode(DIR_PIN_1, OUTPUT);
	pinMode(STEPPER_PIN_1, OUTPUT);
	pinMode(DIR_PIN_2, OUTPUT);
	pinMode(STEPPER_PIN_2, OUTPUT);
	pinMode(LED_PIN, OUTPUT);

	Serial.begin(9600);
	Serial.println("Ready.");

	initMaze();
}

void loop() {
	if (!isSolved())
		solveMaze();
}

void faceEast() {
	switch (curDir) {
		case 0:
			turnRight();
			break;
		case 1:
			break;
		case 2:
			turnLeft();
			break;
		case 3:
			turnAround();
			break;
		default:
			// TODO BAD ERROR
			break;
	}
	curDir = 1;
}

void faceNorth() {
	switch (curDir) {
		case 0:
			break;
		case 1:
			turnLeft();
			break;
		case 2:
			turnAround();
			break;
		case 3:
			turnRight();
			break;
		default:
			// TODO BAD ERROR
			break;
	}
	curDir = 0;
}

void faceSouth() {
	switch (curDir) {
		case 0:
			turnAround();
			break;
		case 1:
			turnRight();
			break;
		case 2:
			break;
		case 3:
			turnLeft();
			break;
		default:
			// TODO BAD ERROR
			break;
	}
	curDir = 2;
}

void faceWest() {
	switch (curDir) {
		case 0:
			turnLeft();
			break;
		case 1:
			turnAround();
			break;
		case 2:
			turnRight();
			break;
		case 3:
			break;
		default:
			// TODO BAD ERROR
			break;
	}
	curDir = 3;
}

char getBP() {
	return (maze[row][col] >> 2) & 3;
}

float getDist(int pin) {
	float volts = analogRead(pin) * 0.0048828125;
	float distance = 12.3 * pow(volts, -1.10);
	return distance;
}

void initMaze() {
	for (int i = 0; i < 16; ++i) {
		for (int j = 0; j < 16; ++j) {
			maze[i][j] = 0;
			if (i == 0)
				maze[i][j] |= (1 << 7);
			else if (i == 15)
				maze[i][j] |= (1 << 5);
			if (j == 0)
				maze[i][j] |= (1 << 4);
			else if (j == 15)
				maze[i][j] |= (1 << 6);
		}
	}
}

bool isCurrentVisited() {
	return (maze[row][col] >> 1) & 1;
}

bool isEV(char dir) {
	switch (dir) {
		case 0:
			return maze[row - 1][col] & 1;
		case 1:
			return maze[row][col + 1] & 1;
		case 2:
			return maze[row + 1][col] & 1;
		case 3:
			return maze[row][col - 1] & 1;
		default:
			return 0;
	}
}

bool isSolved() {
    // TODO 
    // Add checks to make sure that this room, and the adjacent three rooms
    // Have at least openings (Bonus if the openings create a 2 x 2 room. Will
    // involve moving). 
	return ((row == 7 || row == 8) && (col == 7 || col == 8));
}

bool isVisited(char dir) {
	switch (dir) {
		case 0:
			return (maze[row - 1][col] >> 1) & 1;
		case 1:
			return (maze[row][col + 1] >> 1) & 1;
		case 2:
			return (maze[row + 1][col] >> 1) & 1;
		case 3:
			return (maze[row][col - 1] >> 1) & 1;
		default:
			return 0;
	}
}

bool isWall(char dir) {
	switch (dir) {
		case 0:
			return (maze[row][col] >> 7) & 1;
		case 1:
			return (maze[row][col] >> 6) & 1;
		case 2:
			return (maze[row][col] >> 5) & 1;
		case 3:
			return (maze[row][col] >> 4) & 1;
		default:
			return 0;
	}
}

void moveOneRoom(char dir) {
        
	switch (dir) {
		case 0:
			faceNorth();
			--row;
			break;
		case 1:
			faceEast();
			++col;
			break;
		case 2:
			faceSouth();
			++row;
			break;
		case 3:
			faceWest();
			--col;
			break;
		default:
			break;
	}
	nextSquare();
}

void nextSquare() {
	stepForwardCarefully(ROOM_TO_STEPS);
	delay(300);
}

void rotate(boolean cw, int steps) {
	digitalWrite(DIR_PIN_1, cw);
	digitalWrite(DIR_PIN_2, cw);

	//delay(50);

	for (int i = 0; i < steps; ++i) {
		digitalWrite(STEPPER_PIN_1, HIGH);
		digitalWrite(STEPPER_PIN_2, HIGH);
		delayMicroseconds(500);
		digitalWrite(STEPPER_PIN_1, LOW);
		digitalWrite(STEPPER_PIN_2, LOW);
		delayMicroseconds(500);
	}
}

void setBP(char d) {
	/*
		N = 00
		E = 01
		S = 10
		W = 11
		Set BP to opposite of current direction.
	*/
	int N = 0;
	int E = 1;
	int S = 2;
	int W = 3;
	/*switch (d) {
		case 0:
			maze[row][col] |= (S << 2);
			break;
		case 1:
			maze[row][col] |= (W << 2);
			break;
		case 2:
			maze[row][col] |= (N << 2);
			break;
		case 3:
			maze[row][col] |= (E << 2);
			break;
		default:
			break;
	}*/
        char mask = (3 << 2);
        mask = ~mask;
        switch (d) {
             
		case 0:
			maze[row][col] = (maze[row][col] & mask) | (S << 2);
			break;
		case 1:
			maze[row][col] = (maze[row][col] & mask) | (W << 2);
			break;
		case 2:
			maze[row][col] = (maze[row][col] & mask) | (N << 2);
			break;
		case 3:
			maze[row][col] = (maze[row][col] & mask) | (E << 2);
			break;
		default:
			break;
	}
}

void setEV() {
	maze[row][col] |= 1;
}

void setVisited() {
	maze[row][col] |= (1 << 1);
}

void solveMaze(){
	bool backToTop = false;
	while (!isSolved()) {
		Serial.print(row);
		Serial.print(", ");
		Serial.print(col);
		Serial.print(", ");
		Serial.print(maze[row][col]&255, BIN);
		Serial.print(", ");
		Serial.println(maze[row][col+1]&255, BIN);
		backToTop = false;
		if(!isCurrentVisited()) {
			updateWalls();
			setVisited();
		}
		for (char i = 0; i < 4; i ++) {
			//if (!(isWall(i) || (getBP() == i) || isEV(i))) 
			if ( !(isWall(i) || (getBP() == i) || isEV(i) || isVisited(i)) ) {
				moveOneRoom(i);
				setBP(curDir);
				backToTop = true;
				break;
			}
		}
		if (!backToTop) {
			setEV();
			moveOneRoom(getBP());
		}
	}
	digitalWrite(LED_PIN, HIGH);
	char prev_bp = getBP();
        moveOneRoom(prev_bp);
        while (!(row == 0 && col == 0)) {
		//char bp = getBP();
		//moveOneRoom(bp);
                
                char after_bp = getBP();
                setBP(prev_bp);
                Serial.print("first printing ");
                Serial.print(row);
		Serial.print(", ");
		Serial.print(col);
		Serial.print(", ");
		Serial.print(maze[row][col]&255, BIN);
                Serial.print(" after_bp: ");
                Serial.print((int)after_bp);
                Serial.print("\n");
                for (char i = 0; i < 4; i ++) {
			//if (!(isWall(i) || (getBP() == i) || isEV(i))) 
			if ( !(isWall(i) || (getOppDir(prev_bp)==i) || isEV(i) || (i==after_bp) || getDiffBP(i)==getOppDir(i)) && isVisited(i) ) {
				after_bp = i;
				break;
			}
		}
                moveOneRoom(after_bp);
                prev_bp = after_bp;
           
	}
        //setBP(getOppDir(prev_bp));
        //setBP(getOppDir(prev_bp));
       
        setBP(prev_bp);
        
        while (!isSolved()) {
          Serial.print("second printing ");
          Serial.print(row);
          Serial.print(", ");
	  Serial.print(col);
	  Serial.print(", ");
	  Serial.print(maze[row][col]&255, BIN);
          Serial.print("\n");
          moveOneRoom(getBP());
        }
        Serial.print("exited loop ");
	digitalWrite(LED_PIN, LOW);
	wipeAllVisited();
}

char getDiffBP(char d){
    switch(d){
       case  0:
         return (maze[row-1][col] >> 2) & 3;
         
       case  1:
         return (maze[row][col+1] >> 2) & 3;
         
      case  2:
         return (maze[row+1][col] >> 2) & 3;
         
     case  3:
         return (maze[row][col-1] >> 2) & 3;
     default :
         return 0;
    }
}

char getOppDir(char bp){
   switch(bp){
    case 0:
      return 2;        
    case 1:
      return 3;
    case 2:
      return 0;
    case 3:
      return 1;
    default:
      return 0;
   }
}

void stepForward(boolean dir, int steps) {
	digitalWrite(DIR_PIN_1, dir ? 1 : 0);
	digitalWrite(DIR_PIN_2, dir ? 0 : 1);

	for (int i = 0; i < steps; ++i) {
		digitalWrite(STEPPER_PIN_1, HIGH);
		digitalWrite(STEPPER_PIN_2, HIGH);
		delayMicroseconds(500);
		digitalWrite(STEPPER_PIN_1, LOW);
		digitalWrite(STEPPER_PIN_2, LOW);
		delayMicroseconds(500);
	}
}

void stepForwardCarefully(int steps) {
	/*
	int d = steps/10;
	for (int i = 0; i < 10; i++) {
		if (getDist(FRONT_SENSOR_PIN) > 5) {
			float L = getDist(LEFT_SENSOR_PIN);
			float R = getDist(RIGHT_SENSOR_PIN);
			if (L < 10) {
				if (L > 8.5)
					turnLeftABit();
				else if (L < 4.5)
					turnRightABit();
			}
			else if (R < 10) {
				if (R > 8.5)
					turnRightABit();
				else if (R < 4.5)
					turnLeftABit();
			}
			stepForward(true, d);
		}
		else
			return;
	}
	*/
	/*int count = 0;
	bool l, r;
	for (int i = 0; i < 10; ++i) {
		l = false;
		r = false;
		if (getDist(FRONT_SENSOR_PIN) < 5)
			break;
		if (getDist(LEFT_SENSOR_PIN) < 4.5) {
			rotate(true, NINETY_TO_STEPS/9);
			r = true;
			++count;
		}
		else if (getDist(RIGHT_SENSOR_PIN) < 4.5) {
			rotate(false, NINETY_TO_STEPS/9);
			l = true;
			++count;
		}
		stepForward(true, ROOM_TO_STEPS/10);
		if (r)
			rotate(false, NINETY_TO_STEPS/9);
		if (l)
			rotate(true, NINETY_TO_STEPS/9);
	}
	for (int i = 0; i < count; ++ i) {
		if (getDist(FRONT_SENSOR_PIN) < 5)
			break;
		stepForward(true, 60);
	}
	float front = getDist(FRONT_SENSOR_PIN);
	if ((front < 11) && (front > 5)) {
		stepForwardCarefully(ROOM_TO_STEPS/2);
	}*/
        //delay(600);
	int count = 0;
	boolean l, r;
        float rs, ls;
        float prev_ls, prev_rs;
        bool left = getDist(LEFT_SENSOR_PIN) < 12;
        bool right = getDist(RIGHT_SENSOR_PIN) < 12;
        bool flag = false;
	for (int i = 0; i < 10; ++i) {
		l = false;
		r = false;
                Serial.print(i);
                Serial.print("\n");
                rs = getDist(RIGHT_SENSOR_PIN);
                ls = getDist(LEFT_SENSOR_PIN);
                if (((left) && (ls > 12)) && !flag) {
                   i = 5;
                   left = !left;
                   flag = true;
                   stepForward(true, ROOM_TO_STEPS/20);
                }
                if (!left && (ls < 10) &&!flag){
                   i = 4;
                   left = !left;
                  flag = true; 
                }
                //if (!left && (ls < 10))
                //  i = 3;
                if (((right) && (rs > 12)) && !flag) {
                  i = 5;
                  right = !right;
                  flag = true;
                  stepForward(true, ROOM_TO_STEPS/20);
                }
                if (!right && (rs < 10) &&!flag){
                  right = !right;
                  i = 4;
                  flag = true;
                }
                //if (!right && (rs < 10))
                //  i = 3;
		if (getDist(FRONT_SENSOR_PIN) < 5)
			break;
		if (ls < 11) {
                  if(ls < 4.5){
			rotate(false, NINETY_TO_STEPS/5);
                        //delay(300);
			l = true;
			++count;
                  }
                  else if(ls > 9){ // was 9 previously
			rotate(true, NINETY_TO_STEPS/5);
                       // delay(300);
			++count;
                        r = true;
                  }
                  
             
		}
		else if (rs < 11) {
                 
                 if(rs > 9){//previously 9
                    rotate(false, NINETY_TO_STEPS/5);
                    //delay(300);
                    l = true;
	            ++count;
                  }
                 
                  
		}
                if(rs < 4.5){
			rotate(true, NINETY_TO_STEPS/5);
                       // delay(300);
			r = true;
			++count;
                }
		stepForward(true, ROOM_TO_STEPS/10);
		if (r)
			rotate(false, NINETY_TO_STEPS/10);
                       // delay(300);
		if (l)
			rotate(true, NINETY_TO_STEPS/10);
                        //delay(300);
                /*if (ls < 11 && prev_ls < 11 &&  i > 0){
                    if(prev_ls - ls > 1 && prev_ls - ls < 5){
                      rotate(false, NINETY_TO_STEPS/9);
                    }
                    else if(ls - prev_ls > 1 && ls - prev_ls < 5){
                      rotate(true, NINETY_TO_STEPS/9);
                    }
                 else if (rs < 11 && prev_rs < 11 && i > 0){
                    if(prev_rs - rs > 1 && prev_rs - rs < 5 ){
                      rotate(true, NINETY_TO_STEPS/9);
                    }
                    else if(rs - prev_rs > 1 && rs - prev_rs < 5){
                      rotate(false, NINETY_TO_STEPS/9);
                    }
                 }
                }
              Serial.print("right diff: ");
	      Serial.println(rs - prev_rs);
              Serial.print("left diff: ");
	      Serial.println(ls - prev_ls);
              stepForward(true, ROOM_TO_STEPS/10);
              prev_ls = ls;
              prev_rs = rs;
                  
	*/
    }
	for (int i = 0; i < count; ++ i) {
		if (getDist(FRONT_SENSOR_PIN) < 5)
			break;
		stepForward(true, 60);
	}
	float front = getDist(FRONT_SENSOR_PIN);
	if ((front < 10) && (front > 5)) {
		stepForwardCarefully(ROOM_TO_STEPS/2);
	}
}

void turnAround() {
	if (getDist(LEFT_SENSOR_PIN) < getDist(RIGHT_SENSOR_PIN)) {
		turnRight();
		turnRight();
	}
	else {
		turnLeft();
		turnLeft();
	}
}

void turnLeft() {
	rotate(true, NINETY_TO_STEPS);
}

void turnLeftABit() {
	rotate(true, A_BIT);
}

void turnRight() {
	rotate(false, NINETY_TO_STEPS);
}

void turnRightABit() {
	rotate(false, A_BIT);
}

void updateWalls() {
	bool left = getDist(LEFT_SENSOR_PIN) < 15;
	bool right = getDist(RIGHT_SENSOR_PIN) < 15;
	bool front = getDist(FRONT_SENSOR_PIN) < 10;
	switch (curDir) {
		case 0:
			maze[row][col] |= ((front << 7) | (left << 4) | (right << 6));
			break;
		case 1:
			maze[row][col] |= ((front << 6) | (left << 7) | (right << 5));
			break;
		case 2:
			maze[row][col] |= ((front << 5) | (left << 6) | (right << 4));
			break;
		case 3:
			maze[row][col] |= ((front << 4) | (left << 5) | (right << 7));
			break;
		default:
			break;
	}
}

void wipeAllVisited() {
	for (int i = 0; i < 16; ++i) {
		for (int j = 0; j < 16; ++j)
			maze[i][j] &= 253;
	}
}
