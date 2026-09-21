import socket
import struct
import time

MAGIC = bytes.fromhex('00ffff00fefefefefdfdfdfd12345678')
host = 'np.hanasand.com'
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(4)
    stamp = int(time.time() * 1000)
    request = b'\x01' + struct.pack('>Q', stamp) + MAGIC + struct.pack('>Q', 443)
    for attempt in range(3):
        s.sendto(request, (host, 443))
        try:
            data, peer = s.recvfrom(4096)
            break
        except socket.timeout:
            if attempt == 2:
                raise
    assert data[0] == 0x1c and data[1:9] == request[1:9]
    assert data[17:33] == MAGIC
    length = int.from_bytes(data[33:35], 'big')
    motd = data[35:35+length].decode()
    assert 'Name Pending' in motd, motd
    print('Bedrock UDP 443:', motd)
    request = b'\x05' + MAGIC + b'\x0b' + bytes(1172 - 18)
    s.sendto(request, (host, 443))
    data, peer = s.recvfrom(4096)
    assert data[0] == 6 and data[1:17] == MAGIC, data.hex()
    print('RakNet connection negotiation: OK')
