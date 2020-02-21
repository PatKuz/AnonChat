import socket, os, sys, select

class colors:
    RED = '\033[31m'
    YELLOW = '\33[33m'
    PINK = '\33[35m'
    WHITE = '\33[37m'
    CLEAR = '\033[K'
    PREV = '\033[F'

def client_start():
    try:
        IP = str(sys.argv[1])
        PORT = int(sys.argv[2])
        KEY = str(sys.argv[3])
        NAME = str(sys.argv[4])
    except:
        print(colors.RED + '[*] Usage: python3 server.py <IP> <PORT> <KEY> <USERNAME>' + colors.WHITE)
        sys.exit()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    creds = (KEY + ' ' + NAME).encode()
    s.send(bytes(creds))
    os.system('cls' if os.name == 'nt' else 'clear')
    print(s.recv(2048).decode())

    while(1):
        try:
            s_list = [sys.stdin, s]
            read_s, write_s, error_s = select.select(s_list , [], [])
            for sock in read_s:
                if sock == s:
                    data = sock.recv(2048)
                    if not data:
                        print(colors.RED +'[' + colors.YELLOW + '*' + colors.RED + '] Disconnected from AnonChat server.' + colors.WHITE)
                        sys.exit()
                    else:
                        data = str(data.decode())
                        ind_colon = data.index(':')
                        data = colors.PINK + data[:ind_colon] + colors.RED + data[ind_colon:]
                        sys.stdout.write(data)
                else:
                    msg = str(sys.stdin.readline())
                    sys.stdout.write(colors.PREV)
                    sys.stdout.write(colors.CLEAR)
                    msg = msg.encode()
                    s.send(msg)
        except KeyboardInterrupt:
            print(colors.RED +'\n[' + colors.YELLOW + '*' + colors.RED + '] Disconnected from AnonChat server.' + colors.WHITE)
            sys.exit()

if __name__ == '__main__':
    client_start()
