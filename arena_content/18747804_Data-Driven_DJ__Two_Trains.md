Data-Driven DJ
by Brian Foo
Two TrainsSonification of Income Inequality on the NYC Subway
The goal of this song is to emulate a ride on the New York City Subway's 2 Train through three boroughs: Brooklyn, Manhattan, and the Bronx. At any given time, the quantity and dynamics of the song's instruments correspond to the median household income of that area. For example, as you pass through a wealthier area such as the Financial District, the instruments you hear in the song will increase in quantity, volume, and force. Stylistically, I want the song to exhibit the energy and orderly chaos of the NYC subway system itself.
The Song
Listen to the song by using the player above, or check out the song on Soundcloud if you prefer no visuals or would like to comment on a specific part of the song.
Read further down to learn more about how the song was constructed.
Composition & Style
The song composition is entirely algorithmic and is composed of five primary building blocks:
The 2 Train on theNYC Subway: I chose the 2 train because it goes through 3 different boroughs (Brooklyn, Manhattan, and the Bronx) and travels along Broadway, one of NYC's primary arteries. The geographical coordinates of each of the 2 Train's 49 stations are used to create 48 distinct segments in the song, where the length of each segment correlates to the actual distance of that subway station to the next one. In reality, it would take about 1 hour 45 minutes to complete the entire train ride, or about 2 minutes per station. For practical purposes, this song has been compressed to be about 4.5 minutes, which equates to a train going about 336 mph (540 kph) non-stop, where the average time per station/segment is about 5 seconds.
US Census Data for NYC: between 3 and 30 instruments are playing during each segment of this song. Some instruments play softly (i.e. piano/pianissimo) and some play loudly (i.e. forte/fortissimo.) The number and type of instruments are selected based on that station's surrounding median income taken from the 2011 US Census Data Release. In general, the higher the income, the greater the dynamics and quantity of instruments. To be as objective as possible, the same rules are applied throughout the whole song. Also, I tried to select agnostic sound traits (e.g. volume, force) to correlate to median income rather than biased ones (e.g. sad vs happy sounds, vibrant vs dull sounds) to further let the data "speak for itself." As a result, the loudest part of the song (1:37) occurs in the Financial District between Park Place and Chambers St. which had a median income of $205,192 in 2011. Compare this to the quietest part of the song (3:53) in the Bronx between E 180 St. and Bronx Park East where the median income was $13,750 in 2011.
The NYC Subway Chime : the door chime recognized by most New Yorkers is based on two notes (G# and E) in the globally recognizable Westminster Chimes
that you may have heard in school, church, or as a doorbell. The melody consists of different pitches in the key of E major (E, F#, G#, B). Most of the notes in my song also come from this scale.
New York Counterpoint : the minimalist composition by the renowned American composer Steve Reich, a New York native, is performed with 11 pulsating clarinets and bass clarinets. I modeled this song after Reich's composition because it beautifully captures the throbbing vibrancy New York and the movement of its citizens. My song contains 40 clarinet and bass clarinet samples playing different octaves of notes in the D major chord
(D, F#, A) and E major chord
(E, G#, B) which happens to have significant presence in both New York Counterpoint and the Westminster Chimes (and thus the NYC Subway chime; see previous point).
Phase Shifting : in relation to music, phase shifting is a compositional approach in which two or more identical melodies are repeated with slightly variable tempos, so the melodies would slowly shift in and out of sync with each other. This technique was pioneered in the 1960s by Terry Riley and Steve Reich by experimenting with tape looping. I felt this was the perfect metaphor for the NYC Subway: constantly looping but at different tempos, always running but never on time, phasing between order and chaos. All the instruments that you hear in this song implement the approach of phase shifting.
Sounds Used
63 samples were used in this song. As much as I could, I chose sounds that were created by NYC-based musicians to be consistent with the New York theme. 16 samples of songs by NYC musicians were used for the percussion and vocal sounds. Additionally, there are 20 clarinet samples, 20 bass clarinet samples, 6 xylophone samples, and 1 train horn sample. No sounds were performed by me, and no sounds were computer-generated. The sources of all samples are listed below:
Shaker
in Cha chaka cha cha by Angelica Negron, a composer and multi-instrumentalist currently based in Brooklyn, New York.
Bongos
and Kick
in Keep U by Erick Arc Elliott, a rapper, producer, songwriter, and musician from the Flatbush area of Brooklyn, New York. He is also a member of the Flatbush Zombies.
Drum
and Bass
in Keep On Running by Gabriel Garzón-Montano, an R&B artist based in Brooklyn, New York.
Kick in
in Bellybuttons T&A by Brooklyn Funk Essentials, an NYC-based music collective who mix jazz, funk, and hip hop.
Beatbox
in Man vs. Machine by Rahzel, originally from New York City, arguably one of the best beatboxers of all time.
Vocals
in Say You by Lesley Flanigan an experimental electronic musician living in New York City.
Subway Train Horn
via Youtube; this also happens to be the horn of a 2 Train.
Xylophone set
via Freesound , a collaborative database of Creative Commons Licensed sounds.
All 40 clarinet
and bass clarinet
samples have been taken from the amazing Philharmonia sound sample library, thousands of free, downloadable sound samples specially recorded by Philharmonia Orchestra players.
Data Used & Prior Work
Much of the inspiration for this project came from The New Yorker's interactive piece Inequality and New York's Subway. The data for each of our resulting pieces came from the following places:
Census Bureau American Community Survey 2011 Release to obtain the median income of a particular neighborhood in NYC. The survey provides a wide range of important statistics about our nation's people, housing and economy for all communities in the country. You can peruse the data using the US Census FactFinder. You can view the final processed data that I used here.
Subway entrances via NYC Open Data to obtain the geographic coordinates of each subway station. You can also view the final processed data that I used here.
Tools & Process
This song was algorithmically generated in that I wrote a computer program that took data and music samples as input and generated the song as output. I did not manually compose any part of this song.
For those interested in replicating, adapting, or extending my process, all of the code and sound files is open source and can be found here. It also contains a comprehensive README to guide you through the setup and configuration. The following is a brief outline of my process:
Based on the project's objective, I decided upon a stylistic and compositional approach.
I scoured the internet for songs from NYC musicians or songs about NYC. I then extracted individual instrument samples from strong candidates.
Using the data from the previous section, I generated two spreadsheets:
A list of train stations along the 2 Train and their corresponding median income and geographic coordinates
A list of instruments and their corresponding "price", sample file, volume, and tempo.
Using Python, a widely used programming language, I:
Calculated the distance between each train
Assigned instruments to each station based on that station's median income
Generated a sequence of sounds using the relative distances and instruments determined above.
The sequence of sounds from the previous step was fed into ChucK, a programming language for real-time sound synthesis and music creation. I used ChucK because it is really good at generating strongly-timed sequences. The output would then be an audio file that I could listen to.
I then repeated the previous steps numerous times, tweaking the sounds and the algorithms until I was satisfied with the result
I used Processing, a programming language with a visual focus, to generate the visualization using the data above.
If you happen to use my code and create something new, please shoot me an email at hello@brianfoo.com. I'd love to see and share your work!
Q&A
In this section, I will document answers to select questions I've received after the initial post.
Why income inequality?
I was looking for a dataset that would yield a song with some exciting ups and downs, and ideally, would relate to a topic that is relevant and current. When I was looking at a graph of income inequality along the 2 Train, it looked like the perfect song composition with a build-up, climax, and falling action. I thought the subway train would be the perfect vehicle for this type of project because the sonification of data requires the passing of time. So instead of looking at the data all at once on a chart, with a song, you can ride and experience the data as if you were actually taking the train.
Why New York City?
New York City has a particularly large problem with income inequality compared to other cities. To add some personal bias, I've lived here for a little more than a decade. The city has also been a recurring subject in a lot of my recent work, both personally and professionally (I work at The New York Public Library Labs during the day.) Practically speaking, the city provides some great resources like NYC Open Data for playing with its data. That's how I got the subway-specific data to create the song.
Is your intent to make the experience of income inequality exciting in a pleasant way?
I was a bit conflicted about this.
On one hand, I wanted to make a pleasant/exciting-sounding song so it could be palatable for the casual listener and experienced independently from the topic of income inequality.
I felt this would be a valid goal as long as I apply the same rules across the whole song, and I don't make subjective statements like "wealthy neighborhoods should sound like this" or "poor neighborhoods should sound like that." I didn't want to be accused of favoring one area of the city or the other because one sounds "prettier" than the other. So instead of choosing sound traits that would affect mood or vibrancy, I tried to choose more agnostic ones like volume and dynamics.
In other words, the goal wasn't to make income inequality sound exciting or pleasant, but to demonstrate the immense contrast of income through the contrast of sound.
Questions & Feedback
I'd love to hear from you. I'm sure I've also made some erroneous statements somewhere, so please correct me. You can use the widget below or email me at hello@brianfoo.com.
Please enable JavaScript to view the comments powered by Disqus.
Data-Driven DJ is a series of music experiments that combine data, algorithms, and borrowed sounds.
My goal is to explore new experiences around data consumption beyond the written and visual forms by taking advantage of music's temporal nature and capacity to alter one's mood. Topics will range from social and cultural to health and environmental.
Each song will be made out in the open: the creative process will be documented and published online, and all custom software written will be open-source. Stealing, extending, and remixing are inevitable, welcome, and encouraged. Check out the FAQs for more information.
About me
My name is Brian Foo and I am a programmer and visual artist living and working in New York City. Learn more about what I do on my personal website. You can also follow my work on Twitter, Facebook, Soundcloud, or Vimeo.