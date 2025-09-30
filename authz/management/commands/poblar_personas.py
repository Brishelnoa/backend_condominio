from django.core.management.base import BaseCommand
from authz.models import Persona
from faker import Faker
from datetime import datetime
import random

class Command(BaseCommand):
    help = 'Pobla la tabla Persona con datos aleatorios, sin sobrescribir los existentes.'

    def handle(self, *args, **kwargs):
        faker = Faker()
        total_personas = 200
        existentes = set(Persona.objects.values_list('documento_identidad', flat=True))
        creadas = 0
        intentos = 0
        max_intentos = 1000
        self.stdout.write('👤 Poblando personas...')
        while creadas < total_personas and intentos < max_intentos:
            doc_id = str(faker.unique.random_number(digits=8))
            if doc_id in existentes:
                intentos += 1
                continue
            nombre = faker.first_name()
            apellido = faker.last_name()
            telefono = faker.phone_number()
            email = faker.unique.email()
            fecha_nacimiento = faker.date_of_birth(minimum_age=18, maximum_age=90)
            genero = random.choice(['M', 'F', 'O'])
            pais = faker.country()
            tipo_persona = random.choice(['administrador', 'seguridad', 'propietario', 'inquilino', 'cliente'])
            direccion = faker.address()
            Persona.objects.create(
                nombre=nombre,
                apellido=apellido,
                documento_identidad=doc_id,
                telefono=telefono,
                email=email,
                fecha_nacimiento=fecha_nacimiento,
                genero=genero,
                pais=pais,
                tipo_persona=tipo_persona,
                direccion=direccion
            )
            existentes.add(doc_id)
            creadas += 1
            if creadas % 25 == 0:
                self.stdout.write(f'   {creadas} personas creadas...')
            intentos += 1
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total personas creadas: {creadas}'))
