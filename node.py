import socket
import threading

class Node:
    def __init__(self, host, port):
        '''creation objet Node et initialisation variables host ports et peers'''
        self.host = host
        self.port = port
        self.peers = []
    
    def start_server(self, pseudo):
        '''demarrage du serveur'''
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Écoute sur {self.host}:{self.port}")

        while True:
            conn, addr = server.accept()
            print(f"Connexion acceptée de {addr}")
            threading.Thread(target=self.handleClient, args=(conn, addr)).start()
            self.connect_to_peer(addr[0], 5006, pseudo)

    def handleClient(self, conn, addr):
        '''ecoute message entrant et repond'''
        print(f"Traitement de la connexion depuis {addr}")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Message reçu de {addr}: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Erreur avec {addr}: {e}")
        finally:
            conn.close()
            print(f"Connexion fermée avec {addr}")

    def connect_to_peer(self, host, port, pseudo):
        '''connection aux appareils entrant dans le reseau'''
        peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            peer.connect((host, port))
            self.peers.append(peer)
            print(f"Connecté au pair {host}:{port}")
            peer.sendall(b"psdo:" + pseudo.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de la connexion au pair {host}:{port} : {e}")

    def broadcast_message(self, message):
        '''envoie d'un message a tout les appareils du reseau'''
        for peer in self.peers:
            try:
                peer.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Erreur lors de l'envoi au pair : {e}")
    def close(self):
        self.close()

ipLocal = str(input("ton ip ? : "))
pseudo = str(input("ton pseudo : "))
a = f"{pseudo} : "
node_1 = Node(ipLocal, 5006)
server_thread = threading.Thread(target=node_1.start_server, args=(pseudo,))
server_thread.start()
while a != "STOP":
    a = f"{pseudo} : "
    a += str(input(""))
    node_1.broadcast_message(a)
node_1.close()
