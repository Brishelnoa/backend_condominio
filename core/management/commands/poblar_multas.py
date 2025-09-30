from django.core.management.base import BaseCommand
from core.models.propiedades_residentes import MultasSanciones, TiposInfracciones
from authz.models import Persona
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crea 2 a 5 multas por persona, usando tipos de infracción existentes.'

    def handle(self, *args, **kwargs):
        faker = Faker()
        personas = list(Persona.objects.all())
        tipos = list(TiposInfracciones.objects.all())
        if not tipos:
            self.stdout.write(self.style.WARNING('No hay tipos de infracciones para asignar multas.'))
            return
        creados = 0
        self.stdout.write('⚠️ Poblando multas y sanciones...')
        for persona in personas:
            cantidad = random.choices([2, 3, 4, 5], weights=[1, 2, 2, 1])[0]
            for _ in range(cantidad):
                tipo = random.choice(tipos)
                persona_responsable = random.choice(personas)
                MultasSanciones.objects.create(
                    persona_responsable=persona_responsable,
                    persona_infractor=persona,
                    tipo_infraccion=tipo,
                    descripcion_detallada=faker.sentence(),
                    monto=tipo.monto_multa,
                    fecha_infraccion=faker.date_time_between(start_date='-1y', end_date='now'),
                    ubicacion_infraccion=faker.street_name(),
                    estado=random.choice(['pendiente', 'notificada', 'pagada', 'anulada', 'en_disputa']),
                    evidencia_fotos=[],
                    generada_por_ia=random.choice([True, False]),
                    deteccion_ia=None,
                    camara_origen=None,
                    nivel_confianza_ia=Decimal(str(round(random.uniform(0.85, 1.0), 4))),
                    verificada_por=None,
                    fecha_notificacion=None,
                    fecha_pago=None,
                    metodo_notificacion=[],
                    observaciones='',
                    requiere_audiencia=random.choice([True, False])
                )
                creados += 1
                if creados % 25 == 0:
                    self.stdout.write(f'   {creados} multas creadas...')
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total multas creadas: {creados}'))
