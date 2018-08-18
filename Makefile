init:
	pip install -r requirements.txt
	pip install -U pytest
	pip install coverage

test:
	cd tests/; py.test --junitxml results.xml test_*.py

coverage:
	cd tests/; for test in test_*.py; do coverage run --parallel-mode --branch ${test}; done
	cd tests/; coverage combine; coverage xml -i

.PHONY: init test coverage