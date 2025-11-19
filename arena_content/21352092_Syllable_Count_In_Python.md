Syllable Count In Python
Ask Question
Asked
8 years, 1 month ago
Modified
3 years, 3 months ago
Viewed
41k times
6
I need to write a function that will read syllables in a word (for example, HAIRY is 2 syllables).
I have my code shown on the bottom and I'm confident it works in most cases, because it works with every other test I've done, but not with "HAIRY" where it only reads as 1 syllable.
def syllable_count(word):
count = 0
vowels = "aeiouy"
if word[0] in vowels:
count += 1
for index in range(1, len(word)):
if word[index] in vowels and word[index - 1] not in vowels:
count += 1
if word.endswith("e"):
count -= 1
if count == 0:
count += 1
return count
TEST
print(syllable_count("HAIRY"))
Expected: 2
Received: 1
pythonfunction
Share
Improve this question
Follow
edited Oct 16, 2017 at 2:19
Jeremy McGibbon
3,8151717 silver badges2222 bronze badges
asked Oct 15, 2017 at 20:09
Ryan
19922 gold badges44 silver badges1010 bronze badges
Add a comment
|
5 Answers
5
Sorted by:
Reset to default
Highest score (default)
Trending (recent votes count more)
Date modified (newest first)
Date created (oldest first)
7
The problem is that you're giving it an uppercase string, but you only compare to lowercase values. This can be fixed by adding word = word.lower() to the start of your function.
def syllable_count(word):
word = word.lower()
count = 0
vowels = "aeiouy"
if word[0] in vowels:
count += 1
for index in range(1, len(word)):
if word[index] in vowels and word[index - 1] not in vowels:
count += 1
if word.endswith("e"):
count -= 1
if count == 0:
count += 1
return count
print(syllable_count('HAIRY'))
# prints "2"
Share
Improve this answer
Follow
edited Nov 2, 2018 at 18:30
answered Oct 15, 2017 at 20:14
Jeremy McGibbon
3,8151717 silver badges2222 bronze badges
Sign up to request clarification or add additional context in comments.
1 Comment
Add a comment
Kavyajeet Bora Kavyajeet Bora Over a year ago
for "tickle" the function returns 1 but it should be 2 instead. I think adding this should help -
word.endswith("e") and not word.endswith("le") 2020-02-20T08:46:17.97Z+00:00
0
Reply
Copy link
5
There are certain rules for syllable detection, you can view the rules from the website: Counting Syllables in the English Language Using Python
Here's the python code:
import re
def sylco(word) :
word = word.lower()
# exception_add are words that need extra syllables
# exception_del are words that need less syllables
exception_add = ['serious','crucial']
exception_del = ['fortunately','unfortunately']
co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
co_two = ['coapt','coed','coinci']
pre_one = ['preach']
syls = 0 #added syllable number
disc = 0 #discarded syllable number
#1) if letters < 3 : return 1
if len(word) <= 3 :
syls = 1
return syls
#2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
# if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)
if word[-2:] == "es" or word[-2:] == "ed" :
doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]',word))
if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]',word)) > 1 :
if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies" :
pass
else :
disc+=1
#3) discard trailing "e", except where ending is "le"
le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']
if word[-1:] == "e" :
if word[-2:] == "le" and word not in le_except :
pass
else :
disc+=1
#4) check if consecutive vowels exists, triplets or pairs, count them as one.
doubleAndtripple = len(re.findall(r'[eaoui][eaoui]',word))
tripple = len(re.findall(r'[eaoui][eaoui][eaoui]',word))
disc+=doubleAndtripple + tripple
#5) count remaining vowels in word.
numVowels = len(re.findall(r'[eaoui]',word))
#6) add one if starts with "mc"
if word[:2] == "mc" :
syls+=1
#7) add one if ends with "y" but is not surrouned by vowel
if word[-1:] == "y" and word[-2] not in "aeoui" :
syls +=1
#8) add one if "y" is surrounded by non-vowels and is not in the last word.
for i,j in enumerate(word) :
if j == "y" :
if (i != 0) and (i != len(word)-1) :
if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
syls+=1
#9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.
if word[:3] == "tri" and word[3] in "aeoui" :
syls+=1
if word[:2] == "bi" and word[2] in "aeoui" :
syls+=1
#10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"
if word[-3:] == "ian" :
#and (word[-4:] != "cian" or word[-4:] != "tian") :
if word[-4:] == "cian" or word[-4:] == "tian" :
pass
else :
syls+=1
#11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
if word[:2] == "co" and word[2] in 'eaoui' :
if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two :
syls+=1
elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one :
pass
else :
syls+=1
#12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
if word[:3] == "pre" and word[3] in 'eaoui' :
if word[:6] in pre_one :
pass
else :
syls+=1
#13) check for "-n't" and cross match with dictionary to add syllable.
negative = ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]
if word[-3:] == "n't" :
if word in negative :
syls+=1
else :
pass
#14) Handling the exceptional words.
if word in exception_del :
disc+=1
if word in exception_add :
syls+=1
# calculate the output
return numVowels - disc + syls
Share
Improve this answer
Follow
edited Jun 14, 2018 at 7:09
wscourge
11.4k1717 gold badges6565 silver badges8787 bronze badges
answered Jun 14, 2018 at 6:46
Tarun 007
7411 silver badge55 bronze badges
2 Comments
Add a comment
safex safex Over a year ago
multiple examples fail, "announcement" returns 4 (should be 3), "columbia" returns 3 (should be 4),... 2018-11-08T15:51:00.21Z+00:00
0
Reply
Copy link
Pig Pig Over a year ago
More examples that fail: "tried", "course", 2021-04-03T15:53:06.283Z+00:00
0
Reply
Copy link
1
Your code seems to be working fine when given anything in lower case. However if you pass it a word in all upper case it will always return 1. This is because you are testing against "aeiou" and not "aeiouAEIOU".
You can fix this in a few ways.
Example 1:
vowels = "aeiouyAEIOUY"
Example 2:
print(syllable_count("HAIRY".lower()))
Example 3: add this line of code at the start of the 'syllable_count' function
word = word.lower()
Share
Improve this answer
Follow
edited Jan 27, 2019 at 0:16
ABM
1,62822 gold badges2626 silver badges4343 bronze badges
answered Oct 15, 2017 at 20:27
Dominic Egginton
37533 silver badges1313 bronze badges
Comments
Add a comment
0
you could use this as well using lambda map
fun_check = lambda x: 1 if x in ["a","i","e","o","u","y","A","E","I","O","U","y"] else 0
sum(list(map(fun_check,"your_string")))
in single line
sum(list(map(lambda x: 1 if x in ["a","i","e","o","u","y","A","E","I","O","U","y"] else 0,"your string")))
Share
Improve this answer
Follow
answered Jun 14, 2018 at 7:22
Pawanvir singh
37366 silver badges1717 bronze badges
Comments
Add a comment
0
For the best results, you might want to use a dictionary-based implementation. Packages like PyHyphen provide such functionality.
Hyphenator('en_US').syllables('beautiful') # = ['beau', 'ti', 'ful']
(Though, when I test this library using "hairy" it outputs only one syllable because this word is currently not in the default dictionary)
Share
Improve this answer
Follow
answered Aug 17, 2022 at 13:21
Corylus
93788 silver badges1717 bronze badges
Comments
Add a comment
Your Answer
Draft saved
Draft discarded
Sign up or log in
Sign up using Google
Sign up using Email and Password
Submit
Post as a guest
Name
Email
Required, but never shown
Post as a guest
Name
Email
Required, but never shown
Post Your Answer
Discard
By clicking “Post Your Answer”, you agree to our terms of service and acknowledge you have read our privacy policy.
Start asking to get answers
Find the answer to your question by asking.
Ask question
Explore related questions
pythonfunction
See similar questions with these tags.
The Overflow Blog
How to create agents that people actually want to use
Introducing Stack Internal: Powering the human intelligence layer of...
Featured on Meta
We’re releasing our proactive anti-spam measure network-wide
Chat room owners can now establish room guidelines
Policy: Generative AI (e.g., ChatGPT) is banned
Opinion-based questions alpha experiment on Stack Overflow
Linked
0
Syllable Counter in Python fails with silent e in word
0
How to count consecutive vowels in a text file in Python
1
How to get complex words from a text file in python?
1
Counting syllables in a list of strings Python without using RE
Related
9
Count the Number of Syllables in a Word
1
Function that takes a string as input and counts the number of times the vowel occurs in the string
3
Counting vowels in python
3
Python def vowelCount() creating a dictionary
1
Python Counting Vowels
0
Python string vowel counter
2
Counting Syllables In String
1
How to create vowel counter in python
1
function vowel_count that take a string as inputs count the number of occurrence and prints the occurrence
1
How to count vowels and consonants in Python
Hot Network Questions
Where is the island in Dept. Q?
Why am I experiencing a strange ethernet cable termination result? I have not seen this before
CR2032 Lithium Battery Shorted
Meaning of the question "В памяти?"
On hypersurface singularity.
Industrial applications for a space station in close solar orbit
Please evaluate this translation of John 1:1-2
Why does a voltage divider work even with extreme resistor values?
Does Democratic Socialism conflict with the US Democratic Party's core values, or has any Democrat leader spelled out why they oppose it?
Two semicircles in a parallelogram
Should I leave the neutral disconnected when replacing a smart switch with a conventional switch?
Are Quantum Espresso total energies for different charge states of the same system comparable?
How to definitely understand the word "Axiom"
What's the earliest attested reference to lighting a fart on fire?
Coloring a graph with K-colors
Generation ship overtaken by newer technology ship which reaches target planet first
How easy is it to chip a glass jar without breaking it, with various material spoons?
prisoners riddle - a button, a light and a timer
Can myths convey truths even if they are not literally true?
Do European funding agencies consider socioeconomic background in their diversity initiatives?
How can I buy a Nintendo eShop game as a gift without it downloading before a specific date?
Why are Africans compared to Cain?
Does op amp input impedance (significantly) vary with supply voltage?
Why do tuners use dynos instead of accelerometers?
more hot questions
Question feed
lang-py