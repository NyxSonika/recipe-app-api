"""
Views for recpie APIs
"""

from rest_framework import viewsets
# , mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.models import Recipe
# Tag, Ingredient,
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """"View for manage recipe APIs."""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def _params_to_ints(self, qs):
    #     """Convert a list of string IDs to a list of integers"""
    #     return [int(str_id) for str_id in qs.split(',')]
    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        # elif self.action == 'upload_image':
        #     return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)