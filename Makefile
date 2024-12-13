.PHONY: help

help:
	@echo "usage: make (patch|minor|major)"

dryrun:
	@bash scripts/dryrun.sh
	
patch:
	@bash scripts/bumpversion.sh patch

minor:
	@bash scripts/bumpversion.sh minor

major:
	@bash scripts/bumpversion.sh major
