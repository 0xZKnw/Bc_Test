import block as b

class Bc:
    def __init__(self):
        self.chain = [self.genesis()]

    def genesis(self):
        return b.Block(0, "0", "Genesis Block")
    
    def addBlock(self, data):
        previousBlock = self.chain[-1]
        newBlock = b.Block(len(self.chain), previousBlock.hash, data)
        self.chain.append(newBlock)

    def isChainValid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.hash != current.hashBlock() or current.pHash != previous.hash:
                return False
        return True
    
    def getChain(self):
        return self.chain
    
    def getLenChain(self):
        return len(self.chain)
