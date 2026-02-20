PYTHON = python3

.PHONY: install run-server run-client

install:
	$(PYTHON) -m pip install requests

run-server:
	cd Server && $(PYTHON) main.py

run-client:
	cd Client && $(PYTHON) main.py
