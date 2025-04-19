from django.db import models

# Create your models here.

class Loja(models.Model):
    nome = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Rito(models.Model):
    nome = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Grau(models.Model):
    numero = models.IntegerField()
    nome = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.numero}° - {self.nome}"

class Potencia(models.Model):
    nome = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Visita(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.PROTECT, related_name='visitas')
    data = models.DateField()
    rito = models.ForeignKey(Rito, on_delete=models.PROTECT, related_name='visitas')
    grau = models.ForeignKey(Grau, on_delete=models.PROTECT, related_name='visitas')
    potencia = models.ForeignKey(Potencia, on_delete=models.PROTECT, related_name='visitas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'

    def __str__(self):
        return f"Visita à {self.loja.nome} em {self.data}"
