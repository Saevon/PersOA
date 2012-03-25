
# Make sure to show deprecation warnings
TEST_FLAGS=-Wall
TEST=python $(TEST_FLAGS) manage.py test


#
# Documentation
#
.PHONY: help

help:
	@echo "Testing:"
	@echo "    test >> Run the full test suite"

#
# Testing
#
.PHONY: test

test:
	$(TEST)
