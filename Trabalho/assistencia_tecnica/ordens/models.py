from django.db import models

class Computador(models.Model):
    numero_serie = models.CharField(max_length=50, unique=True)
    modelo = models.CharField(max_length=100)
    ano_fabricacao = models.PositiveIntegerField()
    tempo_garantia = models.CharField(max_length=50)  # Exemplo: "12 meses"
    data_vigencia_garantia = models.DateField()

    def __str__(self):
        return f"{self.modelo} - {self.numero_serie}"

