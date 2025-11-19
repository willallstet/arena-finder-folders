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
Things are moving at lightning speed in AI Land. On Friday, a software developer named Georgi Gerganov created a tool called “llama.cpp” that can run Meta’s new GPT-3-class AI large language model, LLaMA, locally on a Mac laptop. Soon thereafter, people worked out how to run LLaMA on Windows as well. Then someone showed it running on a Pixel 6 phone, and next came a Raspberry Pi (albeit running very slowly).
If this keeps up, we may be looking at a pocket-sized ChatGPT competitor before we know it.
But let’s back up a minute, because we’re not quite there yet. (At least not today—as in literally today, March 13, 2023.) But what will arrive next week, no one knows.
Since ChatGPT launched, some people have been frustrated by the AI model’s built-in limits that prevent it from discussing topics that OpenAI has deemed sensitive. Thus began the dream—in some quarters—of an open source large language model (LLM) that anyone could run locally without censorship and without paying API fees to OpenAI.
Open source solutions do exist (such as GPT-J), but they require a lot of GPU RAM and storage space. Other open source alternatives could not boast GPT-3-level performance on readily available consumer-level hardware.
Enter LLaMA, an LLM available in parameter sizes ranging from 7B to 65B (that’s “B” as in “billion parameters,” which are floating point numbers stored in matrices that represent what the model “knows”). LLaMA made a heady claim: that its smaller-sized models could match OpenAI’s GPT-3, the foundational model that powers ChatGPT, in the quality and speed of its output. There was just one problem—Meta released the LLaMA code open source, but it held back the “weights” (the trained “knowledge” stored in a neural network) for qualified researchers only.
Flying at the speed of LLaMA
Meta’s restrictions on LLaMA didn’t last long, because on March 2, someone leaked the LLaMA weights on BitTorrent. Since then, there has been an explosion of development surrounding LLaMA. Independent AI researcher Simon Willison has compared this situation to the release of Stable Diffusion, an open source image synthesis model that launched last August. Here’s what he wrote in a post on his blog:
It feels to me like that Stable Diffusion moment back in August kick-started the entire new wave of interest in generative AI—which was then pushed into over-drive by the release of ChatGPT at the end of November.
That Stable Diffusion moment is happening again right now, for large language models—the technology behind ChatGPT itself. This morning I ran a GPT-3 class language model on my own personal laptop for the first time!
AI stuff was weird already. It’s about to get a whole lot weirder.
Typically, running GPT-3 requires several datacenter-class A100 GPUs (also, the weights for GPT-3 are not public), but LLaMA made waves because it could run on a single beefy consumer GPU. And now, with optimizations that reduce the model size using a technique called quantization, LLaMA can run on an M1 Mac or a lesser Nvidia consumer GPU (although “llama.cpp” only runs on CPU at the moment—which is impressive and surprising in its own way).
Things are moving so quickly that it’s sometimes difficult to keep up with the latest developments. (Regarding AI’s rate of progress, a fellow AI reporter told Ars, “It’s like those videos of dogs where you upend a crate of tennis balls on them. [They] don’t know where to chase first and get lost in the confusion.”)
For example, here’s a list of notable LLaMA-related events based on a timeline Willison laid out in a Hacker News comment:
February 24, 2023: Meta AI announces LLaMA.
March 2, 2023: Someone leaks the LLaMA models via BitTorrent.
March 10, 2023: Georgi Gerganov creates llama.cpp, which can run on an M1 Mac.
March 11, 2023: Artem Andreenko runs LLaMA 7B (slowly) on a Raspberry Pi 4, 4GB RAM, 10 sec/token.
March 12, 2023: LLaMA 7B running on NPX, a node.js execution tool.
March 13, 2023: Someone gets llama.cpp running on a Pixel 6 phone, also very slowly.
March 13, 2023, 2023: Stanford releases Alpaca 7B, an instruction-tuned version of LLaMA 7B that “behaves similarly to OpenAI’s “text-davinci-003” but runs on much less powerful hardware.
After obtaining the LLaMA weights ourselves, we followed Willison’s instructions and got the 7B parameter version running on an M1 Macbook Air, and it runs at a reasonable rate of speed. You call it as a script on the command line with a prompt, and LLaMA does its best to complete it in a reasonable way.
A screenshot of LLaMA 7B in action on a MacBook Air running llama.cpp.
Credit:
Benj Edwards / Ars Technica
A screenshot of LLaMA 7B in action on a MacBook Air running llama.cpp.
Credit:
Benj Edwards / Ars Technica
There’s still the question of how much the quantization affects the quality of the output. In our tests, LLaMA 7B trimmed down to 4-bit quantization was very impressive for running on a MacBook Air—but still not on par with what you might expect from ChatGPT. It’s entirely possible that better prompting techniques might generate better results.
Also, optimizations and fine-tunings come quickly when everyone has their hands on the code and the weights—even though LLaMA is still saddled with some fairly restrictive terms of use. The release of Alpaca today by Stanford proves that fine tuning (additional training with a specific goal in mind) can improve performance, and it’s still early days after LLaMA’s release.
As of this writing, running LLaMA on a Mac remains a fairly technical exercise. You have to install Python and Xcode and be familiar with working on the command line. Willison has good step-by-step instructions for anyone who would like to attempt it. But that may soon change as developers continue to code away.
As for the implications of having this tech out in the wild—no one knows yet. While some worry about AI’s impact as a tool for spam and misinformation, Willison says, “It’s not going to be un-invented, so I think our priority should be figuring out the most constructive possible ways to use it.”
Right now, our only guarantee is that things will change rapidly.
Related Stories
Meta unveils a new large language model that can run on a single GPU [Updated]
LLaMA-13B reportedly outperforms ChatGPT-like tech despite being 10x smaller.
Get ready to meet the Chat GPT clones
A tidal wave of bots is on its way.
Listing image:
Ars Technica
Benj Edwards
Senior AI Reporter
Benj Edwards
Senior AI Reporter
Benj Edwards is Ars Technica's Senior AI Reporter and founder of the site's dedicated AI beat in 2022. He's also a tech historian with almost two decades of experience. In his free time, he writes and records music, collects vintage computers, and enjoys nature. He lives in Raleigh, NC.
150 Comments
Staff Picks
They claimed similar performance to GPT-3 on a bunch of tasks in their paper, are you saying that's not reproducible?
Most tasks work great with a context size of 256 tokens.
Simple Q&A type questions.
Or is it just that it's not as good in terms of context size?
Very simple problems like 'what is the capital of X', or 'what is the difference between an X and Y' can usually be answered in short contexts.
Any sort of useful programming problem or multiple interactions requires much longer contexts - frequently 4k-8k.
Also what does complexity mean in this context?
Number of interacting 'things' and their interactions.
Roughly number of nouns/objects and verbs/actions and how complexly they are interacting.
If I ask LLaMa to do a simple function of two variables, it has no problem.
More complex ideas it quickly fails.
And what relation is there between context size and model total parameters, could you explain that further?
The smaller the model the higher the loss per token, and the sooner it 'caps out' (no further reduction in token loss for a longer context.
For bigger models the more context the better they can accurately predict future tokens
https://github.com/BlinkDL/RWKV-LM/raw/main/RWKV-ctxlen.png
See the cap for RWKV of around 1.93 at 1.1K tokens for 1 Billion parameter model vs 1.64 for the 16 Billion parameter model,
Sorry for the twenty questions, I'm just intensely curious about the subject and I've read a lot of your other comments about AI
Happy to answer questions on this.
March 14, 2023 at 12:53 am
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