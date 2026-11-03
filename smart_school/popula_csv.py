import os
import sys
import csv
import random
from datetime import timedelta
from decimal import Decimal

import django
from django.utils import timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_school.settings')
django.setup()

from api.models import (
    User, Laboratory, MicrocontrollerModel, Microcontroller,
    MeasurementUnit, SensorModel, Sensor, SensorReading,
)

DATA_DIR = os.path.join(BASE_DIR, 'data')

UNITS = {
    'TEMPERATURA':  ('Graus Celsius', '°C'),
    'UMIDADE':      ('Porcentagem', '%'),
    'LUMINOSIDADE': ('Lux', 'lx'),
    'QUALIDADE_AR': ('Partes por milhão', 'PPM'),
    'CONTADOR':     ('Passagens', 'un'),
}

RANGES = {
    'TEMPERATURA':  (18.0, 35.0),
    'UMIDADE':      (30.0, 80.0),
    'LUMINOSIDADE': (0.0, 1000.0),
    'QUALIDADE_AR': (300.0, 1000.0),
    'CONTADOR':     (0, 50),
}


def read_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, mode='r', encoding='utf-8-sig', newline='') as f:
        yield from csv.DictReader(f)


def get_owner():
    owner = User.objects.filter(is_superuser=True).first()
    if owner:
        return owner
    owner, created = User.objects.get_or_create(
        username='seed_user',
        defaults={'ni': '00000000000', 'is_staff': True},
    )
    if created:
        owner.set_unusable_password()
        owner.save()
    return owner


def import_data():
    print("Starting CSV data import...")

    # Unidades de medida
    units = {}
    for func, (name, symbol) in UNITS.items():
        units[func], _ = MeasurementUnit.objects.get_or_create(
            mu_name=name, mu_symbol=symbol, defaults={'mu_is_active': True}
        )
    print("-> Unidades de medida importadas com sucesso.")

    # Modelos
    for row in read_csv('sensormodel.csv'):
        SensorModel.objects.update_or_create(
            sm_id=int(row['sm_id']),
            defaults={
                'sm_name': row['sm_name'],
                'sm_function': row['sm_function'],
            },
        )
    print("-> Modelos de sensores importados com sucesso.")

    owner = get_owner()
    for row in read_csv('microcontroller.csv'):
        lab, _ = Laboratory.objects.get_or_create(
            lab_name=row['lab_name'],
            lab_block=row['lab_block'],
            defaults={'lab_floor': int(row['lab_floor'])},
        )
        mc_model, _ = MicrocontrollerModel.objects.get_or_create(
            mcm_name=row['mc_model']
        )
        Microcontroller.objects.update_or_create(
            mc_id=int(row['mc_id']),
            defaults={
                'mc_mac_address': row['mc_mac_address'],
                'mc_latitude': Decimal(row['mc_latitude']),
                'mc_longitude': Decimal(row['mc_longitude']),
                'mc_is_active': row['mc_is_active'] == '1',
                'mc_model': mc_model,
                'mc_laboratory': lab,
                'mc_owner': owner,
            },
        )
    print("-> Microcontroladores importados com sucesso.")

    # Sensores
    for row in read_csv('sensor.csv'):
        model_obj = SensorModel.objects.get(pk=int(row['sen_model_id']))
        mc_obj = Microcontroller.objects.get(pk=int(row['sen_mc_id']))
        Sensor.objects.update_or_create(
            sen_id=int(row['sen_id']),
            defaults={
                'sen_model': model_obj,
                'sen_connected_to': mc_obj,
                'sen_measurement_unit': units[model_obj.sm_function],
                'sen_is_active': row['sen_is_active'] == '1',
            },
        )
    print("-> Sensores importados com sucesso.")

    # Leituras simuladas
    active_sensors = list(
        Sensor.objects.filter(sen_is_active=True).select_related('sen_model')
    )
    if active_sensors:
        SensorReading.objects.all().delete()
        now = timezone.now()
        for _ in range(100):
            sensor = random.choice(active_sensors)
            low, high = RANGES[sensor.sen_model.sm_function]
            value = (random.randint(low, high)
                     if isinstance(low, int)
                     else round(random.uniform(low, high), 2))

            reading = SensorReading.objects.create(
                sr_sen=sensor,
                sr_measured_value=Decimal(str(value)),
            )
            SensorReading.objects.filter(pk=reading.pk).update(
                sr_measured_at=now - timedelta(minutes=random.randint(1, 1440))
            )
        print("-> 100 leituras simuladas geradas com sucesso para sensores ativos.")

    print("População completada!")


if __name__ == '__main__':
    import_data()