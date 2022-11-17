from django.db import models


class Service(models.Model):
    name = models.CharField('Наименование', max_length=250) #todo  ограничения длины заданы ориентировочные


class Client(models.Model):
    name = models.CharField('Наименование', max_length=250)


class Organisation(models.Model):
    name = models.CharField('Наименование', max_length=250)


class Bill(models.Model):
    client = models.ForeignKey(
        Client, verbose_name='Наименование клиента',
        on_delete=models.CASCADE)
    organisation = models.ForeignKey(
        Organisation, verbose_name='Наименование организации',
        on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, verbose_name='Услуги')
    num = models.IntegerField('Номер')
    sum = models.FloatField('Сумма')
    date = models.DateField('Дата')

    class Meta:
        unique_together = ['client', 'organisation', 'num']
