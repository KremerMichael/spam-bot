# Change as needed
python_ver='python3.9'


# Keep this first so 'make' works
# Install Package
install:
	$(python_ver) setup.py install

# Check linting
check:
	$(python_ver) -m pylint spam-bot/*py
	$(python_ver) -m pylint unit_testing/*py

#	$(python_ver) unit_testing/optimisticetherscan_tests.py
# Test Library
test:
	$(python_ver) unit_testing/spam_bot_tests.py

# Clean up after build
clean:
	rm -r build dist spam-bot.egg-info

# Uninstall package
uninstall:
	$(python_ver) -m pip uninstall spam-bot

# List options
list:
	@grep '^[^#[:space:]].*:' Makefile
