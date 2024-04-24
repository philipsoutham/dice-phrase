PYTHON := python3
PIP := pip3
TARGET_DIR := dice_phrase
ZIPAPP_NAME := dice-phrase
ENTRY_POINT := dice_phrase.main:app

.PHONY: all install_deps build_zipapp clean

all: install_deps build_zipapp

install_deps:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade --requirement requirements.txt --target $(TARGET_DIR)

build_zipapp:
	@echo "Building the zipapp..."
	$(PYTHON) -m zipapp $(TARGET_DIR) -p "/usr/bin/env python3" -m $(ENTRY_POINT) -c -o $(ZIPAPP_NAME)

clean:
	@echo "Cleaning up..."
	rm -f $(ZIPAPP_NAME)
