.PHONY: install run clean

# Create virtual environment and install dependencies
install:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "Installation complete."

# Run the script manually
run:
	./venv/bin/python3 -m src.ha_ingest

# Remove venv and logs
clean:
	rm -rf venv logs/*