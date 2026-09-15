PYTHON		:=	python3
VENV_DIR	:=	.venv
VENV_PYTHON	:=	$(VENV_DIR)/bin/python3


MYPY_FLAGS	:=	--warn-return-any --warn-unused-ignores \
				--ignore-missing-imports --disallow-untyped-defs \
				--check-untyped-defs

all: install run

$(VENV_DIR)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_PYTHON) -m pip install -r requirements.txt
	touch $(VENV_DIR)/bin/activate

install: $(VENV_DIR)/bin/activate

build: install
	@$(VENV_PYTHON) -m build

test: install
	@$(VENV_PYTHON) -m pytest

run: install
	@$(VENV_PYTHON) a_maze_ing.py config.txt

debug: install
	@$(VENV_PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__/
	rm -rf utils/__pycache__/
	rm -rf mazegen/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

lint: install
	@$(VENV_PYTHON) -m flake8 --exclude=$(VENV_DIR) .
	@$(VENV_PYTHON) -m mypy $(MYPY_FLAGS) --exclude $(VENV_DIR) .

lint-strict: install
	@$(VENV_PYTHON) -m flake8 --exclude=$(VENV_DIR) .
	@$(VENV_PYTHON) -m mypy --strict --exclude $(VENV_DIR) .

.PHONY: all install build test run debug clean lint lint-strict
