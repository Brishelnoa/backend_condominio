from django.core.management.base import BaseCommand
from core.models import Vivienda, Propiedad
from authz.models import Persona
from django.db import transaction
from decimal import Decimal
import random
from datetime import date

class Command(BaseCommand):
    help = 'Crea propiedades asociando personas y viviendas, sin modificar las existentes.'

    def handle(self, *args, **kwargs):
        personas = list(Persona.objects.all())
        viviendas = list(Vivienda.objects.all())
        propiedades_existentes = set(
            (p.vivienda_id, p.persona_id) for p in Propiedad.objects.all()
        )
        creadas = 0
        max_propiedades = min(len(personas), len(viviendas))
        random.shuffle(personas)
        random.shuffle(viviendas)
        self.stdout.write('🏠 Poblando propiedades...')
        with transaction.atomic():
            for persona, vivienda in zip(personas, viviendas):
                if (vivienda.id, persona.id) in propiedades_existentes:
                    continue
                try:
                    Propiedad.objects.create(
                        vivienda=vivienda,
                        persona=persona,
                        tipo_tenencia=random.choice(['propietario', 'inquilino']),
                        porcentaje_propiedad=Decimal('100.00'),
                        fecha_inicio_tenencia=date.today(),
                        activo=True
                    )
                    creadas += 1
                    if creadas % 25 == 0:
                        self.stdout.write(f'   {creadas} propiedades creadas...')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'No se pudo crear propiedad para persona {persona.id} y vivienda {vivienda.id}: {e}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total propiedades creadas: {creadas}'))
