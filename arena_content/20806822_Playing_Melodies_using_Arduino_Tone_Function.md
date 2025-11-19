Published  July 4, 2017
12
Aswinth Raj
Author
Arduino is an excellent way to simplify and speed up your microcontroller projects, thanks to its community of developers who have made almost everything look simple. There are lots of Arduino Projects out here for you to try and have fun. Some of your projects might need some sounds action to notify about something or just to impress the viewers. What if I told you that almost any theme songs that could be played on a piano can be mimicked on your Arduino with the help of a simple program and a cheap Piezo speaker?
In this tutorial we will learn how simple and easy it is to Play Melody on Piezo Buzzer or Speaker using the Arduino tone () function. At the end of this tutorial you will be able to play some famous tones of Pirates of Caribbean, Crazy Frog, Super Mario and Titanic. You will also learn how to play any piece of piano music with Arduino. Check the Video at the end.
Hardware Required:
Arduino (any version – UNO is used here)
Piezo Speaker/Buzzer or any other 8ohm speaker.
Breadboard
Connecting Wires
Push buttons
1k resistor (optional)
Understanding the Tone() function of Arduino:
Before we can understand how a tone () works we should know how a Piezo buzzer works. We might have learnt about Piezo crystals in our school, it is nothing but a crystal which converts mechanical vibrations into electricity or vice versa. Here we apply a variable current (frequency) for which the crystal vibrates thus producing sound. Hence in order to make the Piezo buzzer to make some noise we have to make the Piezo electric crystal to vibrate, the pitch and tone of noise depends on how fast the crystal vibrates. Hence the tone and pitch can be controlled by varying the frequency of the current.
Okay, so how do we get a variable frequency from Arduino? This is where the tone () function comes in.  The tone () can generate a particular frequency on a specific pin. The time duration can also be mentioned if required. The syntax for tone () is
Syntax
tone(pin, frequency)
tone(pin, frequency, duration)
Parameters
pin: the pin on which to generate the tone
frequency: the frequency of the tone in hertz - unsigned int
duration: the duration of the tone in milliseconds (optional) - unsigned long
The values of pin can be any of your digital pin. I have used pin number 8 here. The frequency that can be generated depends on the size of the timer in your Arduino board. For UNO and most other common boards the minimum frequency that can be produced is 31Hz and the maximum frequency that can be produced is 65535Hz. However we humans can hear only frequencies between 2000Hz and 5000 Hz.
The pitches.h header file:
Now, we know how to produce some noise using the arduino tone() function. But, how do we know what kind of tone will be generated for each frequency?
Arduino have given us a note table which equates each frequency to a specific musical note type. This note table was originally written by Brett Hagman, on whose work the tone() command was based. We will use this note table to play our themes. If you are someone familiar with sheet music you should be able to make some sense of this table, for others like me these are just another block of code.
#define NOTE_B0
31
#define NOTE_C1
33
#define NOTE_CS1 35
#define NOTE_D1
37
#define NOTE_DS1 39
#define NOTE_E1
41
#define NOTE_F1
44
#define NOTE_FS1 46
#define NOTE_G1
49
#define NOTE_GS1 52
#define NOTE_A1
55
#define NOTE_AS1 58
#define NOTE_B1
62
#define NOTE_C2
65
#define NOTE_CS2 69
#define NOTE_D2
73
#define NOTE_DS2 78
#define NOTE_E2
82
#define NOTE_F2
87
#define NOTE_FS2 93
#define NOTE_G2
98
#define NOTE_GS2 104
#define NOTE_A2
110
#define NOTE_AS2 117
#define NOTE_B2
123
#define NOTE_C3
131
#define NOTE_CS3 139
#define NOTE_D3
147
#define NOTE_DS3 156
#define NOTE_E3
165
#define NOTE_F3
175
#define NOTE_FS3 185
#define NOTE_G3
196
#define NOTE_GS3 208
#define NOTE_A3
220
#define NOTE_AS3 233
#define NOTE_B3
247
#define NOTE_C4
262
#define NOTE_CS4 277
#define NOTE_D4
294
#define NOTE_DS4 311
#define NOTE_E4
330
#define NOTE_F4
349
#define NOTE_FS4 370
#define NOTE_G4
392
#define NOTE_GS4 415
#define NOTE_A4
440
#define NOTE_AS4 466
#define NOTE_B4
494
#define NOTE_C5
523
#define NOTE_CS5 554
#define NOTE_D5
587
#define NOTE_DS5 622
#define NOTE_E5
659
#define NOTE_F5
698
#define NOTE_FS5 740
#define NOTE_G5
784
#define NOTE_GS5 831
#define NOTE_A5
880
#define NOTE_AS5 932
#define NOTE_B5
988
#define NOTE_C6
1047
#define NOTE_CS6 1109
#define NOTE_D6
1175
#define NOTE_DS6 1245
#define NOTE_E6
1319
#define NOTE_F6
1397
#define NOTE_FS6 1480
#define NOTE_G6
1568
#define NOTE_GS6 1661
#define NOTE_A6
1760
#define NOTE_AS6 1865
#define NOTE_B6
1976
#define NOTE_C7
2093
#define NOTE_CS7 2217
#define NOTE_D7
2349
#define NOTE_DS7 2489
#define NOTE_E7
2637
#define NOTE_F7
2794
#define NOTE_FS7 2960
#define NOTE_G7
3136
#define NOTE_GS7 3322
#define NOTE_A7
3520
#define NOTE_AS7 3729
#define NOTE_B7
3951
#define NOTE_C8
4186
#define NOTE_CS8 4435
#define NOTE_D8
4699
#define NOTE_DS8 4978
Above code is given in pitches.h header file in this zip file, you just need to download and include this file in our Arduino code as given at the end this tutorial or use the code given in the zip file.
Playing Musical Notes on Arduino:
To play a decent melody using Arduino we should know what constitutes these melodies. The three main factors required to play a theme are
Note value
Note Duration
Tempo
We have the pitches.h header file to play any note value, now we should find out its specific note duration to play it. Tempo is nothing but how fast the melody should be played. Once you know the Note value and Note duration you can use them with the tone() like
tone (pinName, Note Value, Note Duration);
For the tones played in this tutorial I have given you the note Value and Note duration inside the “themes.h” header file using which you can play them in your projects. But if you have any specific tone in your mine and you want to play it in your project read on.... Else skip this topic and fall down to the next.
To play any specific tone you have to get the sheet music of that particular music and convert sheet music to Arduino sketch by reading the note value and note duration from it.  If you are a musical student it would be a piece of cake for you, else spent some time and break you head like I did. But at the end of the day when your tone plays on the Piezo buzzer you will find your effort worth it.
Once you have the note value and note duration, load them into the program inside the “themes.h” header file as shown below
//##############**"HE IS A PIRATE" Theme song of Pirates of caribbean**##############//
int Pirates_note[] = {
NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4,
NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4,
NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_D4,
NOTE_A3, NOTE_C4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_E4, NOTE_F4, NOTE_F4,
NOTE_F4, NOTE_G4, NOTE_E4, NOTE_E4, NOTE_D4, NOTE_C4, NOTE_C4, NOTE_D4,
0, NOTE_A3, NOTE_C4, NOTE_B3, NOTE_D4, NOTE_B3, NOTE_E4, NOTE_F4,
NOTE_F4, NOTE_C4, NOTE_C4, NOTE_C4, NOTE_C4, NOTE_D4, NOTE_C4,
NOTE_D4, 0, 0, NOTE_A3, NOTE_C4, NOTE_D4, NOTE_D4, NOTE_D4, NOTE_F4,
NOTE_G4, NOTE_G4, NOTE_G4, NOTE_A4, NOTE_A4, NOTE_A4, NOTE_A4, NOTE_G4,
NOTE_A4, NOTE_D4, 0, NOTE_D4, NOTE_E3, NOTE_F4, NOTE_F4, NOTE_G4, NOTE_A4,
NOTE_D4, 0, NOTE_D4, NOTE_F4, NOTE_E4, NOTE_E4, NOTE_F4, NOTE_D4
};
int Pirates_duration[] = {
4,8,4,8,4,8,8,8,8,4,8,4,8,4,8,8,8,8,4,8,4,8,
4,8,8,8,8,4,4,8,8,4,4,8,8,4,4,8,8,
8,4,8,8,8,4,4,8,8,4,4,8,8,4,4,8,4,
4,8,8,8,8,4,4,8,8,4,4,8,8,4,4,8,8,
8,4,8,8,8,4,4,4,8,4,8,8,8,4,4,8,8
};
//###########End of He is a Pirate song#############//
The above block of code shows the note value and note duration of “He is a Pirate” theme form the movie Pirates of the Caribbean. You can add your theme similarly like this.
Schematic and Hardware:
The schematic of this Arduino Tone Generator Project project is shown in the figure below:
The connection is pretty simple we have a Piezo speaker which is connected to pin 8 and Ground of the Arduino through a 1K resistor. This 1k resistor is a current limiting resistor, which is used to keep the current within the safe limits. We also have four switches to select the required melody. One end of the switch is connected to ground and the other end is connected to pin 2, 3, 4 and 5 respectively. The switches will have pull up resistors enabled internally using the software. Since the circuit is pretty simple it can be connect using a bread board as shown below:
Arduino Program Explanation:
Once you have understood the concept, the Arduino program is pretty straight forward.  The complete code is given at the end of the tutorial. If you are not familiar with adding header files you can download the code as a ZIP file from here and directly upload it to your Arduino.
The above two are the header files that have to be added. “pitches.h” is used to equate each musical note to a particular frequency and “themes.h” contains the note value and note duration of all the four tones.
#include "pitches.h"
#include "themes.h"
A function is created to play each tone when required. Here when the function Play_Pirates() is called the “He is a Pirate” tone will be played. This function consists of the tone function which produces the frequency at pin number 8. The noTone(8) is called to stop the music once it’s played.  If you want to play your own tone, change the Pirates_note and Pirates_duration to the new note and duration values that you have saved in “themes.h” value
void Play_Pirates()
{
for (int thisNote = 0; thisNote < (sizeof(Pirates_note)/sizeof(int)); thisNote++) {
int noteDuration = 1000 / Pirates_duration[thisNote];//convert duration to time delay
tone(8, Pirates_note[thisNote], noteDuration);
int pauseBetweenNotes = noteDuration * 1.05; //Here 1.05 is tempo, increase to play it slower
delay(pauseBetweenNotes);
noTone(8);
}
}
The pin 2, 3, 4 and 5 are used to select the particular tone to be played. These pins are held high by default using the internal pull up resistors by using the above line of code. When the button is pressed it is pulled down to ground.
pinMode(2, INPUT_PULLUP);
pinMode(3, INPUT_PULLUP);
pinMode(4, INPUT_PULLUP);
pinMode(5, INPUT_PULLUP);
Below block of code is used to play the song when a button is pressed. It reads the digital value of each button and when it gets low (zero) it assumes that the button is pressed and plays the respective tone by calling the required function.
if (digitalRead(2)==0)
{ Serial.println("Selected -> 'He is a Pirate' ");
Play_Pirates();
}
if (digitalRead(3)==0)
{ Serial.println("Selected -> 'Crazy Frog' ");
Play_CrazyFrog();
}
if (digitalRead(4)==0)
{ Serial.println("Selected -> 'Mario UnderWorld' ");
Play_MarioUW();
}
if (digitalRead(5)==0)
{ Serial.println("Selected -> 'He is a Pirate' ");
Play_Pirates();
}
Working of this Melody Player Arduino Circuit:
Once your Code and Hardware is ready, simply burn the program into your Arduino and you should be able to play the tone by simply pressing the buttons. If you have any problems take a look at your serial monitor for debugging or use the comment section to report the problem and I will be happy to help you out.
The complete working of the project is shown in the video below. Hope you enjoyed the project and would use it in some of your project or create a new tone for your project. If yes feel free to share your work in the comment section.
Complete Project Code
Copy Code
#include "pitches.h" //add Equivalent frequency for musical note
#include "themes.h" //add Note vale and duration
void Play_Pirates()
{
for (int thisNote = 0; thisNote < (sizeof(Pirates_note)/sizeof(int)); thisNote++) {
int noteDuration = 1000 / Pirates_duration[thisNote];//convert duration to time delay
tone(8, Pirates_note[thisNote], noteDuration);
int pauseBetweenNotes = noteDuration * 1.05; //Here 1.05 is tempo, increase to play it slower
delay(pauseBetweenNotes);
noTone(8); //stop music on pin 8
}
}
void Play_CrazyFrog()
{
for (int thisNote = 0; thisNote < (sizeof(CrazyFrog_note)/sizeof(int)); thisNote++) {
int noteDuration = 1000 / CrazyFrog_duration[thisNote]; //convert duration to time delay
tone(8, CrazyFrog_note[thisNote], noteDuration);
int pauseBetweenNotes = noteDuration * 1.30;//Here 1.30 is tempo, decrease to play it faster
delay(pauseBetweenNotes);
noTone(8); //stop music on pin 8
}
}
void Play_MarioUW()
{
for (int thisNote = 0; thisNote < (sizeof(MarioUW_note)/sizeof(int)); thisNote++) {
int noteDuration = 1000 / MarioUW_duration[thisNote];//convert duration to time delay
tone(8, MarioUW_note[thisNote], noteDuration);
int pauseBetweenNotes = noteDuration * 1.80;
delay(pauseBetweenNotes);
noTone(8); //stop music on pin 8
}
}
void Play_Titanic()
{
for (int thisNote = 0; thisNote < (sizeof(Titanic_note)/sizeof(int)); thisNote++) {
int noteDuration = 1000 / Titanic_duration[thisNote];//convert duration to time delay
tone(8, Titanic_note[thisNote], noteDuration);
int pauseBetweenNotes = noteDuration * 2.70;
delay(pauseBetweenNotes);
noTone(8); //stop music on pin 8
}
}
void setup() {
pinMode(2, INPUT_PULLUP); //Button 1 with internal pull up
pinMode(3, INPUT_PULLUP); //Button 2 with internal pull up
pinMode(4, INPUT_PULLUP); //Button 3 with internal pull up
pinMode(5, INPUT_PULLUP); //Button 4 with internal pull up
Serial.begin(9600);
}
void loop() {
if (digitalRead(2)==0)
{ Serial.println("Selected -> 'He is a Pirate' ");  Play_Pirates();  }
if (digitalRead(3)==0)
{ Serial.println("Selected -> 'Crazy Frog' ");  Play_CrazyFrog();  }
if (digitalRead(4)==0)
{ Serial.println("Selected -> 'Mario UnderWorld' ");  Play_MarioUW();  }
if (digitalRead(5)==0)
{ Serial.println("Selected -> 'Titanic' ");  Play_Titanic();  }
}
Video
Tags
arduino
arduino uno
speaker
buzzer
Have any question related to this Article?
Start a Discussion on:
WhatsApp
Telegram
Discord
Forum
Comments
I Need more obvious explantion on how to convert the note to frequency and length of tone please
Log in or register to post comments
You can know more about it here
https://github.com/nseidle/AxelF_DoorBell/wiki/How-to-convert-sheet-music-into-an-Arduino-Sketch
Log in or register to post comments
Hi, thanks for this great project idea. While I was wiring my project I noticed that the buttons wouldn't work unless they were grounded.
Log in or register to post comments
Yes Zahava, one end of the button should be grounded as shown in the curcuit diagram.
Log in or register to post comments
Tone continuously ringing and doesn't stop. How can i solve it?
Log in or register to post comments
Has the program uploaded successfully? Check if you have connected the right pin to the speaker
Log in or register to post comments
Thank you for sharing this project, excellent information on the Tone function and on Piezo devices.
Log in or register to post comments
I have a problem uploading. When I uploaded the code, it says this Redefinition of 'int Pirate_notes[]'.
Please help thankyou :)
Log in or register to post comments
Did you alter the code in someway?
Log in or register to post comments
Hi there
Firstly, thank you for the thorough tutorial! The way you broke down the steps really helped me understand what was going on (well, a little more than I did before, which isn't much to be honest).
My questions are this:
Is there a way to increase the sound. I am using the correct resistors but my sound if very soft. if I remove the resistor, I can hear the Pziezo really struggles.
Secondly, is there a way to have one button (button pin 2) cycle through songs being played. e.g. I press the button, the first song plays. I press it again, the second song, third time, the 3rd song and so on.
Log in or register to post comments
Firstly, thank you for the thorough tutorial! The way you broke down the steps really helped me understand what was going on (well, a little more than I did before, which isn't much to be honest).
Thank you for your words, well yes I dint wanna pump too much of information as it might get boring to read.
Is there a way to increase the sound. I am using the correct resistors but my sound if very soft. if I remove the resistor, I can hear the Pziezo really struggles.
Don't remove the resistor just decrease the value of it. If you want much better sound you should try an audio amplifier circuit, which might be a bit of overkill but if you are into learning things then its worth giving a shot.
Secondly, is there a way to have one button (button pin 2) cycle through songs being played. e.g. I press the button, the first song plays. I press it again, the second song, third time, the 3rd song and so on.
Yes, it is possible but not with the digital pin. You have to use an analog pin and form a potential divider with different values of resistors with each switch, this way when each switch is pressed a different voltage will be supplied to the analog pin using which we can detect which button was pressed.
Log in or register to post comments
1.6.7 version does not run these code. Any help?
Log in or register to post comments
Add New Comment
Comment *
Login to Comment
Sign in with Google
Log in with Facebook
Sign in with GitHub
Log in or register to post comments