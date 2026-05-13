from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.products.models import Shop


class ShopDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):

        # -----------------------------------
        # Get user shop safely
        # -----------------------------------
        try:
            shop = Shop.objects.get(owner=request.user)
        except Shop.DoesNotExist:
            return Response(
                {"error": "Shop not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # -----------------------------------
        # Delete shop
        # -----------------------------------
        shop.delete()

        return Response(
            {"message": "Shop deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )