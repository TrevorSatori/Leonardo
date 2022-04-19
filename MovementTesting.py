import serial, serial.tools.list_ports
import time

# pip install pyserial

def main():

    # finds available serial ports
    com = findPort()

    # Serial object
    arduino = serial.Serial(com, 9600, timeout=1)

    # While loop to test mouse movements in game
    while True:
        
        print ("Enter move X")
        moveX = str(input())

        print ("Enter move Y")
        moveY = str(input())

        print ("Moving X coord:", moveX)
        print ("Moving y coord:", moveY)

        # waits 5 seconds to send commands. Gives time to switch to game
        time.sleep(5)

        # writes move comand to serial object
        arduino.write((moveX + ':' + moveY + 'x').encode())

        print('Done. To quit enter q')

        # if q is entered end the program
        if moveX == 'q' or moveY == 'q':
            break


# Finds available ports
def findPort():

    # Find all serial ports available 
    ports = list(serial.tools.list_ports.comports())

    # Create array for storing ports
    choices = []

    # create variable to increment number of choices 
    choiceNum = 0
    print()
    print('select the number of your serial port')

    # add all serial ports to array 
    for i in ports:
        i = str(i).split(' ')
        choices.append(i[0])
        print(str(choiceNum) + ' - ' + i[0])
        choiceNum += 1
    port = int(input())

    # returns serial port to main function
    try:
        return choices[port]
    except:
        print('choose a valid number')
        findPort()

main()
