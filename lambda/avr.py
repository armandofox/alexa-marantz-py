import telnetlib
import time
import sys

class AVR():


    MARANTZ_IP = '52.119.117.101'
    MARANTZ_PORT = 28147
    DELAY_BETWEEN_COMMANDS = 0.2

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
                conn.write(command + "\r")
                time.sleep(self.delay)
            result = 'OK'
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            result = "{} ({}:{})".format(str(err), exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno)
        conn.close()
        return(result)
