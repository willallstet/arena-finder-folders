Text
settings
Story text
Size
Small
Standard
Large
Width
*
Standard
Wide
Links
Standard
Orange
* Subscribers only
Learn more
Minimize to nav
Hackers of a certain age are intimately familiar with the “Will it run Doom” meme and the wide array of ports it has engendered (including a game of Doom that runs inside an instance of Doom itself). Still, this week’s viral video and eventual itch.io release of a Doom port running in Windows’ standard notepad.exe text editor left us with a number of questions.
Chief among them: “How?” and “Why?”
“My favorite kind of magic trick”
When it comes to the “How?” DoomPad coder Sam Chiet told Ars that the hack is “my favorite kind of magic trick,” the kind that “seems wild, but it’s super simple.”
Building off a C# port of the open-sourced Doom source code (and later shifted to Chocolate Doom for public release), Chiet’s program first converts every successive frame from the game into ASCII text. That’s done using a simple algorithm that figures out the “brightness” of each pixel (by averaging out the RGB color channel data), then converting that to a similarly dark ASCII character using a pre-set lookup table (ranging from “$” and “@” for the darkest pixels to “\” and “.” for the lightest).
i got DOOM running inside Notepad at 60fps pic.twitter.com/EQFuRu4N0r
— Samperson (Crime Arc) (@SamNChiet) October 9, 2022
“[The] conversion is super simple and probably ‘incorrect,’ but it works, and that’s what matters,” Chiet said. “Magic tricks [like this] are always equal parts disappointing and cool!”
Because “the Notepad font is twice as tall as it is wide,” DoomPad initially throws out every other row of generated text to keep the resulting ASCII in the correct proportions. From there, Windows makes it relatively easy to insert that 360×240 array of text into Notepad at whatever font size your window and monitor can handle, Chiet said.
“I’m stealing a reference to the internal textbox and just sticking my memory into it via an operating system ‘message’ and forcing it to re-draw,” he said. As for reading player input, that’s “just something you can steal from anywhere in Windows; you don’t need your specific program ‘open.'”
Chiet said he was somewhat inspired by previous projects like the ASCII-based 1337d00m, which has a key advantage of using color characters.
Chiet said he was somewhat inspired by previous projects like the ASCII-based 1337d00m, which has a key advantage of using color characters.
As it turns out, the Windows Notepad isn’t really well-suited to act as a stable, consistent view window for a fast-paced game like Doom. Chiet’s 60 fps demo has a lot of noticeable flickering, especially near the bottom of the text box.
“Notepad does not have an offscreen ‘buffer’ to render on, so everything it draws, you’re seeing it draw in real time,” Chiet explained. “So it’s stuck rendering [about] 86,000 characters per update, and I’m also not timing it to the screen’s vsync.” Chiet said someone suggested alternating between two Notepad windows every frame as a form of ersatz double buffering, and he thinks that should work.
If that limitation is solved, though, Chiet said that “the sky is the limit for realtime Notepad gameplay.” Since “anything else you want to do in a game engine is already possible” with the same basic method, Chiet said he’s working on releasing a generic framework for Notepad games in the near future.
Beyond that, Chiet said he’s “more excited [about] the things I’m doing to MS Paint,” which he’s not ready to share with the world just yet. But “if DoomPad was a simple magic trick, what I’m doing to MS Paint is a whole David Blaine episode,” he teased.
The DoomPad philosophy
On the one hand, Chiet seemed pretty blasé when asked about why he undertook such a strange coding project, calling it a “total whim.” At a base level, the project was just an extension of an ongoing interest “in the realm of hijacking software. But not in a malware way, in a… funny way,” Chiet said. DoomPad was just a “two-hour ‘wouldn’t this be funny’ [thing] I kludged together” using underlying code he “stole from some of my other (not yet publicly shown) projects,” he said.
On the other hand, Chiet also got a bit philosophical when discussing the wider meaning of his project.
For the 21-year-old hacker, the widespread “Will it run Doom?” question hits differently than it does for those of older generations. “I think there’s two parts to the Doom meme,” Chiet said. “One is nostalgia. The other is the satisfaction in seeing walls you took for granted be taken down. To me, I didn’t grow up with Doom. But the generation I’m a part of has such a giant well of creative rage that memes like this have endured…”
DoomPad isn’t the first GUI hack for notepad.exe. Kyle Halladay’s ray tracing sample from 2020 pulls off some very similar tricks (click “Expand” to see it in motion).
DoomPad isn’t the first GUI hack for notepad.exe. Kyle Halladay’s ray tracing sample from 2020 pulls off some very similar tricks (click “Expand” to see it in motion).
Growing up with “hand-me-downs of hand-me-down computers,” Chiet said he got a crash course in the transition from late ’90s monolith workstations to present-day magic-black-slate smartphones. That transition has meant that many in his generation view technology not just as a tool but more as “a space you work, a space you socialize, etc.” he said.
Chiet comes off as more than a little jaded about that change. “We’re not growing up with a space we fully control,” he said. “We’re growing up with software subscriptions and licensed services. Everything is up for rent, including our attention. The home button on our first ‘Windows’ experience is showing us ads.”
For tech users in his age group, “their creative tools aren’t Kid Pix; they’re TikTok,” Chiet said. “And trying to point this out is like explaining to a fish what water is.”
Running Doom in a Notepad window provides a bit of philosophical pushback against that tendency, Chiet said. “It’s stupid, and it’s shitposty, and I totally own that I probably sound pretentious here, but it fires those neurons that are like, ‘Oh, we can do that.’ It’s a reminder that these spaces are malleable, and that’s a really powerful idea to people whose first computer was an iPhone.”
“It’s also extremely funny,” he added. “That’s a big part of it, too.”
Related Stories
Doomception: How modders got Doom to run inside of Doom
The zenith of over a decade of Action Code Script modding within id's classic.
Hacker exploits printer Web interface to install, run Doom
Firmware update flaw makes it easy to spy on printed docs, break in to networks.
Listing image:
Sam Chiet
Kyle Orland
Senior Gaming Editor
Kyle Orland
Senior Gaming Editor
Kyle Orland has been the Senior Gaming Editor at Ars Technica since 2012, writing primarily about the business, tech, and culture behind video games. He has journalism and computer science degrees from University of Maryland. He once wrote a whole book about Minesweeper.
89 Comments
Comments
Forum view
Loading comments...
Prev story
Next story
1.
With a new company, Jeff Bezos will become a CEO again
2.
Trump admin axed 383 active clinical trials, dumping over 74K participants
3.
I’ve already been using a “Steam Machine” for months, and I think it’s great
4.
Google’s Sundar Pichai warns of “irrationality” in trillion-dollar AI investment boom
5.
After last week’s stunning landing, here’s what comes next for Blue Origin
Customize