# PlayWright_Python_BookingWebAPP

Web automation of a Booking web application using **Playwright**, **Python**, and **Pytest**.

## About
This project demonstrates automation of a Booking web application. It covers UI automation using Playwright with Python and organizes tests using Pytest. It includes reusable page objects, utility functions, and test data management.

## Features
- End-to-end automation of booking flows
- Page Object Model (POM) design for maintainability
- Pytest framework for test management
- Support for running tests in multiple browsers
- Utility functions for common operations

## Project Structure

PlayWright_Python_BookingWebAPP/


&rarr; data/ # Test data files

&rarr; pageobjects/ # Page Object classes

&rarr; tests/ # Test scripts

&rarr; utils/ # Helper functions

&rarr; conftest.py # Pytest fixtures

&rarr; pytest.ini # Pytest configuration

&rarr; README.md # Project documentation


## Prerequisites
- Python 3.8+
- Playwright
- Pytest

### Use below commands to run files
- pytest : To run all the tests
- pytest tests/test_example.py : To run specific tests