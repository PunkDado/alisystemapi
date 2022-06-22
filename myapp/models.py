from django.db import models

class Usuario(models.Model):
    id = models.AutoField
    nome = models.CharField(max_length=30)
    login = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)
    perfil = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.nome

class Login(models.Model):
    login = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.login