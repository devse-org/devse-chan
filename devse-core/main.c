#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <unistd.h>
#include <locale.h>

#include <mosquitto.h>
#include "devse_config.h"
#include "gettext.h"

#define _(x) gettext(x)

static char *prg_name = "devse-core";

void
fatal(const char *str, ...)
{
	va_list ap;

	fprintf(stderr, "%s: ", prg_name);
	va_start(ap, str);
	vfprintf(stderr, str, ap);
	va_end(ap);
	fprintf(stderr, "\n");

	exit(EXIT_FAILURE);
}

void
version(void)
{
	printf(PACKAGE_NAME " v" PACKAGE_VERSION "\n");
	printf("Copyright (C) 2024 d0p1\n");
	printf("License BSD-3-Clause: <https://directory.fsf.org/wiki/License:BSD-3-Clause>\n");
	printf("This is free software: you are free to change and redistribute it.\n");
	printf("There is NO WARRANTY, to the extent permitted by law.\n");

	exit(EXIT_SUCCESS);
}

void
usage(int retval)
{
	if (retval != EXIT_SUCCESS)
	{
			fprintf(stderr, _("Try '%s -h' for more information.\n"), prg_name);
	}
	else
	{
		printf("Usage: %s [-hV] [-c CONFIG]\n", prg_name);
	}

	exit(retval);
}

int
main(int argc, char **argv)
{
	int c;
	char clientid[24];
	struct mosquitto *mosq;

#ifdef ENABLE_NLS
	setlocale(LC_ALL, "");
	bindtextdomain(PACKAGE, LOCALEDIR);
	textdomain(PACKAGE);
#endif /* ENABLE_NLS */

	mosquitto_lib_init();

	while ((c = getopt(argc, argv, "Vhc:")) != -1)
	{
		switch (c)
		{
			case 'V':
				version();
				break;
				
			case 'h':
				usage(EXIT_SUCCESS);
				break;

			case 'c':
				break;
	
			default:
				usage(EXIT_FAILURE);
				break;
		}
	}

	memset(clientid, 0, 24);
	snprintf(clientid, 23, "%s-%d", prg_name, getpid());
	mosq = mosquitto_new(clientid, 1, NULL);
	if (mosq == NULL)
	{
		fatal("Out of memory.");
	}

	c = mosquitto_connect(mosq, "localhost", 1883, 120);
	if (c != MOSQ_ERR_SUCCESS)
	{
		mosquitto_destroy(mosq);
		fatal(mosquitto_strerror(c));
	}

	mosquitto_loop_forever(mosq, -1, 1);

	mosquitto_destroy(mosq);

	mosquitto_lib_cleanup();

	return (EXIT_SUCCESS);
}
