
class Rcon:
    def __init__(self, host, port, password, timeout):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
        self.socket = None
        self.authorized = False
        self.last_response = ''

    PACKET_AUTHORIZE = 5
    PACKET_COMMAND = 6

    SERVERDATA_AUTH = 3
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_RESPONSE_VALUE = 0

    def get_response(self):
        return self.last_response

    def connect(self):
        import socket
        try:
            self.socket = socket.create_connection((self.host, self.port), self.timeout)
        except Exception as e:
            self.last_response = str(e)
            return False
        self.socket.settimeout(3)
        return self.authorize()

    def disconnect(self):
        if self.socket:
            self.socket.close()

    def is_connected(self):
        return self.authorized

    def send_command(self, command):
        if not self.is_connected():
            return False
        self.write_packet(self.PACKET_COMMAND, self.SERVERDATA_EXECCOMMAND, command)
        response_packet = self.read_packet()
        if response_packet['id'] == self.PACKET_COMMAND:
            if response_packet['type'] == self.SERVERDATA_RESPONSE_VALUE:
                self.last_response = response_packet['body']
                return response_packet['body']

        return False

    def authorize(self):
        self.write_packet(self.PACKET_AUTHORIZE, self.SERVERDATA_AUTH, self.password)
        response_packet = self.read_packet()

        if response_packet['type'] == self.SERVERDATA_AUTH_RESPONSE:
            if response_packet['id'] == self.PACKET_AUTHORIZE:
                self.authorized = True
                return True

        self.disconnect()
        return False

    def write_packet(self, packet_id, packet_type, packet_body):
        packet = (packet_id.to_bytes(4, 'little') + 
                  packet_type.to_bytes(4, 'little') + 
                  packet_body.encode('utf-8') + b'\x00' + 
                  b'\x00')
        packet_size = len(packet)

        packet = packet_size.to_bytes(4, 'little') + packet
        self.socket.sendall(packet)
    def read_packet(self):
        size_data = self.socket.recv(4)
        size = int.from_bytes(size_data, 'little')
        packet_data = self.socket.recv(size)
        packet_id, packet_type = int.from_bytes(packet_data[0:4], 'little'), int.from_bytes(packet_data[4:8], 'little')
        body = packet_data[8:-1].decode('utf-8')

        return {'id': packet_id, 'type': packet_type, 'body': body}
