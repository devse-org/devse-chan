AC_INIT([DevSE-Chan], [2.0], [], [devsechan], [])
AM_INIT_AUTOMAKE([foreign subdir-objects])

AC_CONFIG_HEADERS([devse_config.h])

AH_TOP([
#ifndef DEVSE_CONFIG_H
# define DEVSE_CONFIG_H 1
])

AH_BOTTOM([
#endif /* !DEVSE_CONFIG_H */
])

AM_GNU_GETTEXT([external])
AM_GNU_GETTEXT_VERSION([0.21])

AC_LANG(C)
AC_PROG_CC
AC_PROG_CPP
AC_PROG_RANLIB
AM_PROG_AR
AM_PROG_CC_C_O

AC_CHECK_INCLUDES_DEFAULT
AC_C_CONST

PKG_CHECK_MODULES(MOSQUITTO, libmosquitto)
PKG_CHECK_MODULES(CONFIG, libconfig)

AC_CONFIG_FILES([Makefile
				devse-core/Makefile
				devse-irc-agent/Makefile
				po/Makefile.in])
AC_OUTPUT
