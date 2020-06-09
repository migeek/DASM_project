from gpiozero import Button
from gpiozero import LED

#global contacts list
contacts = [None] * 4

#read in button from GPIO2 (see pinout)
recordbutton = Button(2)
recordled = LED(14)

#read in button from GPIO3 (see pinout)
playbutton = Button(3)
playled = LED(15)

#read in button from GPIO4 (see pinout)
sendbutton = Button(4)
sendled = LED(18)

#read in button from GPIO25 (see pinout)
person1button = Button(25)
person1led = LED(0)
person1on = False

#read in button from GPIO11 (see pinout)
person2button = Button(11)
person2led = LED(5)
person2on = False

#read in button from GPIO16 (see pinout)
person3button = Button(16)
person3led = LED(6)
person3on = False

#read in button from GPIO1 (see pinout)
person4button = Button(1)
person4led = LED(13)
person4on = False

#unique counter for sending messages
fileCounter = 0

#unique box ID
boxID = 200
