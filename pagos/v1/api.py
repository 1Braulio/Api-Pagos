from pagos.models import PagosV1
from rest_framework import viewsets
from .serializers import PagosSerializer
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .pagination import StandardResultsSetPagination
from rest_framework import viewsets, filters 

# from rest_framework.throttling import Throttling

# class PostThrottling(Throttling):
#     def allow_request(self, request, view):
#         if request.method == 'POST':
#             # Limit the number of POST requests to 10 per minute
#             return self.throttle_success() if self.rate_limit.get_and_update() <= 10 else self.throttle_failure()
#         return True

class PagosViewSetCustom(viewsets.ModelViewSet):
    queryset = PagosV1.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['usuario', 'fecha_pago', 'servicio']
    ordering = ('-id')

    throttle_scope = 'post'


    def get_serializer_class(self):
        return PagosSerializer

    def list(self, request):
        page = self.paginate_queryset(self.queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        if isinstance(request.data, list):
            serializer = PagosSerializer(data=request.data, many = True)
        else:
            serializer = PagosSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        todo = get_object_or_404(self.queryset, pk=pk)
        serializer = PagosSerializer(todo)
        return Response(serializer.data)

    