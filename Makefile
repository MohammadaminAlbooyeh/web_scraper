PY=python3
VENV=.venv

.PHONY: venv install test build run shell

venv:
	$(PY) -m venv $(VENV)

install: venv
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

test: install
	$(VENV)/bin/pytest -q

build:
	docker build -t web_scraper:latest .

run: build
	docker run --rm -e SCRAPER_USER_AGENT="$(SCRAPER_USER_AGENT)" -e SCRAPER_PROXY="$(SCRAPER_PROXY)" web_scraper:latest

shell:
	$(VENV)/bin/python
