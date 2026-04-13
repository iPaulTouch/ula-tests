from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Cliente")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    correo = models.EmailField(verbose_name="Correo Electrónico")

    def __str__(self):
        return self.nombre

class Dispositivo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='dispositivos')
    marca = models.CharField(max_length=50, verbose_name="Marca")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    serie = models.CharField(max_length=100, unique=True, verbose_name="Número de Serie")

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.serie}"

class Ticket(models.Model):
    ESTADOS = [
        ('Ingreso', 'Ingreso'),
        ('Pendiente', 'Pendiente'),
        ('En revisión', 'En revisión'),
        ('En pruebas', 'En pruebas'),
        ('Finalizado', 'Finalizado'),
    ]
    
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='tickets')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Ingreso')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.estado}"