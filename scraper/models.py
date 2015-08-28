from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models


# Create your models here.

class Categoria(models.Model):
    codice = models.CharField(max_length=5, validators=[RegexValidator(r'^\n\n\n\n\n$')], unique=True)
    nome = models.CharField(max_length=128)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.codice, self.nome,)
