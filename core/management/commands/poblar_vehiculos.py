from django.core.management.base import BaseCommand
from core.models.propiedades_residentes import Vehiculo
from authz.models import Persona
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Crea vehículos para personas existentes, omitiendo los ya registrados.'

    def handle(self, *args, **kwargs):
        faker = Faker()
        personas = Persona.objects.all()
        placas_existentes = set(Vehiculo.objects.values_list('placa', flat=True))
        tags_existentes = set(Vehiculo.objects.values_list('tag_numero', flat=True))
        creados = 0
        self.stdout.write('🚗 Poblando vehículos...')
        for persona in personas:
            # Solo un vehículo por persona si no tiene
            if Vehiculo.objects.filter(propietario=persona).exists():
                continue
            placa = None
            tag = None
            # Generar placa y tag únicos
            for _ in range(10):
                placa_tmp = faker.unique.bothify(text='???-####').upper()
                tag_tmp = faker.unique.bothify(text='TAG-#####').upper()
                if placa_tmp not in placas_existentes and tag_tmp not in tags_existentes:
                    placa = placa_tmp
                    tag = tag_tmp
                    break
            if not placa or not tag:
                continue
            Vehiculo.objects.create(
                propietario=persona,
                placa=placa,
                marca=random.choice(['Toyota', 'Nissan', 'Ford', 'Chevrolet', 'Honda', 'Kia', 'Hyundai']),
                modelo=str(random.randint(2010, 2025)),
                color=random.choice(['Rojo', 'Azul', 'Negro', 'Blanco', 'Gris', 'Verde', 'Amarillo']),
                tipo_vehiculo=random.choice(['auto', 'moto', 'bicicleta', 'camion']),
                tag_numero=tag,
                tag_activo=True,
                activo=True
            )
            placas_existentes.add(placa)
            tags_existentes.add(tag)
            creados += 1
            if creados % 25 == 0:
                self.stdout.write(f'   {creados} vehículos creados...')
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total vehículos creados: {creados}'))
