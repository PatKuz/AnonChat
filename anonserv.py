import socket, sys, os, threading

class colors:
    RED = '\033[31m'
    YELLOW = '\33[33m'
    GREEN = '\33[32m'
    PINK = '\33[35m'
    WHITE = '\33[37m'

def header():
    return(colors.RED + '''
▄▄▄       ███▄    █  ▒█████   ███▄    █     ▄████▄   ██░ ██  ▄▄▄     ▄▄▄█████▓
▒████▄     ██ ▀█   █ ▒██▒  ██▒ ██ ▀█   █    ▒██▀ ▀█  ▓██░ ██▒▒████▄   ▓  ██▒ ▓▒
▒██  ▀█▄  ▓██  ▀█ ██▒▒██░  ██▒▓██  ▀█ ██▒   ▒▓█    ▄ ▒██▀▀██░▒██  ▀█▄ ▒ ▓██░ ▒░
░██▄▄▄▄██ ▓██▒  ▐▌██▒▒██   ██░▓██▒  ▐▌██▒   ▒▓▓▄ ▄██▒░▓█ ░██ ░██▄▄▄▄██░ ▓██▓ ░
 ▓█   ▓██▒▒██░   ▓██░░ ████▓▒░▒██░   ▓██░   ▒ ▓███▀ ░░▓█▒░██▓ ▓█   ▓██▒ ▒██▒ ░
 ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▒░   ▒ ▒    ░ ░▒ ▒  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒ ░░
  ▒   ▒▒ ░░ ░░   ░ ▒░  ░ ▒ ▒░ ░ ░░   ░ ▒░     ░  ▒    ▒ ░▒░ ░  ▒   ▒▒ ░   ░
  ░   ▒      ░   ░ ░ ░ ░ ░ ▒     ░   ░ ░    ░         ░  ░░ ░  ░   ▒    ░
      ░  ░         ░     ░ ░           ░    ░ ░       ░  ░  ░      ░  ░
                                            ░
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-(By PKuz)-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    ''')

ZOMBIES = []
USERS = {}

def server_start():
    try:
        IP = str(sys.argv[1])
        PORT = int(sys.argv[2])
    except:
        print(colors.RED + "[*] Usage: python3 server.py <IP> <PORT>" + colors.WHITE)
        sys.exit()

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((IP,PORT))
        server.listen(10)
        print(header())
        print(colors.RED + '[' + colors.GREEN + '*' + colors.RED + '] Server successfully started on ' + IP + ':' + str(PORT) + '.' + colors.WHITE)
        serv_key = gen_key(15)
        print(colors.RED + '[' + colors.GREEN + '*' + colors.RED + '] Key: ' + serv_key + colors.WHITE)
    except:
        print(colors.RED + '[' + colors.YELLOW + '*' + colors.RED + '] Unable to start server on ' + IP + ':' + str(PORT) + '.' + colors.WHITE)
        sys.exit()
    try:
        while(1):
            c, a = server.accept()
            creds = c.recv(2048).decode().split()
            creds[1] = ' '.join(creds[1])
            if creds[0] != str(serv_key):
                import time
                kickMSG = '[*] Kicked for invalid server credentials or duplicate username.'
                c.send(bytes(kickMSG.encode()))
                print(colors.YELLOW + 'Zombie kicked from ' + str(a) + ' for incorrect key.')
                time.sleep(0.03)
                c.close()
            elif creds[1] in USERS.values():
                c.close()
                print(colors.YELLOW + 'Zombie kicked from ' + str(a) + ' for duplicate username.')
            else:
                print(colors.GREEN + 'Zombie connected from ' + str(a))
                USERS[str(a)] = creds[1]
                ZOMBIES.append(c)
                anon = header()
                c.send(bytes(anon.encode()))
                thread = threading.Thread(target=vacuum, args=(c,a))
                thread.start()
    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colors.RED + '[' + colors.YELLOW + '*' + colors.RED + '] Server closed.' + colors.WHITE)
        server.close()
        os._exit(1)

def vacuum(c,a):
    while(1):
        info = c.recv(2048).decode()
        if not info:
            print(colors.YELLOW + 'Zombie disconnected from ' + str(a) + '.')
            del USERS[str(a)]
            ZOMBIES.remove(c)
            c.close()
            break
        info = USERS[str(a)] + ': ' + info
        for z in ZOMBIES:
            z.send(info.encode())

def gen_key(x):
    import secrets
    return secrets.token_hex(x)

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    server_start()
