from django.shortcuts import render

from recipe.serializers import IngredientSerializer, RecipeImageSerializer, RecipeSerializer,RecipeDetailSerializer, TagSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins, status

from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import Ingredient, Recipe, Tag
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from symbol import parameters
# Create your views here.


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            ),
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
     """View for manage recipe APIs."""
     serializer_class = RecipeDetailSerializer
     queryset = Recipe.objects.all()
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]

     def _convert_params_to_int(self,params):

          return [int(str_id) for str_id in params.split(',')]

     def get_queryset(self):
         """override queryset default get method for auth users only"""
         #return self.queryset.filter(user=self.request.user).order_by('-id')
         tags = self.request.query_params.get('tags')
         ingredients = self.request.query_params.get('ingredients')
         queryset = self.queryset
         if tags:
              tag_ids = self._convert_params_to_int(tags)
              queryset = queryset.filter(tags__id__in = tag_ids)
         if ingredients:
              ingredient_ids = self._convert_params_to_int(ingredients)
              queryset = self.queryset.filter(ingredients__id__in=ingredient_ids)
         
         return queryset.filter(user = self.request.user).order_by('-id').distinct()
     
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

@extend_schema_view(
     list = extend_schema(
          parameters = [
               OpenApiParameter(
                    'assigned_only',
                    OpenApiTypes.INT, enum=[0,1],
                    description = "Items assigned to recipes only"
               )
          ]
     )
)
class BaseRecipeAttrViewSet(mixins.ListModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
     """A Baseclass for tags and ingredients views so that redundant code can be avoided"""

     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]

     def get_queryset(self):
             #return self.queryset.filter(user=self.request.user).order_by('-name')
          queryset = self.queryset
          assigned_only = bool( int(self.request.query_params.get('assigned_only',0)))
          if assigned_only:
               queryset = queryset.filter(recipe__isnull = False)
          
          return queryset.filter(user = self.request.user).order_by('-name').distinct()
     
     def perform_create(self,serializer): #override default save with user,otherwise create fails as queryset filters recipes by user
                                            #creating a recipe, Django does NOT automatically assign user=self.request.user.
          serializer.save(user = self.request.user)



class TagViewSet(BaseRecipeAttrViewSet):
        """Manage tags in the database."""
        serializer_class = TagSerializer
        queryset = Tag.objects.all()

class IngredientViewSet(BaseRecipeAttrViewSet):
     """Manage Ingredients in the db"""

     serializer_class = IngredientSerializer
     queryset = Ingredient.objects.all()
     
        
          

               

     
