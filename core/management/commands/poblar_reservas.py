from django.core.management.base import BaseCommand
from core.models.propiedades_residentes import ReservaEspacio, EspacioComun
from authz.models import Persona
from faker import Faker
import random
from datetime import datetime, timedelta, time
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crea reservas de espacio para personas y espacios comunes existentes.'

    def handle(self, *args, **kwargs):
        faker = Faker()
        personas = list(Persona.objects.all())
        espacios = list(EspacioComun.objects.all())
        if not espacios:
            self.stdout.write(self.style.WARNING('No hay espacios comunes para reservar.'))
            return
        creados = 0
        self.stdout.write('📅 Poblando reservas de espacio...')
        for persona in personas:
            cantidad = random.randint(1, 2)
            for _ in range(cantidad):
                espacio = random.choice(espacios)
                fecha_reserva = faker.date_between(start_date='-3M', end_date='+3M')
                hora_inicio = time(random.randint(7, 20), 0)
                hora_fin = (datetime.combine(datetime.today(), hora_inicio) + timedelta(hours=2)).time()
                ReservaEspacio.objects.create(
                    persona=persona,
                    espacio_comun=espacio,
                    fecha_reserva=fecha_reserva,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    tipo_evento=faker.word(),
                    estado=random.choice(['solicitada', 'confirmada', 'pagada', 'en_uso', 'completada', 'cancelada', 'no_show']),
                    monto_total=Decimal(random.randint(50, 500)),
                    monto_deposito=Decimal(random.randint(0, 100)),
                    fecha_solicitud=datetime.now(),
                    fecha_pago=None,
                    fecha_confirmacion=None,
                    aprobada_por=None,
                    observaciones_cliente='',
                    observaciones_admin='',
                    calificacion_post_uso=None,
                    comentarios_post_uso=None
                )
                creados += 1
                if creados % 25 == 0:
                    self.stdout.write(f'   {creados} reservas creadas...')
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total reservas creadas: {creados}'))
