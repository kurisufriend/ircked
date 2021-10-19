import socket

def default_event_handler(msg, ctx):
    print("<<", str(msg))
    if msg.command == "PING":
        message.manual("", "PONG", msg.parameters).send(ctx.socket)
    if msg.command == "001":
        message.manual("", "JOIN", ["#qrs"]).send(ctx.socket)
    if msg.command == "PRIVMSG" and "\x01VERSION\x01" in msg.parameters:
        message.manual(":"+msg.parameters[0], "PRIVMSG", [msg.prefix[1:].split("!")[0], ":\x01dorfl bot\x01"]).send(s)

class message:
    def __init__(self):
        self.prefix = ""
        self.command = ""
        self.parameters = []
    @staticmethod
    def parse(raw):
        msg = message()
        try:
            raw = raw.split(" ")
            msg.prefix = "" if not(raw[0].startswith(":")) else raw[0]
            if msg.prefix: 
                raw.pop(0)
            msg.command = raw[0]
            msg.parameters = raw[1:][0:15]
        except:
            pass
        return msg
    @staticmethod
    def manual(pre, com, par):
        msg = message()
        msg.prefix = pre
        msg.command = com
        msg.parameters = par
        return msg
    def __str__(self):
        return ("" if not self.prefix else self.prefix+" ") + self.command + " " + (" ".join(self.parameters) if not(type(self.parameters) == type(str)) else self.parameters)
    def send(self, sock):
        sock.send((str(self)+"\r\n").encode("utf-8"))
        print(self.parameters)
        print(">>", str(self))

class privmsg:
    def __init__(self):
        self.msg = message()
    @staticmethod
    def build(fro, to, body):
        pm = privmsg()
        pm.msg.prefix = ":"+fro
        pm.msg.command = "PRIVMSG"
        pm.msg.parameters[0] = to
        for word in body.split(" "):
            pm.msg.parameters.append(word)
        pm.msg.parameters[1] = ":"+pm.msg.parameters[1]

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

dorfl = bot()
dorfl.connect_register("irc.rizon.net", 7000)

dorfl.run()
s.close()