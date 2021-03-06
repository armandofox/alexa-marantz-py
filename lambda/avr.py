import telnetlib
import time
import sys
import os

class AVR():


    MARANTZ_IP = os.environ["IP"]
    MARANTZ_PORT = os.environ["PORT"]
    DELAY_BETWEEN_COMMANDS = 0.3

    def __init__(self, ip=MARANTZ_IP, port=MARANTZ_PORT):
        self.ip = ip
        self.port = port
        self.delay = AVR.DELAY_BETWEEN_COMMANDS

    def send(self, commands):
        if not isinstance(commands,list):
            commands = [commands]
        try:
            conn = telnetlib.Telnet()
            conn.open(self.ip, self.port, 3)
            for command in commands:
                conn.write((command + "\r").encode('ascii'))
                time.sleep(self.delay)
            result = 'OK'
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            result = "{} ({}:{})".format(str(err), exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno)
        conn.close()
        return(result)
