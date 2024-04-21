bin_PROGRAMS = devse-irc-agent
devse_irc_agent_SOURCES = main.c config.c
devse_irc_agent_CPPFLAGS = $(CONFIG_CPPFLAGS) \
						-I$(top_srcdir)/lib \
						-DLOCALEDIR='"$(localedir)"' 
devse_irc_agent_LDADD = ../../lib/libdevse.a $(CONFIG_LIBS) @LIBINTL@
