from django.core.management.base import BaseCommand
from core.models.propiedades_residentes import Notificacion
from authz.models import Usuario
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Crea notificaciones para usuarios existentes.'

    def handle(self, *args, **kwargs):
        faker = Faker()
        usuarios = Usuario.objects.all()
        tipos = ['pago', 'seguridad', 'mantenimiento', 'reserva', 'general']
        creados = 0
        self.stdout.write('🔔 Poblando notificaciones...')
        for usuario in usuarios:
            cantidad = random.randint(1, 3)
            for _ in range(cantidad):
                Notificacion.objects.create(
                    usuario=usuario,
                    titulo=faker.sentence(nb_words=6),
                    mensaje=faker.paragraph(nb_sentences=3),
                    tipo=random.choice(tipos),
                    fecha_creacion=faker.date_time_between(start_date='-1y', end_date='now'),
                    enviada=random.choice([True, False]),
                    fecha_envio=None,
                    leida=random.choice([True, False]),
                    fecha_lectura=None,
                    origen_evento=None,
                    origen_id=None
                )
                creados += 1
                if creados % 50 == 0:
                    self.stdout.write(f'   {creados} notificaciones creadas...')
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total notificaciones creadas: {creados}'))
