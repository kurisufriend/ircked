import socket
from ircked.message import *
def default_event_handler(msg, ctx):
    print("<<", str(msg))
    if msg.command == "PING":
        message.manual("", "PONG", msg.parameters).send(ctx.socket)
    elif msg.command == "001":
        message.manual("", "JOIN", ["#qrs"]).send(ctx.socket)
    elif msg.command == "PRIVMSG" and "\x01VERSION\x01" in msg.parameters:
        message.manual(":"+msg.parameters[0], "PRIVMSG", [msg.prefix[1:].split("!")[0], ":\x01dorfl bot\x01"]).send(ctx.socket)
    if msg.command == "PRIVMSG":
        pm = privmsg.parse(msg)
        if pm.bod == ".hello":
            privmsg.build(ctx.nick, pm.to, "hello, world!").msg.send(ctx.socket)
class irc_bot:
    def __init__(self, nick="dorfl", user="dorfl", real="dorfl"):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con_to = ()
        self.nick = nick
        self.user = user
        self.real = real
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
    def sendraw(self, msg):
        msg.send(self.socket)