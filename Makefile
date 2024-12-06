LINTER=pylint
SOURCE_DIRS=.

.PHONY: lint
lint:
	@echo "Running linter on all files in the repository..."
	$(LINTER) $(SOURCE_DIRS)

.PHONY: format
format:
	@echo "Formatting code using black..."
	black $(SOURCE_DIRS)

.PHONY: clean
clean:
	@echo "Cleaning temporary or unnecessary files..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
