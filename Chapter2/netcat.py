"""

    Copyright Thomas T.
    All Rights reserved.


"""
import argparse
import socket

class NetCat():

    def __init__(self):
        args = self._usage()

        listen = args.listen
        command = args.command
        upload = False
        execute = args.execute
        target = args.target
        upload_destination = args.upload
        port = args.port
        print("")


    def _usage(self):
        example_text = '''Examples:

         python netcat.py -t 192.168.0.1 -p 5555 -l -c
         python netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe 
         python netcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"
         echo 'ABCDEFGHI' | python ./netcat.py -t 192.168.11.12 -p 135
         
         '''

        parser = argparse.ArgumentParser(
            description='Net Cat Tool',
            epilog=example_text,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        parser.add_argument(
            '-t',
            '--target',
            metavar='ip_address',
            type=str,
            help=" - Target ip address"
        )
        parser.add_argument(
            '-p',
            '--port',
            metavar='port_number',
            type=int,
            help=" - Port Number"
        )
        parser.add_argument(
            '-l',
            '--listen',
            action="store_true",
            help=" - listen on [host] : [port] for incoming connections"
        )
        parser.add_argument(
            '-e',
            '--execute',
            type=str,
            metavar='./file_to_run',
            help=" - execute the given file upon receiving a connection"
        )
        parser.add_argument(
            '-c',
            '--command',
            action="store_true",
            help=" - initialize a command shell"
        )
        parser.add_argument(
            '-u',
            '--upload',
            type=str,
            metavar='destination',
            help=" - upon receiving connection upload a file and write to [destination]"
        )

        return parser.parse_args()

    def client_sender(self, send_string: str):

        assert self.target is not None
        assert self.port is not None

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data.
            sock.connect((self.target, self.port))

            # Send data encoded, sendall() is dirty lie.
            sock.send(send_string.encode())

            # Return data from the server and shut down
            received = str(sock.recv(1024), "utf-8")

    def start(self):

        if self.listen == True:
            # Server Loop
            pass
        elif self.listen == False and self.target is not None and self.port is not None:
            # Read in data, and Send it to target
            read = input()
            read = str(read)
            if len(read) > 0:
                self.client_sender(read)


if __name__ == "__main__":
    nc = NetCat()
    nc.start()
