"""
The purpose of this script is to get the running-config of a Cisco device through a serial connection, as a CLI tool
"""

import sys
import serial
import time

def login(ser, username, password):
    # Wait for the device to send the login prompt
    time.sleep(2)
    ser.write(username.encode('ascii') + b"\r")

    # Wait to get the prompt back for password
    time.sleep(2)
    ser.write(password.encode('ascii') + b"\r")
    print("Authenticating... Please wait")
    # If the device uses radius authentication, wait until it falls back to local authentication
    time.sleep(20)

def main():
    # Get the serial port from the command line arguments
    serial_port = sys.argv[1]

    # get output file path as txt from command line arguments
    output_file = sys.argv[2]

    # Authentication username and password as optional command line arguments
    username = sys.argv[3]
    password = sys.argv[4]

    # Create a serial connection
    ser = serial.Serial(
        serial_port, 9600, timeout=10, parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS
    )

    # Login to the device if username and password are provided
    if username and password:
        login(ser, username, password) # login function is defined above
    # If the device uses radius authentication, wait until it falls back to local authentication
    time.sleep(10)
    ser.write(password.encode('ascii') + b"\r")
    time.sleep(2)

    print("Sending command to get running-config...")
    # Send the command to get the running-config
    ser.write(b"show run\r")

    # Wait for the device to respond
    time.sleep(2)

    # Read the response
    response = ser.read(ser.inWaiting())
    print("Response below should be the running-config")
    # Print the response
    print(response)

    # Write the response to a file
    with open(output_file, "w") as f:
        f.write(response.decode("utf-8"))

    # Close the serial connection
    ser.close()
    # example: python get-config.py /dev/ttyUSB0 running-config.txt admin admin or
    # python get-config.py /dev/ttyUSB0 running-config.txt


if __name__ == "__main__":
    main()
