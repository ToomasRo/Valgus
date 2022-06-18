import serial
import time

bluetooth = None


def init(comport):
    print("Start")
    # This will be different for various devices and on windows it will probably be a COM port.
    port = comport
    # Start communications with the bluetooth unit
    bluetooth = serial.Serial(port, 9600)
    print("Connected")
    bluetooth.flushInput()  # This gives the bluetooth a little kick


def close():
    bluetooth.close()  # Otherwise the connection will remain open until a timeout which ties up the /dev/thingamabob
    print("Done")


def send(data):
    print(f"Sending {data}")
    bluetooth.write(data.encode("utf-8"))


def main():
    init("COM4")
    send("A-1")
    close()


if __name__ == "__main__":
    main()
