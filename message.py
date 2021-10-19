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