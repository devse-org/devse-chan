bin_PROGRAMS = devse-irc-agent
devse_irc_agent_SOURCES = main.c
devse_irc_agent_CPPFLAGS = $(MOSQUITTO_CPPFLAGS) $(CONFIG_CPPFLAGS) -DLOCALEDIR='"$(localedir)"'
devse_irc_agent_LDADD = $(MOSQUITTO_LIBS) $(CONFIG_LIBS)
