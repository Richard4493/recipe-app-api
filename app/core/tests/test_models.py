"""
Tests for models.
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_is_normalized(self):

        sample_response = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, normalized_email in sample_response:
            user = get_user_model().objects.create_user(email, 'password')
            self.assertEqual(user.email, normalized_email)


    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    
    def test_create_superuser(self):

        user = get_user_model().objects.create_superuser(
            'sample@mail.com',
            'samplepassword'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_create_recipe(self):

        user = get_user_model().objects.create_user(
            'testsample@mail.com',
            'testpassword'
        )

        recipe = models.Recipe.objects.create(
            user = user,
            title = "Chicken curry",
            time_minutes = 5,
            price = Decimal('5.50'),
            description = "Chicken curry sample recipe"
        )

        self.assertEqual(str(recipe),recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_tag_on_update(self):
        """Test creating a tag on recipe update is successful."""
