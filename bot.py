import socket
from message import *
def default_event_handler(msg, ctx):
    print("<<", str(msg))
    if msg.command == "PING":
        message.manual("", "PONG", msg.parameters).send(ctx.socket)
    if msg.command == "001":
        message.manual("", "JOIN", ["#qrs"]).send(ctx.socket)
    if msg.command == "PRIVMSG" and "\x01VERSION\x01" in msg.parameters:
        message.manual(":"+msg.parameters[0], "PRIVMSG", [msg.prefix[1:].split("!")[0], ":\x01dorfl bot\x01"]).send(s)
class bot:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con_to = ()
        self.nick = "dorfl"
        self.user = "dorfl"
        self.real = "dorfl"
        self.behaviour = {}
    def connect_register(self, addy, port):
        self.socket.connect((addy, port))
        self.socket.send(f"USER {self.user} 0 * :{self.real}\r\n".encode("utf-8"))
        self.socket.send(f"NICK {self.nick}\r\n".encode("utf-8"))
        self.con_to = (addy, port)
    def run(self, event_handler = default_event_handler):
        while True:
            data = self.socket.recv(512).decode("utf-8")
            if not data: continue
            msgs = [message.parse(raw) for raw in [part for part in data.split("\r\n") if part]]
            for msg in msgs:
                event_handler(msg, self)