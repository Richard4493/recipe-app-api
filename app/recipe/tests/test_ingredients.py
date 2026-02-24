"""
Tests for the ingredients API.
"""

from django.contrib.auth import get_user_model
from recipe.serializers import IngredientSerializer
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient
from django.urls import reverse


from django.test import TestCase

INGREDIENT_URL = reverse("recipe:ingredient-list")

def detail_url(ingredient_id):
     
     return reverse("recipe:ingredient-detail",args=[ingredient_id])


def create_user(email='user@example.com', password='testpass123'):

    return get_user_model().objects.create_user(email = email, password = password)

class PublicIngredientsApiTests(TestCase):

    def setUp(self):
            self.client = APIClient()

    def test_authentication_required_for_ingredient_list(self):
            """Test auth is required for retrieving ingredients."""
            res = self.client.get(INGREDIENT_URL)

            self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientApiTests(TestCase):
      
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
         """To test ingredient list API is working"""
         Ingredient.objects.create(user = self.user,name="Rice")
         Ingredient.objects.create(user = self.user,name="Salt")

         res = self.client.get(INGREDIENT_URL)
         ingredients = Ingredient.objects.all().order_by("-name")
         serializer = IngredientSerializer(ingredients,many = True)

         self.assertEqual(res.status_code,status.HTTP_200_OK)
         self.assertEqual(res.data,serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user."""

        user2 = create_user(email = "unauth@mail.com",password="test123")
        Ingredient.objects.create(user = user2,name = "user2ing")
        ingredientTrue = Ingredient.objects.create(user = self.user,name = "authusering")

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],ingredientTrue.name)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['id'], ingredientTrue.id)

    def test_update_ingredient(self):
         """Test for ingredient test update"""

         ingredient = Ingredient.objects.create(user = self.user, name = "Sugar")

         payload = {"name" : "Refined Sugar"}
         url = detail_url(ingredient.id)
         res = self.client.patch(url,payload)
         self.assertEqual(res.status_code,status.HTTP_200_OK)
         ingredient.refresh_from_db()
         self.assertEqual(ingredient.name,payload['name'])

    def test_delete_ingredient(self):
        """Test deleting an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='Lettuce')

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())





    

    

    

