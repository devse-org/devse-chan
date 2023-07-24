#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <locale.h>

#include <mosquitto.h>
#include "devse_config.h"

static char *prg_name = "devse-irc-agent";
static char *opt_irc_nick = "devse-chan";
static char *opt_irc_user = "devsechan";
static char *opt_irc_server = NULL;
static char *opt_server_password = NULL;
static char *opt_irc_login_cmd = NULL;
static short opt_irc_port = 6667;
static char *opt_mqtt_user = NULL;
static char *opt_mqtt_password = NULL;
static char *opt_mqtt_host = "localhost";
static short opt_mqtt_port = 1881;
static char *opt_config_path = NULL;

void
version(void)
{
	printf(PACKAGE_NAME " v" PACKAGE_VERSION "\n");
	printf("Copyright (C) 2023 d0p1\n");
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
		fprintf(stderr, "Try '%s -h' for more information.\n", prg_name);
	}
	else
	{
		printf("Usage: %s [OPTIONS...]\n", prg_name);
	}

	exit(retval);
}

int
main(int argc, char **argv)
{
	int c;

	setlocale(LC_ALL, "");
	bindtextdomain(PACKAGE, LOCALEDIR);
	textdomain(PACKAGE);

	while ((c = getopt(argc, argv, "Vh")) != -1)
	{
		switch (c)
		{
			case 'V':
				version();
				break;

			case 'h':
				usage(EXIT_SUCCESS);
				break;

			default:	
				usage(EXIT_FAILURE);
				break;
		}
	}

	return (EXIT_SUCCESS);
}
