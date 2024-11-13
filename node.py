import socket
import threading

class Node:
    def __init__(self, host, port):
        '''Création de l'objet Node avec l'hôte, le port et les pairs'''
        self.host = host
        self.port = port
        self.peers = []  # Contient uniquement les connexions sortantes initiées par ce nœud
        self.connections = {}  # Gère les connexions entrantes et leurs adresses
        self.pseudo = str(input("quel est ton pseudo ? : "))

    def start_server(self):
        '''Démarrage du serveur'''
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Écoute sur {self.host}:{self.port}")

        while True:
            conn, addr = server.accept()
            print(f"Connexion acceptée de {addr}")
            
            # Vérification pour éviter les connexions en double
            if addr not in self.connections:
                self.connections[addr] = conn
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        '''Gestion des messages entrants et réponse'''
        print(f"Traitement de la connexion depuis {addr}")
        
        # Connecte uniquement si ce nœud n'a pas initié la connexion
        if '192.0.0.2' != self.host and addr[1] != self.port:
            self.connect_to_peer('192.0.0.2', 5006)  # Remplace par le port approprié si nécessaire
        
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"{data.decode('utf-8')}")
                # Si le message est nouveau, il est diffusé
                #self.broadcast_message(data.decode('utf-8'), addr)
        except Exception as e:
            print(f"Erreur avec {addr}: {e}")
        finally:
            conn.close()
            del self.connections[addr]  # Retire la connexion de la liste
            print(f"Connexion fermée avec {addr}")

    def connect_to_peer(self, host, port):
        '''Connexion aux pairs du réseau'''
        peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if not any(p.getpeername() == (host, port) for p in self.peers):
                peer.connect((host, port))
                self.peers.append(peer)
                print(f"Connecté au pair {host}:{port}")
                #peer.sendall(b"bite")  # Exemple de message d'initialisation
        except Exception as e:
            print(f"Erreur lors de la connexion au pair {host}:{port} : {e}")
            peer.close()

    def broadcast_message(self, message, sender_addr=None):
        '''Diffusion du message aux appareils via les connexions sortantes'''
        for peer in self.peers:
            # Envoie uniquement aux pairs qui ne sont pas les émetteurs originaux
            if sender_addr is None or peer.getpeername() != sender_addr:
                try:
                    m = self.pseudo + " : " + message
                    peer.sendall(m.encode('utf-8'))
                except Exception as e:
                    print(f"Erreur lors de l'envoi au pair : {e}")
                    peer.close()
                    self.peers.remove(peer)

node_1 = Node('192.168.173.185', 5006)
server_thread = threading.Thread(target=node_1.start_server)
server_thread.start()

while True:
    a = input("")
    node_1.broadcast_message(a)
