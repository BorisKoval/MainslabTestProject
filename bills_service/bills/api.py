import django_filters
from django_filters import rest_framework as filters

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Bill
from .serializers import BillsSerializer, UploadBillsSerializer


class BillsInfoFilter(django_filters.FilterSet):
    """Фильтрация для счетов"""

    client = django_filters.CharFilter(
        field_name='client__name', lookup_expr='iexact')
    organisation = django_filters.CharFilter(
        field_name='organisation__name', lookup_expr='iexact')

    class Meta:
        model = Bill
        fields = ['client', 'organisation', 'num', 'sum', 'date']


class BillsViewSet(mixins.ListModelMixin, GenericViewSet):
    """Апи для отображения списка счетов."""

    queryset = Bill.objects.all()
    serializer_class = BillsSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BillsInfoFilter


class UploadBills(mixins.CreateModelMixin, GenericViewSet):
    """Апи для загрузки счетов"""

    serializer_class = UploadBillsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            return Response(
                {'error': f'Произошла ошибка при обработке файла: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(status=status.HTTP_201_CREATED)
