from .bot import irc_bot

dorfl = irc_bot()
dorfl.connect_register("irc.rizon.net", 7000)

dorfl.run()
