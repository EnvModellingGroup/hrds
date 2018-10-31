test:
	python -mpytest tests/

lint:
	@echo "    Linting hrds codebase"
	@python -m flake8 hrds
	@echo "    Linting hrds test suite"
	@python -m flake8 hrds
