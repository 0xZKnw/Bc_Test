import hashlib
import time as t

class Block:
    def __init__(self, id, pHash, data):
        self.id = id
        self.pHash = pHash
        self.time = t.time()
        self.data = data
        self.hash = self.hashBlock()

    def hashBlock(self):
        sha = hashlib.sha256()
        sha.update(f"{self.id}{self.pHash}{self.time}{self.data}".encode('utf-8'))
        return sha.hexdigest()