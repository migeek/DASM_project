from gpiozero import Button
from gpiozero import LED

#global contacts list
contacts = [None] * 4

#read in button from GPIO2 (see pinout)
recordbutton = Button(2)

#read in button from GPIO3 (see pinout)
playbutton = Button(3)

#read in button from GPIO4 (see pinout)
sendbutton = Button(4)

#read in button from GPIO25 (see pinout)
person4button = Button(25)
person4led = LED(0)
person4on = False

#read in button from GPIO8 (see pinout)
person1button = Button(8)
person1led = LED(5)
person1on = False

#read in button from GPIO7 (see pinout)
person2button = Button(7)
person2led = LED(6)
person2on = False

#read in button from GPIO1 (see pinout)
person3button = Button(1)
person3led = LED(13)
person3on = False

#unique counter for sending messages
fileCounter = 0

#unique box ID
boxID = 100
