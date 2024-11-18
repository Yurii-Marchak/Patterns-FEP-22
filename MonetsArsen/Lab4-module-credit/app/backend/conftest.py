import asyncio  # Import the asyncio module for asynchronous programming and event loop management
import pytest  # Import pytest for testing and test fixture management

# Specify pytest plugins to use for the test suite; in this case, pytest_asyncio is used for async test support
pytest_plugins = ["pytest_asyncio"]

@pytest.fixture(scope="function")
def event_loop():
    """
    Fixture to provide a new event loop for each test function.

    This fixture creates a new event loop for each test and ensures the event loop
    is closed after the test function has run. It is useful for asynchronous testing
    when using pytest with asyncio-based code.

    The 'scope="function"' means a new event loop is created for each test function.
    """
    loop = asyncio.new_event_loop()  # Create a new event loop
    yield loop  # Yield the event loop to be used in the test
    loop.close()  # Close the event loop after the test completes
