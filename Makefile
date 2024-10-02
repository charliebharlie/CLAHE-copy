# Define the run command
algorithm = test_clahe.py

PYTHON_RUN = python

# Define the test command, e.g., pytest for Python
TEST_DIR = tests/
TEST_CMD = pytest -vv

run: 
	clear && echo "Running algorithm..."
	$(PYTHON_RUN) $(algorithm)

test: 
	$(TEST_CMD) $(TEST_DIR)

back:
	flask --app clahe run

front:
	$(NPM_RUN) $(frontend)

beta: 
	$(PYTHON_RUN) compare/CE_beta.py

og: 
	$(PYTHON_RUN) originalAlgo.py


new:
	$(PYTHON_RUN) clahe/test_distance.py

map:
	$(PYTHON_RUN) clahe/test_interactive.py
.PHONY: all test clean
