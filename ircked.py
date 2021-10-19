import socket
from bot import bot

dorfl = bot()
dorfl.connect_register("irc.rizon.net", 7000)

dorfl.run()
s.close()