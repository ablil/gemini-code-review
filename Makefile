.PHONY: help

help:
	@echo "usage: make (patch|minor|major)"

patch:
	@bash bumpversion.sh patch

minor:
	@bash bumpversion.sh minor

major:
	@bash bumpversion.sh major
