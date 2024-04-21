#include <libgen.h>
#include <stddef.h>
#include <stdlib.h>
#include <libconfig.h>
#include <stdio.h>
#include <unistd.h>
#include "devse_config.h"
#include "gettext.h"
#include "irc.h"
#include "logger.h"

#define _(x) gettext(x)

static const char *prg_name = "devse-irc-agent";
static config_t config;

static void
config_cleanup(void)
{
	config_destroy(&config);
}

void
config_init_default(void)
{
	config_setting_t *setting_root, *setting_master, *setting_irc, *setting;

	config_init(&config);
	atexit(config_cleanup);

	setting_root = config_root_setting(&config);

	setting_master = config_setting_add(setting_root, "master", CONFIG_TYPE_GROUP);

	setting = config_setting_add(setting_master, "host", CONFIG_TYPE_STRING);
	config_setting_set_string(setting, "localhost");

	setting = config_setting_add(setting_master, "port", CONFIG_TYPE_INT);
	config_setting_set_int(setting, 1881);

	setting_irc = config_setting_add(setting_root, "irc", CONFIG_TYPE_GROUP);

	setting = config_setting_add(setting_irc, "port", CONFIG_TYPE_INT);
	config_setting_set_int(setting, 6667);

	setting = config_setting_add(setting_irc, "ssl", CONFIG_TYPE_BOOL);
	config_setting_set_bool(setting, 0);

	setting = config_setting_add(setting_irc, "nick", CONFIG_TYPE_STRING);
	config_setting_set_string(setting_irc, "devse-chan");

	setting = config_setting_add(setting_irc, "user", CONFIG_TYPE_STRING);
	config_setting_set_string(setting, "devse");

	config_setting_add(setting_irc, "relays", CONFIG_TYPE_ARRAY);

}

static void
version(void)
{
	printf(PACKAGE_NAME " v" PACKAGE_VERSION "\n");
	printf("Copyright (C) 2024 d0p1\n");
	printf("License BSD-3-Clause: <https://directory.fsf.org/wiki/License:BSD-3-Clause>\n");
	printf("This is free software: you are free to change and redistribute it.\n");
	printf("There is NO WARRANTY, to the extent permitted by law.\n");

	exit(EXIT_SUCCESS);
}

static void
usage(int retval)
{
	if (retval != EXIT_SUCCESS)
	{
		fprintf(stderr, _("Try '%s -h' for more information.\n"), prg_name);
	}
	else
	{
		printf(_("Usage: %s [-Vh] [-c CONFIG]\n"), prg_name);
	}

	exit(retval);
}

void
config_from_cmd(int argc, char **argv)
{
	int c;

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
				config_load(optarg);
				break;

			default:	
				usage(EXIT_FAILURE);
				break;
		}
	}
}

int
config_load(const char *file)
{
	if (config_read_file(&config, file) != CONFIG_TRUE)
	{
		LOG_ERROR("%s:%d: %s", config_error_file(&config), 
			config_error_line(&config),
			config_error_text(&config));
		return (-1);
	}

	LOG_INFO("%s: loaded", file);
	return (0);
}
