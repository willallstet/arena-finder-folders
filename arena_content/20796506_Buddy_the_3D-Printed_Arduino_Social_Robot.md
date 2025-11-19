×Embed the widget on your own siteAdd the following snippet to your HTML:<iframe frameborder='0' height='385' scrolling='no' src='https://www.hackster.io/slantconcepts/buddy-the-3d-printed-arduino-social-robot-ec3dca/embed' width='350'></iframe>A desktop interactive 3D-printed Arduino social robotics kit for fun and STEM education.Read up about this project on Buddy, the 3D-Printed Arduino Social RobotSlant Concepts90 23,064 OverviewThingsStorySoftwareDesignElectronicsSchematicsCodeCreditsComments(12)Slant ConceptsPublished September 18, 2019 © CC BY-NC-NDBuddy, the 3D-Printed Arduino Social RobotA desktop interactive 3D-printed Arduino social robotics kit for fun and STEM education.IntermediateShowcase (no instructions)23,064Things used in this project Hardware componentsLittleArm Mason 3D Printer×1LittleArm Gotech 9025 9G Arduino Servo×1LittleArm Arduino Robotics Board×1Arduino Nano R3×1Buy from NewarkBuy from CPCSoftware apps and online servicesArduino IDEHand tools and fabrication machines3D Printer (generic)Story LittleBot Buddy is the 9th robot that we have made at LittleBots. We have been working to make robotics and STEM exciting and fun. And it hasn't changed with Buddy. Except now anyone can enjoy this robot. Whether you are a builder or not. You can just "hang out" with Buddy.Buddy is live now on Kickstarter. Please help us continue to grow on this project.When we started looking for what our next robot would be, we wanted to start moving closer to home. We wanted a make a robot that wouldn't just be for the classroom or workbench. We wanted a bot that we would enjoy just having around all day at our desk. A robot anyone can enjoy. As we worked on it we knew that we had to make a bot that you could fall in love with. It couldn't be an arm, or a little rover that would run out of battery. It would have to be a guy that you could interact with naturally and was always ready. We also knew that he couldn't be a robot, he had to be Alive. Alive, that was hard. We had to create a robot that would be spontaneous and that you could interact with and feel like he was listening to you and talking back.SoftwareThis was hard. The software is what makes Buddy come alive. It defines how he moves and responds.
It is pretty cool.The standard software that Buddy Comes with allows him to interact with you. He will see you and react. And he will be curious about his surroundings. He does this by constantly updating a map of his surroundings. So he will notice when you place an object near him. He will inspect it and figure out how big it is.Expanding on this, you can surprise and play with Buddy by placing and removing objects inside his space. Depending on how he is feeling that day we can be surprised, angry, or excited when he discovers the changes.Buddy generates all of his actions spontaneously. They are not prerecorded or predefined. He literally decided every single motion on the fly. And it is based on how he "feels" at any given time.This software will be available when it is fully complete. Currently attached to this project is an early draft of the arduino code currently used. It is functional but it doesn't have the full interactivity and smarts added yet.How Buddy SeesBuddy sees by updating certain waypoint in his area, And then inspecting items that pop up as he looks around. His eyes are not camera. They are a simple proximity sensor. But he uses to build a simple 3D map of the area around him.When he sees something in the worldview change. He will react to it. It is a simple system that we had to use some clever pieces of psychology to make it appear alive and more complex.Apps, Arduino and BlocklyThere is no app for this version of Buddy (though there might be one in our stretch goals). When he is built or pulled out of the Box he is ready to go. Just plug him in and then have fun.But Buddy is a STEM kit. He is meant to teach robotics and engineering and the psychology and interaction that comes with those in a way that is fun. What is better than building a robot that actually seems alive.Buddy can be reprogrammed. We will be posting code samples in Arduino and he is compatible with graphical systems like makeblock and Scratch. We want it to be easy to work with this little guy in and out of the classroom.
DesignCuteCute. That is how we wanted him to be described. Cute. We wanted you to say "Awwww" when you see him. He's like a potted plant that happens to be alive on your desk.SimpleThere are few bells and whistles.
The entire kit has fewer than 15 screws. Less than 25 parts total.This helps him stand up to the rigors of the classroom STEM groups. He can be picked up by his neck (not recommended) and likely not damaged. Buddy is really an exercise in minimalism. This makes him very robust.
Top Quality PartsThere is nothing "cheap" about this kit. Every decision was made to make a top quality product.The main board of Buddy is manufactured inside of the US and is a system that we have used in the last 8 of our robotics kits. It is solid and battle tested.The motors through Buddy, are top quality metal-geared servos used in performance RC aircraft. They are not typical off the shelf items. They are precision devices that can stand the test of time and the abuse they might suffer at the hands of kids.Buddy is fully 3D-printed. We made this choice because is allows Kids to do more than just program the robot. Seeing that he is 3D-printed invited them to print accessories or redesign him and then print those parts at school or a library. 3D printing opens the doors for more engineering thinking, which is the whole point of our kitsAssembly Tutorial for Building the BuddyElectronicsAs with all of our previous kits we have created the Buddy with the Meped
Board and arduino nano. This board is very flexible and is ideal for makers and students to expand the robot by adding more sensors and capabilities.There are 8 digital outputs that can run servos, buzzers, and LED's. And there are a number of analog inputs for adding more sensors. Along with bluetooth and IR inputs ready to go.With this board it is possible to add on Arms, sound sensors, and all kinds of other programmable devices.The Meped Arduino Robot Board
Buddy is live now on Kickstarter.Read moreSchematics Servo ConnectionsWhere to connect each of the Servos of BuddyCode Buddy V0.1Buddy V0.1C/C++This code is an early stable version that only has Buddy react to items in front of him. This does not yet have the deep emotions and reactions.//#include <mapping.h>
//started work on 9/19
// 1_0 worked well with botclock2_2
#include <Servo.h>
//arduino library
#include <math.h>
//standard c library
Servo baseServo;
Servo nodServo;
Servo tiltServo;
struct headPos {
int baseServoAngle;
int nodServoAngle ;
int tiltServoAngle ;
int desiredDelay ;
};
struct headPos faceMotion;
#define echoPin A2 // Echo Pin
#define trigPin A3 // Trigger Pin
//int desiredDelay = 16;
int ready = 0;
int randomNumber = 0;
// Define the default startup mode
int
robotMode = 700;
int buzzerTone = 500;
//+++++++++++++++ULTRASONIC VARIABLES++++++++++++++++++++++++++++
#define echoPin A2
// Echo Pin
#define trigPin A3
// Trigger Pin
#define buzzerPin 10
// Pin for the buzzer
bool holder = 1;
int maximumRange = 200;
// Maximum range needed
int minimumRange = 0;
// Minimum range needed
long readDistance;
// the output distance from the sensor
//+++++++++++++++FUNCTION DECLARATIONS+++++++++++++++++++++++++++
int ultraSensor(int theEchoPin, int theTrigPin);
void moveTo( struct headPos faceMotion);
void Speak3 (int soundPin, int currentTone, int finalTone);
void storedAction(int positionSelected, int theSpeed);
void speakWalter (int soundPin, int maxWords);
int servoParallelControl (int thePos, Servo theServo, int theSpeed );
void generateAction();
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
void setup()
{
Serial.begin(9600);
baseServo.attach(2);
nodServo.attach(3);
tiltServo.attach(4);
Serial.setTimeout(50);
//ensures the the arduino does not read serial for too long
Serial.println("started");
baseServo.write(90);
//intial positions of servos
nodServo.write(90);
tiltServo.write(90);
pinMode(trigPin, OUTPUT);
pinMode(echoPin, INPUT);
pinMode(buzzerPin, OUTPUT);
ready = 0;
noTone(buzzerPin);
}
void loop()
{
// read a usb command if available
if (Serial.available()) {
// read what type of a command will be sent
robotMode = Serial.parseInt();
if (robotMode == 200) {
faceMotion.baseServoAngle = Serial.parseInt();
faceMotion.nodServoAngle = Serial.parseInt();
faceMotion.tiltServoAngle = Serial.parseInt();
//buzzerTone = Serial.parseInt();
if (Serial.read() == '\n') {
// if the last byte is 'd' then stop reading and execute command 'd' stands for 'done'
Serial.flush();
//clear all other commands piled in the buffer
Serial.print('d');
//send completion of the command
}
}
}
//++++++++++++++++Decision of process to use+++++++++++++++++++++++++++
if (robotMode == 500) {
//Go Compeletely Silent
Serial.print('d');
//send completion of the command
Serial.flush();
//clear all other commands piled in the buffer
}
if (robotMode == 600) {
// Alarm Sequence
Serial.print('d');
//send completion of the command
Serial.flush();
//clear all other commands piled in the buffer
tone(buzzerPin, 1000);
//delay(5000);
noTone(buzzerPin);
}
if (robotMode == 700) {
//Normal Interaction Mode
Serial.print('d');
//send completion of the command
Serial.flush();
//clear all other commands piled in the buffer
//read the distance read by the sensor
readDistance = 100;//ultraSensor(echoPin, trigPin);
if (readDistance > 80) {
int nothingCount = 0;
generateAction();
//Check an area in the map
speakWalter(buzzerPin, random(1, 25));
//this is where all the fun starts
randomNumber = random(1, 10); // find a random whole number between the two values
int randomIterations = random (1,5);
//Serial.println(randomNumber);
//run through s set of random actions
int i;
for (i=1; i<randomIterations; i++){
generateAction();
}
//storedAction(randomNumber, 7);
}
else if (readDistance <= 6) {
// do something when this close
//fast response in surprise
}
else {
// occassionally check map and inspect world in general.
}
} // end of 700 if mode
// ---------------------------------------Act Upon Mode Type---------------------------------------------
//
//++++++++++++++++++Remote Mode++++++++++++++++++++++
//
if (robotMode == 200) {
//
//faceMotion.base
//
tone(buzzerPin, buzzerTone);
//
moveTo(faceMotion );
//
//servoParallelControl ( baseServoAngle, baseServo, 5 );
//
}
//
// ++++++++++++++++Speech Mode+++++++++++++++++++++
//
if (robotMode == 600) {
//
//speakWalter(buzzerPin, 50);
//
}
//
//
// ++++++++++++++++Stopped Mode+++++++++++++++++++++
//
if (robotMode == 700) {
//
//
}
} // end of primary loop
//++++++++++++++++++++++++++++++FUNCTION DEFINITIONS++++++++++++++++++++++++++++++++++++++++++
int ultraSensor(int theEchoPin, int theTrigPin) {
//this fucntion caluclates and returns the distance in cm
long duration, distance; // Duration used to calculate distance
/* The following trigPin/echoPin cycle is used to determine the
distance of the nearest object by bouncing soundwaves off of it. */
digitalWrite(theTrigPin, LOW);
delayMicroseconds(2);
digitalWrite(theTrigPin, HIGH);
delayMicroseconds(10);
digitalWrite(theTrigPin, LOW);
duration = pulseIn(theEchoPin, HIGH);
//Calculate the distance (in cm) based on the speed of sound.
distance = duration / 58.2;
return distance;
}
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++
void speakWalter (int soundPin, int maxWords) {
int toneDuration;
int numberOfWords;
int toneFreq;
// frequency of tone created
int phraseDelay;
// the time between individual statements
numberOfWords = random (1, maxWords);
//Serial.print("Number of words = ");
//Serial.println(numberOfWords);
// generate the random set of words
for ( int i; i <= numberOfWords; i++) {
toneDuration = random (25, 300);
toneFreq = random (200, 400);
tone(soundPin, toneFreq);
delay(toneDuration);
noTone(soundPin);
}
//phraseDelay = random(100, 10000);
//delay(phraseDelay);
//noTone(soundPin);
}
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++
void Speak2 (int soundPin, int maxWords, Servo Rot1, Servo Nod1, Servo Tilt1) {
//function that links servo motion to sound
int toneDuration;
int numberOfWords;
int toneFreq;
numberOfWords = random (1, maxWords);
//Serial.print("Number of words = ");
//Serial.println(numberOfWords);
for ( int i; i <= numberOfWords; i++) {
// randomly generate the tone durations and freq
toneDuration = random (25, 150);
toneFreq = random (100, 1800);
// use the tone durations to define servo movemnt
//large number of tones
tone(soundPin, toneFreq);
delay(toneDuration);
noTone(soundPin);
}
}
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++
void Speak3 (int soundPin, int currentTone, int finalTone) {
// has two notes meld into each other as a singer might
int toneDuration = 8;
//int numberOfWords;
//int toneFreq;
// frequency of tone created
//int phraseDelay;
// the time between individual statements
//numberOfWords = random (1,maxWords);
//Serial.print("Number of words = ");
//Serial.println(numberOfWords);
int theDiff = (finalTone - currentTone) / 5; //The difference between the values
if (theDiff > 0) {
// if ascending
for ( int i; i <= theDiff; i++) {
tone(soundPin, currentTone);
delay(toneDuration);
currentTone = currentTone + 5;
noTone(soundPin);
}
noTone(soundPin);
}
else {
theDiff = abs(theDiff);
for ( int i; i <= theDiff; i++) {
tone(soundPin, currentTone);
delay(toneDuration);
currentTone = currentTone - 5;
noTone(soundPin);
}
noTone(soundPin);
}
}
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
void moveTo( struct headPos faceMotion) {
int status1 = 0;
int status2 = 0;
int status3 = 0;
int done = 0 ;
while ( done == 0) {
//move the servo to the desired position
//this loop will cycle through the servos sending each the desired position.
//Each call will cause the servo to iterate about 1-5 degrees
//the rapid cycle of the loop makes the servos appear to move simultaneously
status1 = servoParallelControl(faceMotion.baseServoAngle, baseServo, faceMotion.desiredDelay);
status2 = servoParallelControl(faceMotion.nodServoAngle, nodServo, faceMotion.desiredDelay);
status3 = servoParallelControl(faceMotion.tiltServoAngle, tiltServo, faceMotion.desiredDelay);
//continue until all have reached the desired position
if (status1 == 1 & status2 == 1 & status3 == 1 ) {
done = 1;
}
}// end of while
}
//+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
int servoParallelControl (int thePos, Servo theServo, int theSpeed ) {
int startPos = theServo.read();
//read the current pos
int newPos = startPos;
//int theSpeed = speed;
//define where the pos is with respect to the command
// if the current position is less that the actual move up
if (startPos < (thePos - 5)) {
newPos = newPos + 1;
theServo.write(newPos);
delay(theSpeed);
return 0;
}
else if (newPos > (thePos + 5)) {
newPos = newPos - 1;
theServo.write(newPos);
delay(theSpeed);
return 0;
}
else {
return 1;
}
}
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
void generateAction() {
int waypoint = 0;
int theJoint = 0;
// one of the joints in a trajectory array
int trajSize = 0;
int theSpeed = 5;
struct headPos newPosition;
newPosition.desiredDelay = theSpeed;
delay (random (100, 1000)); //delay between ne motions
theSpeed = random (1, 7);
newPosition.tiltServoAngle = random (20, 150); //actually nod)
newPosition.baseServoAngle = random (10, 170);
newPosition.nodServoAngle = random (80, 150); //50 min j(bottom, top)
newPosition.desiredDelay = theSpeed;
moveTo (newPosition);
}
//++++++++++++++++++++++++++++
void checkMap() {
//randomly cycle and move to positions to check if there is any item at that location. (create behaviors for moving to those locations without the
}
//+++++++++++++++++++++++++++
void storedAction(int positionSelected, int theSpeed) {
int waypoint = 0;
int theJoint = 0;
// one of the joints in a trajectory array
int trajSize = 0;
struct headPos newPosition;
newPosition.desiredDelay = theSpeed;
if (positionSelected == 1) {
// up
int trajSize = 1;
int trajectory[trajSize][5] = {{101, 65, 153, 75, 5}
};
while (waypoint < trajSize) {
newPosition.tiltServoAngle = trajectory[waypoint][theJoint];
newPosition.baseServoAngle = trajectory[waypoint][theJoint + 1];
newPosition.nodServoAngle = trajectory[waypoint][theJoint + 2];
moveTo (newPosition);
waypoint++;
}
}
else if (positionSelected == 2) {
//shake
int trajSize = 9;
int trajectory[trajSize][5] = {{97, 65, 130, 75, 5}, {97, 101, 130, 75, 5}, {97, 71, 130, 75, 5}, {97, 114, 130, 75, 5}, {97, 70, 130, 75, 5}, {97, 107, 130, 75, 5}, {101, 79, 146, 75, 8}, {101, 56, 146, 75, 8}, {101, 81, 146, 75, 8}
};
while (waypoint < trajSize) {
newPosition.tiltServoAngle = trajectory[waypoint][theJoint];
newPosition.baseServoAngle = trajectory[waypoint][theJoint + 1];
newPosition.nodServoAngle = trajectory[waypoint][theJoint + 2];
moveTo (newPosition);
waypoint++;
}
}
else if (positionSelected == 6) {
//nod head
int trajSize = 9;
int trajectory[trajSize][5] = {{97, 70, 130, 75, 5}, {97, 70, 117, 75, 5} , {97, 70, 141, 75, 5}, {97, 70, 112, 75, 5}, {97, 70, 143, 75, 5}, {97, 70, 115, 75, 5}, {97, 70, 146, 75, 5}, {97, 70, 115, 75, 5}, {97, 70, 144, 75, 5}
};
while (waypoint < trajSize) {
newPosition.tiltServoAngle = trajectory[waypoint][theJoint];
newPosition.baseServoAngle = trajectory[waypoint][theJoint + 1];
newPosition.nodServoAngle = trajectory[waypoint][theJoint + 2];
moveTo (newPosition);
waypoint++;
}
}
else if (positionSelected == 7) {
//hang and shake
int trajSize = 5;
int trajectory[trajSize][5] = {{101, 65, 111, 75, 12}, {101, 99, 111, 75, 8} , {101, 43, 111, 75, 8}, {101, 101, 111, 75, 8}, {101, 48, 111, 75, 8}
};
while (waypoint < trajSize) {
newPosition.tiltServoAngle = trajectory[waypoint][theJoint];
newPosition.baseServoAngle = trajectory[waypoint][theJoint + 1];
newPosition.nodServoAngle = trajectory[waypoint][theJoint + 2];
moveTo (newPosition);
waypoint++;
}
}
else if (positionSelected == 9) {
//excited
int trajSize = 11;
int trajectory[trajSize][5] = {{89, 76, 143, 5, 5}, {114, 76, 143, 5, 5} , {87, 76, 143, 5, 5}, {114, 76, 143, 5, 5}, {88, 76, 143, 5, 5}, {121, 76, 143, 5, 5}, {91, 76, 143, 5, 5}, {115, 76, 143, 5, 5}, {88, 76, 143, 5, 5}, {117, 76, 143, 5, 5}, {96, 76, 143, 5, 5}
};
while (waypoint < trajSize) {
newPosition.tiltServoAngle = trajectory[waypoint][theJoint];
newPosition.baseServoAngle = trajectory[waypoint][theJoint + 1];
newPosition.nodServoAngle = trajectory[waypoint][theJoint + 2];
moveTo (newPosition);
waypoint++;
}
}
else if (positionSelected == 10) {
//Jump
int trajSize = 3;
int trajectory[trajSize][5] = {{97, 70, 160, 75, 10}, {97, 70, 65, 75, 1} , {97, 70, 130, 75, 5}
};
while (waypoint < trajSize) {
newPosition.tiltServoAngle = trajectory[waypoint][theJoint];
newPosition.baseServoAngle = trajectory[waypoint][theJoint + 1];
newPosition.nodServoAngle = trajectory[waypoint][theJoint + 2];
newPosition.desiredDelay = trajectory[waypoint][theJoint + 4];
moveTo (newPosition);
waypoint++;
}
}
else {
//nod head
int trajSize = 9;
int trajectory[trajSize][5] = {{97, 70, 130, 75, 5}, {97, 70, 117, 75, 5} , {97, 70, 141, 75, 5}, {97, 70, 112, 75, 5}, {97, 70, 143, 75, 5}, {97, 70, 115, 75, 5}, {97, 70, 146, 75, 5}, {97, 70, 115, 75, 5}, {97, 70, 144, 75, 5}
};
while (waypoint < trajSize) {
newPosition.tiltServoAngle = trajectory[waypoint][theJoint];
newPosition.baseServoAngle = trajectory[waypoint][theJoint + 1];
newPosition.nodServoAngle = trajectory[waypoint][theJoint + 2];
moveTo (newPosition);
waypoint++;
}
}
}
CreditsSlant Concepts 8 projects • 177 followersSlant is a group of makers and engineers creating robots and other gadgetsFollow
ContactContactComments
Related channels and tagshome automationtoys