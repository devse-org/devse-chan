EXTRA_DIST  = Cargo.toml \
				src/main.rs

all-local:
	(cd $(srcdir); CARGO_TARGET_DIR=$(abs_builddir)/target cargo build --@CARGO_TARGET@)

clean-local:
	-(cd $(srcdir); CARGO_TARGET_DIR=$(abs_builddir)/target cargo clean)

install-exec-local:
	$(MKDIR_P) $(DESTDIR)$(bindir)
	$(INSTALL) -c -m 755 target/@CARGO_TARGET@/devse-agent-discord$(EXEEXT) $(DESTDIR)$(bindir)