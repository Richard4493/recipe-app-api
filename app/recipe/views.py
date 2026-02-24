from django.shortcuts import render

from recipe.serializers import IngredientSerializer, RecipeSerializer,RecipeDetailSerializer, TagSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
from core.models import Ingredient, Recipe, Tag
# Create your views here.

class RecipeViewSet(viewsets.ModelViewSet):
     """View for manage recipe APIs."""
     serializer_class = RecipeDetailSerializer
     queryset = Recipe.objects.all()
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]

     def get_queryset(self):
         """override queryset default get method for auth users only"""
         return self.queryset.filter(user=self.request.user).order_by('-id')
     
     def get_serializer_class(self):
          """override srializer_class default get method for action specific"""
          if self.action == 'list':
               return RecipeSerializer
          
          return self.serializer_class
     def perform_create(self,serializer): #override default save with user,otherwise create fails as queryset filters recipes by user
                                            #creating a recipe, Django does NOT automatically assign user=self.request.user.
          serializer.save(user = self.request.user)

class TagViewSet(mixins.ListModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet,):
        """Manage tags in the database."""
        serializer_class = TagSerializer
        queryset = Tag.objects.all()
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
             return self.queryset.filter(user=self.request.user).order_by('-name')
        
class IngredientViewSet(mixins.ListModelMixin,mixins.UpdateModelMixin ,mixins.DestroyModelMixin , viewsets.GenericViewSet):
     """Manage Ingredients in the db"""

     serializer_class = IngredientSerializer
     queryset = Ingredient.objects.all()
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]

     def get_queryset(self):
         return self.queryset.filter(user = self.request.user).order_by('-name')
     
        
          

               

     
