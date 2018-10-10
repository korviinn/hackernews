#!/bin/make -f

.PHONY: help info venv rm test docs man lint i$(PYTHON) clean run build deploy

# === CONSTANTS ===

PYTHON=python3.7
PIPENV=PIPENV_COLORBLIND=1 PIPENV_YES=1 PIPENV_NOSPIN=1 PIPENV_HIDE_EMOJIS=1 $(PYTHON) -m pipenv

# === READING PROJECT METADATA ===

NAME=$(shell $(PYTHON) setup.py --name)
VERSION=$(shell sed 's/__version__ *= *'"'"'\(.*\)'"'"'/\1/;t;d' $(NAME)/__init__.py)
COPYRIGHT=$(shell sed 's/__copyright__ *= *'"'"'\(.*\)'"'"'/\1/;t;d' $(NAME)/__init__.py)
AUTHOR=$(shell sed 's/__author__ *= *'"'"'\(.*\)'"'"'/\1/;t;d' $(NAME)/__init__.py)
DESCRIPTION=$(shell sed 's/__long_description__ *= *'"'"'\(.*\)'"'"'/\1/;t;d' $(NAME)/__init__.py)
MAINTAINER=$(shell sed 's/__maintainer__ *= *'"'"'\(.*\)'"'"'/\1/;t;d' $(NAME)/__init__.py)
MAINTAINER_EMAIL=$(shell sed 's/__maintainer_email__ *= *'"'"'\(.*\)'"'"'/\1/;t;d' $(NAME)/__init__.py)


# === STATEFUL PHONY TARGETS ===

VENV_CREATED=$(shell if $(PIPENV) --venv 2>&1 > /dev/null; then echo 1; else echo 0; fi)

# === HELP AND METADATA ACCESS ===

help:
	@echo ""
	@cat README.md
	@echo ""

info:
	@cat README.md | head -n 6
	@echo "  *** Project $(NAME) v$(VERSION)"
	@echo "  *** $(AUTHOR)"
	@echo "  *** (C) $(COPYRIGHT)"
	@echo ""
	@echo "Maintainer: $(MAINTAINER) <$(MAINTAINER_EMAIL)>"
	@echo "Description: $(DESCRIPTION)"
ifeq ($(VENV_CREATED), 1)
	@echo "Using interpreter: $(shell $(PIPENV) run $(PYTHON) --version 2>&1)"
endif


# === VIRTUALENV MANAGEMENT ===

venv:
ifneq ($(VENV_CREATED), 1)
	@$(PIPENV) install -d
	@$(PIPENV) run $(PYTHON) setup.py develop
else
	@true
endif

rm:
ifeq ($(VENV_CREATED), 1)
	@$(PIPENV) --rm
else
	@true
endif


# === DEV PROCESSES AUTOMATION ===

test: venv
	@cd tests && $(PIPENV) run pytest --cov-report html:coverage --cov=$(NAME) -v .

docs: venv
	@$(PIPENV) run $(PYTHON) -m sphinx -M html docs docs/_build

man: venv
	@$(PIPENV) run $(PYTHON) -m sphinx -M man docs docs/_build
	@man ./docs/_build/man/$(NAME).1

lint: venv
	@$(PIPENV) run autopep8 --recursive --in-place --aggressive $(NAME)
	@$(PIPENV) run pylint --disable=C0111 $(NAME) || true

clean: build_clean rm
	@$(PYTHON) setup.py clean
	@rm -rf tests/coverage
	@rm -rf .cache
	@rm -rf Pipfile.lock
	@rm -rf $(NAME).egg-info
	@rm -rf docs/_build

run: venv
	@$(PIPENV) run $(PYTHON) -m $(NAME)


# === VERSION CONTROL AUTOMATION ===

version:
	@echo `$(PYTHON) setup.py --version`

bump_major:
	@sed -i 's/\(__version__ *= *\)'"'"'\([0-9]\)\.\([0-9]\)\.\([0-9]\)'"'"'/echo "\1'"'"'$$\((\2+1)).0.0'"'"'"/ge' $(NAME)/__init__.py
	@echo "New version: `$(PYTHON) setup.py --version`"

bump_minor:
	@sed -i 's/\(__version__ *= *\)'"'"'\([0-9]\)\.\([0-9]\)\.\([0-9]\)'"'"'/echo "\1'"'"'\2.$$\((\3+1)).0'"'"'"/ge' $(NAME)/__init__.py
	@echo "New version: `$(PYTHON) setup.py --version`"

bump_patchlevel:
	@sed -i 's/\(__version__ *= *\)'"'"'\([0-9]\)\.\([0-9]\)\.\([0-9]\)'"'"'/echo "\1'"'"'\2.\3.$$\((\4+1))'"'"'"/ge' $(NAME)/__init__.py
	@echo "New version: `$(PYTHON) setup.py --version`"

