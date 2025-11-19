×Embed the widget on your own siteAdd the following snippet to your HTML:<iframe frameborder='0' height='385' scrolling='no' src='https://www.hackster.io/david-packman/clippygpt-6a683a/embed' width='350'></iframe>Everyone is asking if ChatGPT is actually Clippy in disguise. Well, what better way to find out than building a ChatGPT-powered Clippy?Read up about this project on ClippyGPTDavid Packman39 14,436 OverviewThingsStoryIntroductionThe BOMBasic BOMFull BOMPrinting the partsAssemblyClippyBottom BaseTop BasePreparing your SBC for the codeSchematicsCodeCreditsComments(11)David PackmanPublished March
3, 2023 © CC BYClippyGPTEveryone is asking if ChatGPT is actually Clippy in disguise. Well, what better way to find out than building a ChatGPT-powered Clippy?IntermediateFull instructions provided24 hours14,437Things used in this project Hardware componentssmall through-hole protoboard or small breadboardYou can always cut down a protoboard to suit the needs. Basically you'll use this to create a power splitter to provide 5v power to all the parts via a 1 to 3 split.×1USB Adapter, Right-AngleYou may want to get a 4-pack from Amazon so you have left and right angle to ensure you have the right part.×15v 4a power adapterIf you use a higher voltage adapter you'll need to add a 5v step-down regulator. There are mounting holes for a https://www.pololu.com/product/4091 regulator.×1Adafruit Adafuit CRICKIT for Raspberry PIThe CRICKIT should work on any SBC with a Pi-compatible GPIO. As an alternative, you can use a serial or I2C PWM/Servo controller instead. There are mounting holes for an Adafruit 16 channel PWM Servo controller.×1Adafruit Mono 2.5a audio ampWhile the Crickit has a built in 3a amp that you can leverage instead, it can be difficult to make it work. So this is an alternative that you can use, mounting points are in the build.×1SG90 Micro-servo motorNote, you can also use the Feetech FS90 if there are none at Adafruit, there are a lot of TowerPro SG90 knock offs of variable quality. You can find the FS90 at https://www.pololu.com/product/2818.×2Flat ribbon HDMI cable with HDMI or Micro HDMI headersThese are basically HDMI ribbon cables made for drone cameras. If you're using an SBC with microHDMI output you'll want to look for HDMI ribbon cable sets that include those and regular HDMI terminals instead.×1Raspberry Pi 3 Model BHey, these are impossible to come by, so you should also be able to get another brand SBC with a RasPi pinout/mounting pattern like the Libre LePotato, Libre Renegade, or RockPi. Just make sure the USB ports are positioned like the RasPi 3B or the right angle USB adapter won't work and you'll need to figure out how to make a USB extension cable work instead. :(×1Buy from NewarkBuy from AdafruitBuy from CPCBuy from ModMyPiBuy from SparkFunSpeaker with a 1.75 inch mounting hole patternThis build used a salvaged speaker from an Alexa Echo Dot. So you'll want to find something with a similar hole pattern.×1Elecrow 5 inch HDMI displayBasically any 5 inch HDMI display with the HDMI and Power at the top of the display.×1Fishing lineAny strong thread with minimal stretch. I use 100 test pound braided line.×1female barrel jack×1M2, M2.5 and M3 Screws, nuts, and heatset nutsI used a variety of M2, M2.5, and M3 screws, nuts, heatset nuts, square nuts, and standoffs in this build.×1Software apps and online servicesRaspberry Pi RaspbianYou can use Debian or a Debian distro like Raspbian, whatever your SBC of choice uses.
However, speech services on Ubuntu requires OpenSSLv1, which isn't supported on Ubuntu anymore.OpenAI api python libraryMicrosoft Azure Speech ServicesHand tools and fabrication machinesSoldering iron (generic)Story IntroductionDid you ever want to make your robot friend more conversational? I sure have, so I built ClippyGPT as a proof of concept for integrating OpenAI and Azure Speech Services into robotics using Python to give my companion bots more personality and make them more engaging. Now you can build your own ClippyGPT or use the sample code to integrate ChatGPT into your next robot project!*NOTE: See the 3D Printing Parts section for a link to the STL files!*NOTE: Updated on May 1, 2023 to clean up code and add new ChatGPT 3.5 multi-turn "chat mode".The BOMSo, this section is split up a bit, and there is a lot of room here for you to choose different devices based on your needs. First I’ll talk about a basic build which doesn’t include any moving parts to make a basic echo dot smartspeaker experience. Then I’ll go over what else is needed to build the full ClippyGPT experience.Basic BOMThe bare minimum needed to build the basic non-moving talking chatgpt experience, You’ll need:·A Single Board Computer, (eg. Raspberry Pi), running a Debian distro, which includes Raspbian (ideally full desktop Bullseye). NOTE: It’s important that the board have the USB ports positioned similarly to a Raspberry Pi 3B or else you’ll need to use a USB extension cable instead of a Right-Angle USB adapter to get the microphone into the right position.· A Power Supply, ideally a 5v 5a switching power supply with a 5.5mm barrel jack. You can use a higher voltage PS if you also add a step-down regulator like this one https://www.pololu.com/product/4091which has mounting holes for it in the model.· A 5.5mm female barrel jack connector, like these https://www.amazon.com/gp/product/B01GPQZ4EE· A through-hole protoboard or a small breadboard to split the power out to the components.· A small speaker with a mounting hole pattern of 1.25 inches (31.75mm). I used a speaker recycled from an old echo dot.· A 2.5w mono amp like this one https://www.adafruit.com/product/2130· A right-angle USB adapter like this one https://www.amazon.com/gp/product/B073GTBQ8V· A USB microphone, like this one https://www.amazon.com/gp/product/B07SVYVZ1H.Full BOMIf you want the full build, in addition to the above, also get:·Two Tower Pro SG90 or Feetech FS90 servo motors.· A servomotor controller, I used an Adafruit Crickit Hat for Raspberry Pi but have mounting holes for the Adafruit 16 channel PWM controller too.· Fishing line – This is what moves the eyebrows. I use 100 test lbs braided, but whatever you have should work as long as there’s no stretch.· An HDMI flat ribbon cable kit like this one https://www.amazon.com/dp/B07R9RXWM5· A compact HDMI 5 inch display with power and HDMI cable connections at the top of the screen, like this one https://www.amazon.com/dp/B013JECYF2.· Some micro USB pigtail cables like these https://www.amazon.com/dp/B09DKYPCXKfor powering the SBC, display, and whatnot. (you may need barrel jack and/or USB C ones depending on which SBC and servo driver you choose).· Audio jack screw down adapter, like these https://www.amazon.com/dp/B06Y5YJRPD· A spring-loaded retractable ink pen. (You’ll use the compression spring in it for the eyebrow movement.)Printing the partsThe STL files are available at https://www.printables.com/model/413897-clippygpt.These parts were printed on various printers at.02 layer height using both PLA and PETG, so either or should work fine. The top and bottom shells should be the only parts that really need supports and brims may be useful if you have problems with large prints curling up.The only parts you may want to use a finer resolution on are the bits for the eyebrow movement, where.01 may give them some more strength.The eyes were made with white filament and a manual filament change to black where the pupils start.AssemblyClippy:1. First, if you’re trying for movement, thread one length of line for each side, one from the left slot in the back and the other through the right slot, until they come out the bottom with a good bit extra on each end, you can cut them to size after tying them down to the moving parts.2. Glue the eyes so they align with the horizontal slots. If you find that gluing isn’t working for you, use some spare filament across those aligned gaps to reinforce it with either glue or by plastic welding them in place.3. Tie the lines to the small holes in the brow clip pieces, (applying superglue to the knots can prevent slipping, just make sure it’s dry before handling), then insert those into the slots in the back above the respective eyes.4. Get some short M2 heatset inserts and install one in the back of each eyebrow, then you can use 8mm M2 screws to attach the eyebrows to the clips.5. Get that spring you liberated from the retractable pen and cut it in half. Then place each half on each of the long posts on the eyebrow clips. Using that post as a guide, place the small U-shaped Brow Hoops at the very end of those posts and hold it in place while you use a soldering iron tip to weld it to Clipply, while avoiding melting it so much that it sticks to the posts. You want this part to hold the spring and post in place while allowing the clip to move up and down.
Bottom Base1. Prep the bottom part of the case by installing the M2 and M2.5 hex nuts in the underside of the bottom part of the base as shown here:
2. Now you should be able to install the bottom base electronics as shown below:
3. I find that using 5 or 6mm M2 screws work fine for the parts using M2 fasteners.Note: For the SBC mount, you’ll want to put 1.8mm M2.5 standoffs in place first, then bolt the SBC onto those in order to provide the right height for the right-angle USB adapter to align with the slot for the microphone.Note: The power jack cover should fasten to the bottom to secure the jack without heatset nuts, just use a longer screw to secure it, like a 12mm M2.Top Base1. Prep the top cover of the base by embedding heatset knurled nuts as described in this image:
2. While you’re at it, might as well do the M2 heatset inserts for these parts too:
3. Now we can mount the electronics inside the top part of the base:4. The servomotor arm holes may need to be enlarged a little. I recommend using a small drill bit to enlarge the second hole from the end in order to pass the fishing line through it easily. You can mount the servo motors using a single screw (the screw that comes with the servomotor should work) on the angled mounting points behind where Clippy will be mounted. Also, you may want to align the arms so that they are in this position to start with at the appropriate end of the range for each motor so that they enough range to pull on the lines as described in the image below:
5. Now we can mount the display by placing it inside the cavity of the BubbleFront piece. It should fit snug, but if it doesn’t then feel free to use a file to make it fit better, it should be pushed all the way in.6. Now, use M2 screws to bolt the BubbleBack to the BubbleFront to secure the display between both pieces. If you’ve done it right the outer edge of both should be flush to each other.7. Insert M3 square nuts in the three slots in the lower part of the BubbleBack, then bolt the bubble assembly to the top case with M3 screws. You should be able to connect the HDMI and power cables in through the gap in the case at this point.
8. Now to mount Clippy. First, pass the fishing line in through the gap where Clippy goes, then push clippy down into that gap, then forward into the slot as shown below.
9. NOTE: If you have trouble sliding Clippy forward into that slot you may need to clean out any remaining bits of support material that might still be there until it fits in there snuggly, but without too much effort.10. If you put Clippy in the slot correctly, there should be enough room to slide the ClippyClip piece down behind Clippy to secure Clippy into place. At this point, you can bolt that ClippyClip into position using M2 screws from the underside of the top cover.
11. With the servo arms in the right position as noted above in step 4, go ahead and tie the lines to the arms so that there is as little slack as possible without moving the brows. You may want to glue the knots here to keep them from slipping.12. If you didn't use a breadboard or a regulator to distribute power to your parts, you can use a thru-hole protoboard to do so, like in this image:
13. Go ahead and wire up all the electronics before using M3 screws to fasten the bottom case to the top. NOTE: Make sure the SD card for your SBC is installed before shutting the case.
14. Once bolted together, go ahead and insert the USB microphone into the front of the case where the right-angle USB adapter should be aligned with the slot at the front of the case:
Preparing your SBC for the codeNow that everything is put together and your SBC’s operating system has been installed, let’s get the software ready. (NOTE: I recommend using the latest Debian or Raspbian Bullseye. Ubuntu won’t work because there’s a library dependency on OpenSSL1, which Ubuntu doesn’t support.)1. Using the instructions for your Single Board Computer (SBC) install the operating system and set up all the basics that you need, like SHS, VNC, screen orientation, GPIO mapping, etc…2. Optional, before you start, you can do this all in a virtual environment if you choose. So if you do, now’s the time to set that up.3. In the config, make sure to enable i2c.4. As always, run sudo apt-get update and sudo apt-get upgrade in the terminal.5. Set up the libraries and setting for the servomotor controller you’re using. If you’re using the Crickit hat, do the following in the terminal:pip3 install Adafruit-blinkai2cdetect -y 1(if you see a matrix with 49 inside of it, then you’re good so far).pip3 install Adafruit-circuitpython-crickitIf any of this gave you errors or if it doesn’t work, refer to https://learn.adafruit.com/adafruit-crickit-hat-for-raspberry-pi-linux-computers/python-installationfor help.6. Set up Azure Speech Servicesa. Sign up for a free Azure account at azure.microsoft.com (we’ll be using free tier speech services, so you shouldn’t expect any charges unless you use ClippyGPT A LOT!).b. Create a speech resource in Azure portal using the following steps: https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServicesc. Get the keys and region for your resource: https://learn.microsoft.com/azure/cognitive-services/cognitive-services-apis-create-account#get-the-keys-for-your-resource.d. In the files I share there will be a file that contains the offline keyword model table
for the “Hey Clippy” wakeword which require no extra steps or code changes to use. However, if you want a different wakeword, you’ll want to create one using the steps at https://learn.microsoft.com/azure/cognitive-services/speech-service/custom-keyword-basics?pivots=programming-language-python.e. On the terminal, type the following commands:sudo apt-get install build-essential libssl-dev libasound2 wget pip3 install azure-cognitiveservices-speech pip3 install –upgrade azure-cognitiveservices-speech7. Set up OpenAIa. Sign up for an account at https://openai.com/b. Get an API key!c. This part does cost a little bit of money, but you get an $18 grant to start with.d. On the SBC terminal, type:pip3 install openai8. Then install OpenAI's tiktokenpip3 install tiktoken9. Copy the files and update them:a. Copy the offline keyword table to your device in the same location you plan to run the python script from.b. Copy the python script to the same location.c. Type sudo nano pythonscriptname to edit the script. For example, if you use my python script you'll type:sudo nano ClippySampleCode.pyd. In the script, replace all the placeholders for the API keys and region info with the information you grabbed from Azure and OpenAI.10. Double Check your Configuration.a. On the desktop, right-click the speaker to ensure that you’re using the audio jack as your default audio output.b. Right-click the microphone to ensure your audio input is set to the USB microphone.11. Run the code:python3 ClippySampleCode.py11. To start a conversation, say "Hey Clippy". Once Clippy replies, you can either ask it a question for single-turn completion answers, or say "Let's chat" to activate multi-turn chat mode where you can ask follow-up questions while Clippy carries context over to each turn. To end chat mode, just say "I'm done".12. Have fun with it, try different things, and let me know what you do to improve it if you do!Read moreSchematics Offline Wake Word training tableThis is the wake word table for the "Hey Cippy" wake word, download this to the same location where you put the sample python code if you want to use the Hey Clippy wake word.Code Clippy sample python codeClippy sample python codePythonCopy this to your SBC then edit to:1. line 59 - replace x's with your Azure Speech Key2. line 60 - replace x's with your Azure Speech Region3. line 61 - replace x's with your OpenAI API keyNOTE: You will probably want to adjust the servomotor angles for your servos wherever you see "crickit_servo"import os
import time
import openai
import tiktoken
import azure.cognitiveservices.speech as speechsdk
from adafruit_crickit import crickit
def keyword_from_microphone():
"""runs keyword spotting locally, with direct access to the result audio"""
# Creates an instance of a keyword recognition model. Update this to
# point to the location of your keyword recognition model.
model = speechsdk.KeywordRecognitionModel("dd238e75-10d4-4c44-a691-9098aeac7e28.table")
# The phrase your keyword recognition model triggers on, matching the keyword used to train the above table.
keyword = "Hey Clippy"
# Create a local keyword recognizer with the default microphone device for input.
keyword_recognizer = speechsdk.KeywordRecognizer()
done = False
def recognized_cb(evt):
# Only a keyword phrase is recognized. The result cannot be 'NoMatch'
# and there is no timeout. The recognizer runs until a keyword phrase
# is detected or recognition is canceled (by stop_recognition_async()
# or due to the end of an input file or stream).
result = evt.result
if result.reason == speechsdk.ResultReason.RecognizedKeyword:
print("RECOGNIZED KEYWORD: {}".format(result.text))
nonlocal done
done = True
def canceled_cb(evt):
result = evt.result
if result.reason == speechsdk.ResultReason.Canceled:
print('CANCELED: {}'.format(result.cancellation_details.reason))
nonlocal done
done = True
# Connect callbacks to the events fired by the keyword recognizer.
keyword_recognizer.recognized.connect(recognized_cb)
keyword_recognizer.canceled.connect(canceled_cb)
# Start keyword recognition.
result_future = keyword_recognizer.recognize_once_async(model)
print('Clippy is ready to help...'.format(keyword))
result = result_future.get()
# Read result audio (incl. the keyword).
if result.reason == speechsdk.ResultReason.RecognizedKeyword:
crickit.servo_2.angle = 100
time.sleep(.5)
crickit.servo_2.angle = 150
Responding_To_KW()
def Responding_To_KW():
# Let's add our api keys and other api settings here
speech_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#REPLACE X's WITH YOUR AZURE SPEECH SERVICES API KEY!!!
service_region = "xxxxxxx"
#REPLACE X's WITH YOUR AZURE SERVICE REGION!!!
openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxx" #REPLACE X's WITH YOUR OPENAI API KEY!!!
# Let's configure our speech services settings here
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Set voice, there are many to choose from in Azure Speech Studio
speech_config.speech_synthesis_voice_name = "en-US-GuyNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
# Set response string
resp_text = "How can I help?"
# say response
result = speech_synthesizer.speak_text_async(resp_text).get()
# Wait until finished talking
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
# Then listen for a response
speech_recognition_result = speech_recognizer.recognize_once_async().get()
# After a response is heard
if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
#print the response to the console
print("Recognized: {}".format(speech_recognition_result.text))
#Move eyebrows to signal question received
crickit.servo_2.angle = 100
crickit.servo_1.angle = 90
time.sleep(.5)
crickit.servo_1.angle = 140
time.sleep(.5)
crickit.servo_2.angle = 150
# Check to see if chat mode is initiated
if speech_recognition_result.text == "Let's chat.":
# Set response
resp_text = "Ok, what would you like to chat about?"
# Print, then say response
print(resp_text)
result = speech_synthesizer.speak_text_async(resp_text).get()
#wait until done speaking
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#Configure chat settings
system_message = {"role": "system", "content": "You are Clippy, the digital assistant, and you provide succinct and helpful advice"}
max_response_tokens = 250
token_limit= 4096 #this is the token limt for GPT3.5, adjust if using another model
conversation=[]
conversation.append(system_message) #this keeps the system role in the conversation
# Here is where we count the tokens
def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
encoding = tiktoken.encoding_for_model(model)
num_tokens = 0
for message in messages:
num_tokens += 4
# every message follows <im_start>{role/name}\n{content}<im_end>\n
for key, value in message.items():
num_tokens += len(encoding.encode(value))
if key == "name":
# if there's a name, the role is omitted
num_tokens += -1
# role is always required and always 1 token
num_tokens += 2
# every reply is primed with <im_start>assistant
return num_tokens
while(True):
#Now we start listening
speech_recognition_result = speech_recognizer.recognize_once_async().get()
if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
#Do the eybrow thing
crickit.servo_2.angle = 100
time.sleep(.5)
crickit.servo_2.angle = 150
#print what it heard
print("Recognized: {}".format(speech_recognition_result.text))
user_input = speech_recognition_result.text
# Append the latest prompt to the conversation
conversation.append({"role": "user", "content": user_input})
# and do the token count
conv_history_tokens = num_tokens_from_messages(conversation)
# check token count
while (conv_history_tokens+max_response_tokens >= token_limit):
# And delete the top section if count is too high
del conversation[1]
conv_history_tokens = num_tokens_from_messages(conversation)
response = openai.ChatCompletion.create(
model="gpt-3.5-turbo", # Set the model to be used
messages = conversation, #send the conversation history
temperature=.6, #set the temperature, lower is more specific, higher more random
max_tokens=max_response_tokens, #set max tokens based on count
)
#format conversation and print response
conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
response_text = response['choices'][0]['message']['content'] + "\n"
#print and say response
print(response_text)
result = speech_synthesizer.speak_text_async(response_text).get()
#check for exit phrase
if "I'm done" in speech_recognition_result.text:
keyword_from_microphone()
# If not chat mode, then...
else:
#Send question as prompt to ChatGPT
completion_request = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
#Here's where you pick which model to use
messages = [
#The system role is set here, where you can somewhat guide the response personality
{"role": "system", "content": "You are Clippy, the digital assistant, and you provide succinct and helpful advice"},
#This is where the prompt is set
{"role": "user", "content": (speech_recognition_result.text)},
],
max_tokens=250,
#Max number of tokens used
temperature=0.6,
#Lower is more specific, higher is more creative responses
)
#Get and print response
response_text = completion_request.choices[0].message.content
print(response_text)
#Say response
result = speech_synthesizer.speak_text_async(response_text).get()
#Go back once done talking
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
keyword_from_microphone()
keyword_from_microphone()
CreditsDavid Packman 3 projects • 30 followersI make robot friendsFollow
ContactContactComments
Related channels and tagsartificial intelligenceroboticsspeech recognitiontext to speech