If you haven’t kept up with the world of e-ink displays, here’s some good news: they are pretty cheap now. For as little as $15 you can get a small e-ink display that has good enough performance and contrast to actually do something useful. There’s only one problem: figuring out how to drive them in your project.
Tired of seeing nothing but wiring diagrams and sample code when it came to actually putting these e-ink modules to use, [Jouko Strömmer] decided to try his hand at creating a turn-key application for these gorgeous little displays. The result is PaperTTY, a Python program that allows the user to open up a fully functional Linux virtual terminal on an e-ink display.
Of course, there are some caveats. For one, this all assumes you’re using a Waveshare display (specifically their 2.13 inch HAT) connected to a Raspberry Pi over SPI. Not to say that’s the only hardware combination that will work, but it’s the only one that [Jouko] has done any testing on at this point. If you want to try to shake things up in terms of hardware, you might need to get your hands dirty.
The advantage of being able to open a Linux VT on one of these e-ink displays is pretty simple: you can run basically any piece of software you want on it. Rather than having to come up with software that specifically features support for the display, you can just use (or write) standard Linux console programs. [Jouko] mentions a number of popular programs such as vim and irssi, but you could just as easily write a Bash script to dump whatever data you like to the screen.
In the video after the break [Jouko] shows PaperTTY in action for the doubters who think these sorts of displays are no good for interactive use. The display is very crisp and readable, with no signs of flickering. Overall he says the experience is not unlike using a slow SSH connection. It might not be how we’d like to use a computer full time, but we can definitely see the potential.
With the recent progress with Kindle hacking, it seems that interest in e-ink is as high as ever. Despite what the haters might claim, it’s a useful niche tech that still holds plenty of promise.
49 thoughts on “Run A Linux Terminal On Cheap E-Ink Displays”
The refresh speed on the video is impressive for an eInk display.
Report comment
Reply
I was thinking that too, the eDisplay I have seen so far were very slow. And most would do a fade-in/fade-out of some sort, annoying…
Report comment
Reply
Some Waveshare e-ink screens support partial refresh, which may be done as fast as 0.3 sec.
The inverting flickering is needed to get rid of the ghost-image of the previous image. When activating a pixel on an e-ink screen, it may alter the surrounding pixels a bit and rotating a pixel may not always be the exact meant rotation. So if you write the new image inverted first, each pixel will be refreshed and rotated by 180 degree, so any residual image will be lost.
When doing partial updates, you may get some garbage on screen which does resemble the typical JPEG artifacts a bit. (although entirely different cause)
So if you’re going to buy one, make sure to check the refresh rate, since some may take up-to 8 seconds to refresh. For example the screens with an extra color like red or yellow are very slow.
Report comment
Reply
The mono Waveshare ones are surprisingly fast (per the video), the 2-colour ones (black/white/red) are surprisingly slow – 20 seconds for a refresh!
Report comment
Reply
I recall an article on here, I think it might have been some madman running Doom on an e-ink display. It was configurable, the refresh rate got faster, if you chose to use fewer grey levels. In simple monochrome it was some small fraction of a second. There’s probably a lot of stuff to do with e-ink that people haven’t explored yet. If you can get 4-greys working fast enough you could even do a Gameboy emulator.
The invert-refresh thing gets rid of any leftover ghost pixels, but perhaps you could limit it to smaller areas, use a smart algorithm rather than the brute-force whole-screen refresh. Maybe even limited to single pixels, the user might not notice it. Again, I bet there’s possibilities.
Report comment
Reply
Ha – you’re going to convince me to work that project again. Here it was in 16 colors: https://www.youtube.com/watch?v=Fd8cFR_uTQM
Report comment
Reply
Check out what’s possible now: https://www.youtube.com/watch?v=EzBPBoBc9q4
Report comment
Reply
Typematrix keyboard !
Report comment
Reply
I just don’t get display sizes.
Why are they always only a single number? It’s the diagonal measurement right? If there was only one single standard height to width ration I would get it but are there not several? How does one design a project when you have to buy something just to find out what the actual dimensions are? Am I the only one who ever has specific requirements?
Report comment
Reply
They are often given as only a single number because of televisions. Originally the aspect ratio on a TV was more or less fixed so that it was treated as implicit, hence diagonal resolution was sufficient. This has persisted and spilled over into descriptions of other displays.
It’s stupid to specify diagonal size when aspect ratio is not known though, I agree.
Report comment
Reply
For displays it is still somewhat comprehensible what is meant by its value.
Image sensors have a totally different “diameter” value, which is based on the old tubes used in old cameras.
Those tubes had some outer diameter, which was used to define the size. However a 1″ tube means an image recording area of 12.8×9.6 mm, give or take, which is 16 mm in diameter. (about a factor of 1.6 smaller)
So the industry is still using dimensions dating back from the time an image tube that never recorded a pixel, to indicate the size of modern sensors. Even while we now have sensors that didn’t have a matching one in the era of tubes.
Report comment
Reply
I suspect if this disbalance didn’t sound favourable to them, they’d have switched to measurements that make sense. For now Sony is only happy to call their tiny sensors “one inch” and sell p&s cameras at absurd prices.
Report comment
Reply
Not only Sony. Almost all sensors not fitting another dimension like “APS-C” or “Full frame” or something similar, is using the very strange inch rating to give some idea of its dimensions.
For example Aptina, which is now On Semiconductor: http://www.onsemi.com/PowerSolutions/parametrics.do?id=101682
The sensors “sound” larger than they are, but the size indicator really doesn’t make sense.
Report comment
You should be referencing the full spec sheet/diagram for the product before buying it. I would hope that, generally speaking, you do more research on a component than reading its name.
Report comment
Reply
Dude, you only need the diagonal and the aspect ratio. Both of which should be easily available. You can tell the approximate aspect ratio just by looking. There’s only so many that are manufactured.
Once you’ve got that it’s just a simple bit of Pythagoras. Right-angled triangle.
Report comment
Reply
Man, I’m still hoping desperately that someday we get a 60Hz+ eink display.
I’d throw top-end laptop money at something I could use outside, even if it was mediocre in other ways.
Report comment
Reply
Have you seen the SHARP memory display? I’ve wondered if it would scale well and still be readable.
https://youtu.be/VmronCahqd8
Report comment
Reply
The biggest they make is 4.4 inch, which is a shame. OTOH you can get colour, only 8 different, muddy colours, but it’s still nifty!
Perhaps it’s one of those things where they don’t make bigger ones cos of lack of demand, and there’s no demand because they don’t make bigger ones. It’d take some huge company wanting loads of them, before they’d tool up to make bigger sizes.
Is there some size limit intrinsic to the technology?
Report comment
Reply
I just watched the interview, which is very informative by the way.
Sharp really does have some nice innovative ideas on displays.
My DV film camera, which I bought in 2005(???) was a Sharp and it had by far the best visible LCD imaginable in bright sunlight. You could just switch off the backlight and get more battery lifetime.
Too bad that didn’t catch on for other products.
As I understood from the talk, the screen is just a normal LCD in terms of the LC switching pixels, so there shouldn’t be a size limit on that.
There is of course the SRAM like transistor layout to address each pixel, which is incorporated into the same display. So maybe the production line isn’t capable yet of making large screens? Or perhaps the yields suffer for bigger displays?
Also these kind of displays are really meant to be used in low-power applications, which is typically wearable or to be used somewhere where power supply may be an issue. Typically that is for small devices, so I guess there really is no demand yet for bigger displays using this type of technology.
Report comment
Reply
Panasonic used to do toughbooks with reflexive displays. Not sure how high your ‘top-end laptop money’ goes though!
Report comment
Reply
Toughbooks were great we had many for work Only Laptop that i’ve come across with some good battery management and maintenance tools.
Report comment
Reply
To save others the search,
$17.99
https://www.waveshare.com/product/mini-pc/raspberry-pi/displays/2.13inch-e-paper-hat.htm
Report comment
Reply
“If you haven’t kept up with the world of e-ink displays, here’s some good news: they are pretty cheap now. For as little as $15 you can get a small e-ink display that has good enough performance and contrast to actually do something useful. ”
Well since the “you need more than one screen” fad is still going, place documentation on the E-ink, and work on the other. It’s not like the former’s going to be changing a lot, and it needs to be very readable.
Report comment
Reply
People don’t want multiple screens, they want sufficient work-space. That’s achievable in several ways, one could use one large high resolution screen or multiple smaller, lower resolution screens in various arrangements. I don’t think I’d even be able to use an e-ink display for the documentation I use, as I need to be able to search it.
E-ink certainly wouldn’t suit my need for multiple monitors where I’m running several instances of the software I’m developing as well as the development environment.
I would use an e-ink display for a smart watch, or a ‘distraction free’ writing environment, as well as e-books obviously.
Report comment
Reply
My preference for multi monitor is that all monitors can be treated as physical “instances”
Emulating that on a big display gets funky and involves emulated borders, and the best implementation I’ve seen were some X11 hackery.
Report comment
Reply
That’s how I use my multi monitor systems as well, for now it’s easier. If I were to get a single large screen for desktop use I’d invest some time in finding or making a window manager with areas for sub-screens.
Report comment
Reply
Acer Gridvista was pretty awesome for that, divvy up your monitor into virtual screens, but only works with XP… today on windows 10 you can’t even arrange your windows as easily as in windows 3.xx program manager.
Report comment
Reply
I’m a developer myself. I very much prefer multiple monitors over one big one when I am working. It’s easy to maximize my development environment in one screen, a web browser or the application I am developing in another. If I feel like being accessible then my inbox is a good use for a third.
A single big screen is just a single big pain in the ass.
I can drag and size windows until they are perfectly arranged but time and time again in the heat of the moment chasing down some bug, magnifying some feature, etc… I will end up moving things.
Then after it’s over it’s back to arranging windows again. What a waste of perfectly good time, energy and patience!
At home, on Linux I solved this problem by switching to StumpWM, a tiling window manager. That works although it brings it’s own problems with it. At work I am forced to use Windows so no Stump for me there.
For a while I did have a program that divided a single monitor into virtual screens. That was cool but buggy and occasionaly caused crashes.
Were I to have unlimited time on my hands I would love to develop some sort of tiled/windows hybrid window manager to solve this problem once and for all. It’s never going to happen. Stringing 2 or more monitors on every computer is going to have to suffice for now.
Back to something closer to the device in the article…. I would love a phone that has both an eInk and a regular display. Then I could use my phone for reading and flashcards in bright sunlight but still have the main display for it’s better resolution, color and framerate when I am inside.
Yes, I know something like that was available for a while. I’m not made of money, I don’t buy one of every phone generation (what is that, 6 months?). A new phone just wasn’t an option at the time those were available.
Report comment
Reply
Actually if you were made of money, spending it would involve losing parts of your body. You’d be even less able to buy expensive phones.
Report comment
Reply
Arm and a leg?
Report comment
That’s why I’m interested in a e-ink display.
Granted I’d prefer it to be a portable A4 sized ordeal so it can be put away when not needed, but that’s my preference for one.
Report comment
Reply
The “you need more than one screen” fad is still going because you DO need more than one screen for many types of work. If you don’t for yours, congratulations.
Report comment
Reply
“fad”? LOL
Report comment
Reply
It would be nice to be able to use such a display as the console terminal.
Report comment
Reply
Given that he’s doing bilevel rendering, and freetype lost its bilevel truetype hinter close to a decade ago … should really consider using bitmap fonts instead/in addition.
Report comment
Reply
That’s a very good point, I just happened to use TrueType first. I tried it out and bitmap (.pcf) fonts are easy to do, I just need to modify cursor rendering a bit first. I’ll add bitmap font support tonight *if* I have time :)
Report comment
Reply
Bitmap font support is now added, experimental as usual…
Report comment
Reply
Epaper displays is still WAY overpriced.
We aren’t going to see any sanely priced epaper displays until the patents from EInk finally expire.
Until that happens, don’t even bother with it.
Report comment
Reply
Yeah, where the hell am I going to get my hands on $15?!
Report comment
Reply
$15 for a one-off is fine.
But if you want to produce any quantity (without going BIG quantity and custom made), that price is way too high. I can get an equivilant size full colour OLED for maybe $5, and I would expect that a monochrome display should be in the region of $3 to $4, not the triple or quadruple as it is.
Report comment
Reply
OLED is rather energy hungry. So if you want something to be powered on a small battery, OLED is a no-go.
LCD with reflective background is the only alternative. And still then, the readability of e-ink in full sunlight is unbeatable.
You see them more often in stores as price tags, like in the Media Markt stores, so I guess they get a better price for them in large quantities, or there is some other saving to make them less expensive than the alternative (flexible pricing of the products advertised throughout the day for example)
Report comment
Reply
Does anyone know suppliers other than waveshare for DIY friendly e-ink displays?
Report comment
Reply
PaPiRus, Inky. Both can be bought from RPi resellers.
Report comment
Reply
The thing that really appeals to me about this pairing is the persistence of the
e-Ink display without power. For low power scenarios, it might be feasible to have the SOC (raspberry pi) turn on for just a few minutes, perform some monitoring measurement or operation, update the display, then power off. If the e-Ink stays in place with the raspberry pi powered down, it can be glanced at with the values noted while the real computer isn’t drawing any power.
Report comment
Reply
more useful than mine:
https://www.youtube.com/watch?v=rjoKQZi-yRE
Report comment
Reply
I use the same display (red/black/white version—should also work with black/white) to display cryptocurrency charts.
https://github.com/DurandA/inky-cryptochart
Report comment
Reply
Just a heads up – added driver support for up to 17 display models. Doesn’t mean they all work right away – needs people with the hardware to test and report any bugs so we can iron them out.
Report comment
Reply
Thank you so much for working on these waveshare drivers. Would you have any ideas on how to make the drivers work for the 9.7inch? I’m trying to fiddle around with the image dimensions, but there seems to be other things I need to fix to make it run..Any pointers would be helpful.
Report comment
Reply
Check out the issue here, a person named ‘phaer’ got partial refresh working with the 9.7″ and was going to use some other terminal code as a base instead: https://github.com/joukos/PaperTTY/issues/25. Maybe they can help.
Sadly I don’t have the hardware myself.
Report comment
Reply
Leave a ReplyCancel reply
Please be kind and respectful to help make the comments section excellent. (Comment Policy)This site uses Akismet to reduce spam. Learn how your comment data is processed.
Search
Search for:
Never miss a hack
Follow on facebook
Follow on twitter
Follow on youtube
Follow on rss
Contact us
Subscribe
If you missed it
In Praise Of Plasma TVs
20 Comments
Tech In Plain Sight: Pneumatic Tubes
29 Comments
If IRobot Falls, Hackers Are Ready To Wrangle Roombas
44 Comments
Moving From Windows To FreeBSD As The Linux Chaos Alternative
105 Comments
“AI, Make Me A Degree Certificate”
139 Comments
More from this category
Our Columns
Congratulations To The 2025 Component Abuse Challenge Winners
3 Comments
Keebin’ With Kristina: The One With The Cipher-Capable Typewriter
18 Comments
Hackaday Links: November 16, 2025
12 Comments
The Value Of A Worked Example
11 Comments
Hackaday Podcast Episode 345: A Stunning Lightsaber, Two Extreme Cameras, And Wrangling Roombas
1 Comment
More from this category