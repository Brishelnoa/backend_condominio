from django.core.management.base import BaseCommand
from authz.models import Usuario, Persona, FamiliarPropietario
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Crea 2 familiares por propietario, sin modificar los existentes.'

    def handle(self, *args, **kwargs):
        faker = Faker()
        parentescos = [p[0] for p in FamiliarPropietario.PARENTESCO_CHOICES]
        propietarios = Usuario.objects.filter(persona__tipo_persona='propietario')
        creados = 0
        self.stdout.write('👨‍👩‍👧‍👦 Poblando familiares de propietarios...')
        for propietario in propietarios:
            familiares_existentes = FamiliarPropietario.objects.filter(propietario=propietario).count()
            faltan = max(0, 2 - familiares_existentes)
            for _ in range(faltan):
                # Crear persona para familiar
                persona_fam = Persona.objects.create(
                    nombre=faker.first_name(),
                    apellido=faker.last_name(),
                    documento_identidad=faker.unique.random_number(digits=8),
                    telefono=faker.phone_number(),
                    email=faker.unique.email(),
                    fecha_nacimiento=faker.date_of_birth(minimum_age=1, maximum_age=90),
                    genero=random.choice(['M', 'F', 'O']),
                    pais=faker.country(),
                    tipo_persona='familiar',
                    direccion=faker.address(),
                    activo=True
                )
                parentesco = random.choice(parentescos)
                FamiliarPropietario.objects.create(
                    propietario=propietario,
                    persona=persona_fam,
                    parentesco=parentesco,
                    parentesco_descripcion='',
                    autorizado_acceso=True,
                    puede_autorizar_visitas=False,
                    observaciones='',
                    activo=True
                )
                creados += 1
                if creados % 25 == 0:
                    self.stdout.write(f'   {creados} familiares creados...')
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total familiares creados: {creados}'))
