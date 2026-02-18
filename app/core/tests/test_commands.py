"""
Test custom Django management commands.
This file contains unit tests for the wait_for_db management command.
"""

# patch is used to mock functions during testing
from unittest.mock import patch

# Psycopg2 OperationalError occurs when PostgreSQL connection fails
# (aliased here for clarity if needed in other tests)
from psycopg2 import OperationalError as Psycopg2OpError

# call_command allows us to run Django management commands in tests
from django.core.management import call_command

# Django's OperationalError (database connection related error)
from django.db.utils import OperationalError

# SimpleTestCase is used when no actual database interaction is needed
from django.test import SimpleTestCase


# Patch the "check" method of the wait_for_db Command class
# This replaces the real database check with a mock (fake function)
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test suite for custom management commands."""

    def test_wait_for_db_ready(self, patched_check):
        """
        Test that the command completes successfully when the database is ready.
        
        patched_check is the mocked version of Command.check method.
        """

        # Simulate database being ready by making check() return True immediately
        patched_check.return_value = True

        # Call the custom management command: python manage.py wait_for_db
        # This executes the handle() method of the Command class
        call_command('wait_for_db')

        # Verify that the check() method was called exactly once
        # and with the correct argument (default database)
        patched_check.assert_called_once_with(databases=['default'])
    
    # Patch the time.sleep function so it doesn't actually delay the test execution
    # This makes the test run instantly instead of waiting in real time
    @patch('time.sleep')

    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test waiting for database when OperationalError occurs.

        This test simulates database connection failures multiple times,
        and verifies that the wait_for_db command retries until the database is ready.
        """

        # Simulate database connection behavior using side_effect:
        #
        # First 2 calls → raise Psycopg2OpError (PostgreSQL connection error)
        # Next 3 calls → raise Django OperationalError (database not ready)
        # Final call → return True (database is ready)
        #
        # This simulates database becoming ready after multiple retries.
        patched_check.side_effect = [Psycopg2OpError] * 2 + [OperationalError] * 3 + [True]   #list multiplication and concatination

        # Run the custom management command: python manage.py wait_for_db
        #
        # The command will:
        # - Try connecting to database
        # - Catch errors
        # - Retry after sleep()
        # - Stop when connection succeeds
        call_command('wait_for_db')

        # Verify that the check() method was called exactly 6 times
        #
        # 2 Psycopg2OpError attempts
        # 3 OperationalError attempts
        # 1 successful attempt
        #
        # Total = 6 calls
        self.assertEqual(patched_check.call_count, 6)

        # Verify that the last call to check() was made with correct argument
        # This ensures the command is checking the correct database ("default")
        patched_check.assert_called_with(databases=['default'])
