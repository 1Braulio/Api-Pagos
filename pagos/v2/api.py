from datetime import datetime, timedelta
from rest_framework.throttling import BaseThrottle, UserRateThrottle
# ThrottleHistory
from pagos.models import Services, ExpiredPayments, PaymentUser
from rest_framework import viewsets, permissions
from .serializers import ServicesSerializer, ExpiredPaymentsSerializer, PaymentUserSerializer
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .pagination import StandardResultsSetPagination
from rest_framework import viewsets, filters 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# class DailyThrottlingClass(BaseThrottle):
#     def __init__(self):
#         self.history = ThrottleHistory()

#     def allow_request(self, request, view):
#         return self.history.check(self.get_ident(request), 1000, 86400)

class DailyThrottlingClass(UserRateThrottle):
	rate = '2000/day'
	scope = 'days'

class ServicesView(APIView):
	
	throttle_classes = [DailyThrottlingClass]
	
	def get_permissions(self):
		if self.request.method == 'GET':
			return [IsAuthenticated()]
		elif self.request.method == 'POST':
			return [IsAdminUser()]
		else:
			return [IsAuthenticated()]


	def get(self, request):
		services = Services.objects.all()
		serializer = ServicesSerializer(services, many=True)
		return Response(serializer.data)


class ExpiredPaymentsView(APIView):
	
	throttle_classes = [DailyThrottlingClass]

	def get_permissions(self):
		if self.request.method == 'GET':
			return [IsAuthenticated()]
		elif self.request.method == 'POST':
			return [IsAdminUser()]
		else:
			return [IsAuthenticated()]


	def get(self, request):
		expired_payments = ExpiredPayments.objects.all()
		serializer = ExpiredPaymentsSerializer(expired_payments, many=True)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
		serializer = ExpiredPaymentsSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
    

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentUserViewSet(viewsets.ModelViewSet):
	queryset = PaymentUser.objects.all()
	pagination_class = StandardResultsSetPagination
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['payment_date', 'expiration_date']
	ordering = ('-id',)

	throttle_scope = 'get'

	def get_serializer_class(self):
		return ExpiredPaymentsSerializer

	def get_permissions(self):
		if self.action in ['list', 'retrieve', 'create']:
			return [IsAuthenticated()]
# elif self.action in ['destroy', 'update', 'partial_update']:
#     return [permissions.IsAdminUser]
		else:
			return [IsAdminUser()]

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


	def update(self, request, pk=None):
		todo = get_object_or_404(self.queryset, pk=pk)
		serializer = TodoSerializer(todo, data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def partial_update(self, request, pk=None):
		todo = get_object_or_404(self.queryset, pk=pk)
		serializer = TodoSerializer(todo, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(status=status.HTTP_400_BAD_REQUEST)

	def destroy(self, request, pk=None):
		todo = get_object_or_404(self.queryset, pk=pk)
		todo.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)