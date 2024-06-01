import socket

target = input("Enter the target IP address: ")
ports = [80, 21, 412, 81, 82]

def port_scan(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((target, port))
        if result == 0:
            print("Port {} is open".format(port))
        else:
            print("Port {} is closed".format(port))
        sock.close()
    except Exception as e:
        print("Error occurred:", e)

for port in ports:
    port_scan(target, port)
