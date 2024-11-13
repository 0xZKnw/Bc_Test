import block as b
import chain as c
import node as n
import threading
import time

chain = c.Bc()

node_1 = n.Node('192.168.173.185', 5006)
server_thread = threading.Thread(target=node_1.start_server)
server_thread.start()
node_1.connect_to_peer('192.0.0.2', 5006)
bcList = chain.getChain()
node_1.broadcast_message(f"{bcList[0].id}:{bcList[0].pHash}:{bcList[0].hash}:{bcList[0].data}:{chain.getLenChain()}\n")
while True:
    cmd = str(input(""))

    if "addBlock" in cmd:
        chain.addBlock(cmd.replace("addBlock ", ""))

    if time.time() - chain.getChain()[-1].time <= 5:
        msg = f"{bcList[-1].id}:{bcList[-1].pHash}:{bcList[-1].hash}:{bcList[-1].data}:{chain.getLenChain()}\n"
        node_1.broadcast_message(msg)
        time.sleep(5)