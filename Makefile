test:
	python3 -mpytest tests/

lint:
	@echo "    Linting hrds codebase"
	@python3 -m flake8 hrds
	@echo "    Linting hrds test suite"
	@python3 -m flake8 hrds
