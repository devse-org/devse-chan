bin_PROGRAMS = devse-core
devse_core_SOURCES = main.c
devse_core_CPPFLAGS =  $(CONFIG_CPPFLAGS) \
						-I$(top_srcdir)/lib \
						-DLOCALEDIR='"$(localedir)"' 
devse_core_LDADD = ../lib/libdevse.a $(CONFIG_LIBS) @LIBINTL@
