"""

    Copyright Thomas T.
    All Rights reserved.


"""
import argparse
import socket
import socketserver
import sys



class MyBigFatTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        # Note this will only accept the first 1024 bytes of the data.
        self.data = self.request.recv(1024).strip()

        # Write out data to Server Console.
        print("{} wrote:".format(self.client_address[0]))
        # Write out byte string
        print(self.data)
        # Write out normal string
        print(str(self.data, 'utf-8'))

        # Just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


class NetCat():

    def __init__(self):
        args = self._usage()

        self.listen = args.listen
        self.command = args.command
        self.upload = False
        self.execute = args.execute
        self.target = args.target
        self.upload_destination = args.upload
        self.port = args.port
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


    def _read_input_and_send(self):
        # Read in data, and Send it to target
        while True:
            read = input()
            read = str(read)
            if len(read) > 0:
                self.client_sender(read)

    def client_sender(self, send_string: str):

        assert self.target is not None
        assert self.port is not None

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data.
            sock.connect((self.target, self.port))

            # Send data encoded, sendall() is dirty lie.
            sock.send(send_string.encode())

            # Return data from the server and shut down
            recv = sock.recv(1024)
            response = str(recv, "utf-8")
            while sys.getsizeof(recv) > 1024:
                recv = sock.recv(1024)
                response += str(recv, "utf-8")

            print(response)

    def server_loop(self):

        # If no target is defined, we listen on all interfaces
        if self.target is None:
            self.target = "0.0.0.0"

        # Create the server, binding to localhost on port 9999
        with socketserver.TCPServer((self.target, self.port), MyBigFatTCPHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()



    def start(self):

        if self.listen == True:
            # Server Loop
            self.server_loop()

        elif self.listen == False and self.target is not None and self.port is not None:
            self._read_input_and_send()


if __name__ == "__main__":
    nc = NetCat()
    nc.start()
