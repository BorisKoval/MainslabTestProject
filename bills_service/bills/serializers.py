import csv
from datetime import datetime
from io import StringIO
from itertools import islice

from rest_framework import serializers

from .models import Bill
from .models import Client
from .models import Organisation
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    """Сериалайзер для услуг."""

    class Meta:
        model = Service
        fields = ['name']


class BillsSerializer(serializers.ModelSerializer):
    """Сериалайзер для счетов."""
    client_name = serializers.CharField(source='client.name')
    organisation_name = serializers.CharField(source='organisation.name')
    services = ServiceSerializer(many=True)

    class Meta:
        model = Bill
        fields = [
            'client_name', 'organisation_name', 'num', 'sum', 'date', 'services'
        ]


class UploadBillsSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def create(self, validated_data):
        bill = Bill()

        csv_string = validated_data['csv_file'].file.read().decode()
        io_string = StringIO(csv_string)
        reader = csv.reader(io_string, delimiter=',')
        for row_data in islice(reader, 1, None):

            # Проверяем наличие client_name и client_org
            try:
                client_name = row_data[0]
                client_org = row_data[1]
            except IndexError:
                continue

            # Проверяем валидность номера, суммы и даты
            try:
                num = int(row_data[2])
                bill_sum = float(row_data[3].replace(',', '.'))
                date = datetime.strptime(row_data[4], '%d.%m.%Y')
            except (TypeError, ValueError):
                continue

            service_names = row_data[5].strip().replace('-', '').split(';')

            client, _ = Client.objects.get_or_create(name=client_name)
            organisation, _ = Organisation.objects.get_or_create(
                name=client_org)

            services = []
            for service_name in service_names:
                service, _ = Service.objects.get_or_create(
                    name=service_name)
                services.append(service)

            # Проверяем валидность услуг
            if not services:
                continue

            bill, _ = Bill.objects.get_or_create(
                client=client,
                organisation=organisation,
                date=date,
                num=num,
                sum=bill_sum,
            )
            for service in services:
                bill.services.add(service)
            bill.save()

        return bill
