.PHONY: help

ROOT_DIR = $(shell git rev-parse --show-toplevel)
SCRIPTS_DIR = "$(ROOT_DIR)/scripts"

help:
	@echo "usage: make (patch|minor|major)"

dryrun:
	@bash $(SCRIPTS_DIR)/dryrun.sh
	
patch:
	@bash $(SCRIPTS_DIR)/bumpversion.sh patch

minor:
	@bash $(SCRIPTS_DIR)/bumpversion.sh minor

major:
	@bash $(SCRIPTS_DIR)/bumpversion.sh major
