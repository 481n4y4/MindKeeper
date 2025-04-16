import serial.tools.list_ports

def is_esp_connected():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "CP210" in port.description or "CH340" in port.description:
            return True
    return False
