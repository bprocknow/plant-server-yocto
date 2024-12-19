import serial
import sys

def send_command(port="/dev/ttyS0", baudrate=9600, led_state=1):
    try:
        # Open the serial connection
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1  # Set timeout to 1 second
        )

        # Define packet components
        START_BYTE = 0x7E
        COMMAND_BYTE = 0x01
        PAYLOAD_LENGTH = 0x01
        PAYLOAD_BYTE = 0x01 if led_state else 0x00
        CHECKSUM = START_BYTE ^ COMMAND_BYTE ^ PAYLOAD_LENGTH ^ PAYLOAD_BYTE  # XOR checksum

        # Create the packet
        packet = bytes([START_BYTE, COMMAND_BYTE, PAYLOAD_LENGTH, PAYLOAD_BYTE, CHECKSUM])

        # Send the packet
        ser.write(packet)

        # Close the serial connection
        ser.close()

        return 0  # Success

    except serial.SerialException as e:
        print(f"Serial exception: {e}")
        return 1  # Failure due to serial issue
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 2  # Other failure

if __name__ == "__main__":
    # Example: Turn the LED on

    if len(sys.argv) != 2:
        print("Command line arg 0 - on/off")
        exit(1)

    arg = sys.argv[1].lower()
    if arg == "1":
        led_state = 1
    elif arg == "0":
        led_state = 0
    else:
        print("Invalid input - 1/0 only")
        exit(1)

    result = send_command(led_state=led_state)  # Change `led_state=0` to turn off
    exit(result)

