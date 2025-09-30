from django.core.management.base import BaseCommand
from seguridad.models import Copropietarios
from core.models import Vivienda
from authz.models import Persona
from faker import Faker
from django.db import transaction
import random

class Command(BaseCommand):
    help = 'Crea copropietarios relacionados a personas y viviendas, omitiendo los ya existentes y excepciones.'

    def handle(self, *args, **kwargs):
        faker = Faker()
        viviendas_omitidas = {"A-101", "C-103"}
        viviendas = Vivienda.objects.exclude(numero_casa__in=viviendas_omitidas)
        personas = Persona.objects.all()
        creados = 0
        self.stdout.write('👥 Poblando copropietarios...')
        for persona, vivienda in zip(personas, viviendas):
            # Verificar que no exista ya un copropietario con ese documento
            if Copropietarios.objects.filter(numero_documento=persona.documento_identidad).exists():
                continue
            try:
                Copropietarios.objects.create(
                    nombres=persona.nombre,
                    apellidos=persona.apellido,
                    numero_documento=persona.documento_identidad,
                    tipo_documento=random.choice(['CC', 'CE', 'PA', 'TI']),
                    telefono=persona.telefono,
                    email=persona.email,
                    unidad_residencial=vivienda.numero_casa,
                    tipo_residente=random.choice(['Propietario', 'Inquilino', 'Familiar']),
                    usuario_sistema=None,
                    activo=True
                )
                creados += 1
                if creados % 25 == 0:
                    self.stdout.write(f'   {creados} copropietarios creados...')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'No se pudo crear copropietario para persona {persona.id} y vivienda {vivienda.numero_casa}: {e}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total copropietarios creados: {creados}'))
        self.stdout.write(self.style.WARNING(f'Viviendas omitidas: {', '.join(viviendas_omitidas)}'))
