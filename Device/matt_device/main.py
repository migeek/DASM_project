import os, signal, time
from box_client import *
from gpiozero import Button
from gpiozero import LED
from pydub import AudioSegment
import globals as g

# start the client 
start_client()

# main loop 
def client_box_main():
    while True:
        record_and_send()
        play_recording()

#function for recording message and then sending it
def record_and_send():
    if g.recordbutton.is_pressed:

        person_leds_off() # turns off all person LEDs
        g.recordled.on()

        g.fileCounter += 1

        # Create a child process
        pid = os.fork() 

        if pid: 
            print("\nIn parent process") 
            time.sleep(2)

            #pushing record button second time ends the loop
            while True:
                if g.recordbutton.is_pressed:
                    g.recordled.off()
                    break

            os.kill(pid, signal.SIGTERM) 

            fileName = "audio-" + str(g.boxID) + "-" + str(g.fileCounter)

            #convert .wav to .mp3
            song = AudioSegment.from_wav(fileName + ".wav")
            song.export(fileName + ".mp3", format="mp3")
       
            print("Signal sent, child interrupted.") 
            print("record loop")
            while True:
                if g.playbutton.is_pressed:
                    play_audio(fileName + ".mp3")
                if g.sendbutton.is_pressed:
                    destIDs = []
                    #choosing who to send messages to
                    if g.person1on and g.contacts[0] != None:
                        destIDs.append(g.contacts[0])
                    if g.person2on and g.contacts[1] != None:
                        destIDs.append(g.contacts[1])
                    if g.person3on and g.contacts[2] != None:
                        destIDs.append(g.contacts[2])
                    if g.person3on and g.contacts[3] != None:
                        destIDs.append(g.contacts[3])
                    for destID in destIDs:
                        print("send to dest ", destID)
                        #send audio once you have list of destinations
                        send_audio(destID)
                    print("done recording")
                    g.sendled.off()
                    person_leds_off()
                    break

        else: 
            print("In child process") 
            print("Process ID:", os.getpid()) 
            print("Recording audio")

            #recording message
            #args is the command you would run on command line to record message using our microphone
            fileName = "audio-" + str(g.boxID) + "-" + str(g.fileCounter)
            args = ("arecord", "-D", "dmic_sv", "-c2", "-r", "48000", "-f", "S32_LE", "-t", "wav", "-V", "mono", "-v", fileName + ".wav") # change audio name
            os.execvp("arecord", args)

#function for playing message(s) from contact
def play_recording():
    if g.playbutton.is_pressed:
        g.playled.on()
        files = []
        #choose the contact you want to listen to and then play their message using play button
        #add them to files[] for playing
        if g.person1on and g.contacts[0] != None:
            fileStart = "audio-" + str(g.contacts[0])
            for fileName in os.listdir('.'):
                if os.path.isfile(os.path.join("./",fileName)) and fileStart in fileName:
                    files.append(fileName)
        if g.person2on and g.contacts[1] != None:
            fileStart = "audio-" + str(g.contacts[1])
            for fileName in os.listdir('.'):
                if os.path.isfile(os.path.join("./",fileName)) and fileStart in fileName:
                    files.append(fileName)
        if g.person3on and g.contacts[2] != None:
            fileStart = "audio-" + str(g.contacts[2])
            for fileName in os.listdir('.'):
                if os.path.isfile(os.path.join("./",fileName)) and fileStart in fileName:
                    files.append(fileName)
        if g.person4on and g.contacts[3] != None:
            fileStart = "audio-" + str(g.contacts[3])
            for fileName in os.listdir('.'):
                if os.path.isfile(os.path.join("./",fileName)) and fileStart in fileName:
                    files.append(fileName)
        #play audio files in files[]
        for f in files:
            play_audio(f)
        g.playled.off()

#function for playing .mp3 files
def play_audio(fileName: str):
    print("play ", fileName)
    pid = os.fork() 

    if pid:
        time.sleep(2)
        while True:
            if pid_exited(pid):
                # play audio terminated
                break
            if g.playbutton.is_pressed:
                # kill audio early
                os.kill(pid, signal.SIGTERM) 
                break
    else:
        # play audio
        args = ("omxplayer", "-o", "local", fileName)
        os.execvp("omxplayer", args)


def person1_pressed():
    g.person1on = not g.person1on # toggle state
    if g.person1on:
        g.person1led.on()
    else:
        g.person1led.off()

def person2_pressed():
    g.person2on = not g.person2on # toggle state
    if g.person2on:
        g.person2led.on()
    else:
        g.person2led.off()

def person3_pressed():
    g.person3on = not g.person3on # toggle state
    if g.person3on:
        g.person3led.on()
    else:
        g.person3led.off()

def person4_pressed():
    g.person4on = not g.person4on # toggle state
    if g.person4on:
        g.person4led.on()
    else:
        g.person4led.off()

def pid_exited(pid):        
    try:
        os.kill(pid, 0)
    except OSError:
        return True
    else:
        return False


def person_leds_off():
    g.person1led.off()
    g.person2led.off()
    g.person3led.off()
    g.person4led.off()
    g.person1on = False
    g.person2on = False
    g.person3on = False
    g.person4on = False

g.person1button.when_pressed = person1_pressed
g.person2button.when_pressed = person2_pressed
g.person3button.when_pressed = person3_pressed
g.person4button.when_pressed = person4_pressed

# execute the main loop            
client_box_main()
