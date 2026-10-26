from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ni = models.CharField(max_length=11, verbose_name="Número de Identificação do usuário")
    photo = models.URLField(max_length=500, null=True, blank=True, verbose_name="URL da foto de perfil do usuário")

    class Meta:
        db_table = 'api_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.get_full_name() or 'Sem Nome'})"

class Laboratory(models.Model):
    lab_id = models.AutoField(primary_key=True)
    lab_name = models.CharField(max_length=20, verbose_name="Nome do laboratório")
    lab_block = models.CharField(max_length=1, verbose_name="Bloco do laboratório")
    lab_floor = models.SmallIntegerField(verbose_name="Andar do laboratório")

    class Meta:
        db_table = 'api_laboratory'
        verbose_name = 'Laboratory'
        verbose_name_plural = 'Laboratories'

    def __str__(self):
        return f"{self.lab_name} - Bloco {self.lab_block}"

class MicrocontrollerModel(models.Model):
    mcm_id = models.AutoField(primary_key=True)
    mcm_name = models.CharField(max_length=50, verbose_name="Nome do Microcontrolador")

    class Meta:
        db_table = 'api_micro_controller_model'
        verbose_name = 'Microcontroller Model'
        verbose_name_plural = 'Microcontroller Models'

    def __str__(self):
        return self.mcm_name

class Microcontroller(models.Model):
    mc_id = models.AutoField(primary_key=True)
    mc_mac_address = models.CharField(max_length=17, unique=True, verbose_name="Endereço MAC do microcontrolador")
    mc_latitude = models.DecimalField(max_digits=10, decimal_places=8, verbose_name="Latitude do microcontrolador")
    mc_longitude = models.DecimalField(max_digits=11, decimal_places=8, verbose_name="Longitude de localização do microcontrolador")
    mc_registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de registro")
    mc_is_active = models.BooleanField(default=True, verbose_name="Status do microcontrolador")

    # ForeignKeys
    mc_model = models.ForeignKey(MicrocontrollerModel, on_delete=models.PROTECT, verbose_name="Modelo")
    mc_laboratory = models.ForeignKey(Laboratory, on_delete=models.PROTECT, verbose_name="Laboratório")
    mc_owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Cadastrado por")

    class Meta:
        db_table = 'api_micro_controller'
        verbose_name = 'Microcontroller'
        verbose_name_plural = 'Microcontrollers'

    def __str__(self):
        return f"ESP8266 ({self.mc_mac_address})"

class MeasurementUnit(models.Model):
    mu_id = models.AutoField(primary_key=True)
    mu_name = models.CharField(max_length=45, verbose_name="Nome da unidade de medida")
    mu_symbol = models.CharField(max_length=10, verbose_name="Simbologia da unidade de medida")
    mu_is_active = models.BooleanField(default=True, verbose_name="Status da unidade de medida")

    class Meta:
        db_table = 'api_measurement_unit'
        verbose_name = 'Measurement Unit'
        verbose_name_plural = 'Measurement Units'

    def __str__(self):
        return f"{self.mu_name} ({self.mu_symbol})"

class SensorModel(models.Model):
    class SensorFunctionChoices(models.TextChoices):
        TEMPERATURE = 'TEMPERATURA', 'Temperatura'
        HUMIDITY = 'UMIDADE', 'Umidade'
        LUMINOSITY = 'LUMINOSIDADE', 'Luminosidade'
        PASSAGE_COUNTER = 'CONTADOR', 'Contagem de Passagens'

    sm_id = models.AutoField(primary_key=True)
    sm_name = models.CharField(max_length=50, verbose_name="Nome do sensor")
    sm_function = models.CharField(
        max_length=20, 
        choices=SensorFunctionChoices.choices, 
        verbose_name="Função do sensor"
    )

    class Meta:
        db_table = 'api_sensor_model'
        verbose_name = 'Sensor Model'
        verbose_name_plural = 'Sensor Models'

    def __str__(self):
        return f"{self.sm_name} - {self.get_sm_function_display()}"

class Sensor(models.Model):
    sen_id = models.AutoField(primary_key=True)
    sen_is_active = models.BooleanField(default=True, verbose_name="Status de ativação do sensor")

    # ForeignKeys
    sen_model = models.ForeignKey(SensorModel, on_delete=models.PROTECT, verbose_name="Modelo")
    sen_measurement_unit = models.ForeignKey(MeasurementUnit, on_delete=models.PROTECT, verbose_name="Unidade de Medida")
    sen_connected_to = models.ForeignKey(Microcontroller, on_delete=models.PROTECT, related_name="sensors", verbose_name="Conectado ao Microcontrolador")

    class Meta:
        db_table = "api_sensor"
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"

    def __str__(self):
        return f"Sensor #{self.sen_id} ({self.sen_model.sm_name})"

class SensorReading(models.Model):
    sr_id = models.BigAutoField(primary_key=True)
    sr_measured_value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="O valor medido")
    sr_measured_at = models.DateTimeField(auto_now_add=True, verbose_name="Data e hora da medição")

    # ForeignKeys
    sr_sen = models.ForeignKey(Sensor, on_delete=models.PROTECT, related_name="readings", verbose_name="Sensor Responsável")

    class Meta:
        db_table = "api_sensor_reading"
        verbose_name = "Sensor Reading"
        verbose_name_plural = "Sensor Readings"

    def __str__(self):
        return f"Leitura {self.sr_measured_value} em {self.sr_measured_at}"