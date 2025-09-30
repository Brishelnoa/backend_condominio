from django.core.management.base import BaseCommand
from core.models.propiedades_residentes import Mascota
from authz.models import Persona
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Crea 1 a 2 mascotas por persona, omitiendo las ya registradas.'

    def handle(self, *args, **kwargs):
        faker = Faker()
        personas = Persona.objects.all()
        self.stdout.write(f'🔎 Personas encontradas: {personas.count()}')
        nombres_existentes = set(Mascota.objects.values_list('nombre', flat=True))
        creados = 0
        self.stdout.write('🐶 Poblando mascotas...')
        for persona in personas:
            mascotas_existentes = Mascota.objects.filter(propietario=persona).count()
            faltan = max(0, random.randint(1, 2) - mascotas_existentes)
            for _ in range(faltan):
                nombre = faker.unique.first_name()
                if nombre in nombres_existentes:
                    continue
                Mascota.objects.create(
                    propietario=persona,
                    nombre=nombre,
                    tipo_animal=random.choice(['Perro', 'Gato', 'Ave', 'Pez', 'Conejo', 'Tortuga']),
                    raza=faker.word(),
                    edad=random.randint(1, 15),
                    descripcion=faker.sentence(),
                    vacunas_vigentes=random.choice([True, False]),
                    activo=True
                )
                nombres_existentes.add(nombre)
                creados += 1
                if creados % 25 == 0:
                    self.stdout.write(f'   {creados} mascotas creadas...')
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total mascotas creadas: {creados}'))
