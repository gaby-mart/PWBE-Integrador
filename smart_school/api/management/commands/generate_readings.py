import random
from django.core.management.base import BaseCommand
from api.models import SensorReading, Sensor

class Command(BaseCommand):
    help = 'Gera leituras de sensores ativos no sistema.'

    def handle(self, *args, **options):
        active_sensors = Sensor.objects.filter(sen_is_active=True)

        if not active_sensors.exists():
            self.stdout.write(self.style.WARNING('Nenhum sensor ativo encontrado.'))
            return

        count_created = 0

        for sensor in active_sensors:
            measured_value = round(random.uniform(0, 100), 2)  # Gera um valor aleatório entre 0 e 100
            
            SensorReading.objects.create(
                sr_measured_value=measured_value,
                sr_sen=sensor
            )
            count_created += 1

        self.stdout.write(self.style.SUCCESS(f'Sucesso! {count_created} leituras simuladas foram geradas.'))