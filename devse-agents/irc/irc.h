#ifndef DEVSE_AGENTS_IRC_H
# define DEVSE_AGENTS_IRC_H 1

/* config.c */
void config_init_default(void);
void config_from_cmd(int argc, char **argv);
int config_load(const char *file);

#endif /* DEVSE_AGENTS_IRC_H */
