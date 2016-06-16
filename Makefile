
# Make sure to show deprecation warnings
TEST_FLAGS=-Wall
TEST_CMD=manage.py test --pattern=*_test.py
TEST=python $(TEST_FLAGS) $(TEST_CMD)


#
# Documentation
#
.PHONY: help

help:
	@echo "Testing:"
	@echo "    test >> Run the full test suite"
	@echo "Running"
	@echo "    use manage.py"

#
# Testing
#
.PHONY: test

test:
	$(TEST)

coverage:
	coverage run --source='.' $(TEST_CMD)
