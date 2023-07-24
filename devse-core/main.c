#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <locale.h>

#include <mosquitto.h>
#include "devse_config.h"

static char *prg_name = "devse-core";

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
		printf("Usage: %s \n", prg_name);
	}

	exit(retval);
}

int
main(int argc, char **argv)
{
	int c;
	char clientid[24];
	struct mosquitto *mosq;

	setlocale(LC_ALL, "");
	bindtextdomain(PACKAGE, LOCALEDIR);
	textdomain(PACKAGE);

	mosquitto_lib_init();

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

	memset(clientid, 0, 24);
	snprintf(clientid, 23, "%s-%d", prg_name, getpid());
	mosq = mosquitto_new(clientid, 1, NULL);

	mosquitto_connect(mosq, "localhost", 1883, 120);

	while (1)
	{
		mosquitto_loop(mosq, -1, 1);
	}
	mosquitto_destroy(mosq);

	mosquitto_lib_cleanup();

	return (EXIT_SUCCESS);
}
