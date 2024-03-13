bin_PROGRAMS = devse-core
devse_core_SOURCES = main.c
devse_core_CPPFLAGS = $(MOSQUITTO_CPPFLAGS) \
						$(CONFIG_CPPFLAGS) \
						-I$(top_srcdir)/lib \
						-DLOCALEDIR='"$(localedir)"' 
devse_core_LDADD = $(MOSQUITTO_LIBS) $(CONFIG_LIBS) @LIBINTL@
