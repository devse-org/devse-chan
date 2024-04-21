
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#include "devse_config.h"
#include "gettext.h"
#include "irc.h"
#include "logger.h"

#define _(x) gettext(x)

int
main(int argc, char **argv)
{
#ifdef ENABLE_NLS
	setlocale(LC_ALL, "");
	bindtextdomain(PACKAGE, LOCALEDIR);
	textdomain(PACKAGE);
#endif /* ENABLE_NLS */

	logger_init_default();
	config_init_default();

	config_from_cmd(argc, argv);



	return (EXIT_SUCCESS);
}
