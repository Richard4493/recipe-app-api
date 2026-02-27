from django.shortcuts import render

from recipe.serializers import IngredientSerializer, RecipeImageSerializer, RecipeSerializer,RecipeDetailSerializer, TagSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins, status

from rest_framework.decorators import action
from rest_framework.response import Response
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
          elif self.action == 'upload_image':
                return RecipeImageSerializer
          
          return self.serializer_class
     def perform_create(self,serializer): #override default save with user,otherwise create fails as queryset filters recipes by user
                                            #creating a recipe, Django does NOT automatically assign user=self.request.user.
          serializer.save(user = self.request.user)

     @action(methods=['POST'], detail=True, url_path='upload-image')  #
     def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BaseRecipeAttrViewSet(mixins.ListModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
     """A Baseclass for tags and ingredients views so that redundant code can be avoided"""

     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]

     def get_queryset(self):
             return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
        """Manage tags in the database."""
        serializer_class = TagSerializer
        queryset = Tag.objects.all()

class IngredientViewSet(BaseRecipeAttrViewSet):
     """Manage Ingredients in the db"""

     serializer_class = IngredientSerializer
     queryset = Ingredient.objects.all()
     
        
          

               

     
