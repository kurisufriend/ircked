import socket
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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("irc.rizon.net", 7000))
#s.send("PASS none\r\n".encode("utf-8"))
s.send("USER dorfl 0 * :dorfl\r\n".encode("utf-8"))
s.send("NICK dorfl\r\n".encode("utf-8"))

while True:
    data = s.recv(512).decode("utf-8")
    if not data: continue
    msgs = [message.parse(raw) for raw in [part for part in data.split("\r\n") if part]]
    for msg in msgs:
        print("<<", str(msg))
        if msg.command == "PING":
            message.manual("", "PONG", msg.parameters).send(s)
        if msg.command == "001":
            message.manual("", "JOIN", ["#qrs"]).send(s)
        if msg.command == "PRIVMSG" and "\x01VERSION\x01" in msg.parameters:
            message.manual(":"+msg.parameters[0], "PRIVMSG", [msg.prefix[1:].split("!")[0], ":\x01dorfl bot\x01"]).send(s)
s.close()