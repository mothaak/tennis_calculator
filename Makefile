.PHONY: test lint type

test:
	pytest

lint:
	flake8 tennis_calculator

type:
	mypy tennis_calculator 