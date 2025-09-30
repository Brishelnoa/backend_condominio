from django.core.management.base import BaseCommand
from core.models.administracion import Pagos
from authz.models import Persona, Usuario
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crea pagos mensuales de expensas para cada persona durante un año, omitiendo los ya existentes.'

    def handle(self, *args, **kwargs):
        faker = Faker()
        personas = Persona.objects.all()
        metodos_pago = ['efectivo', 'transferencia', 'tarjeta', 'cheque']
        estados = ['procesado', 'pendiente_verificacion', 'rechazado', 'reembolsado']
        year = datetime.now().year
        creados = 0
        self.stdout.write('💸 Poblando pagos de expensas (1 año por persona)...')
        for persona in personas:
            for mes in range(1, 13):
                fecha_pago = datetime(year, mes, random.randint(1, 28), random.randint(8, 20), random.randint(0, 59))
                existe = Pagos.objects.filter(persona=persona, fecha_pago__year=year, fecha_pago__month=mes, tipo_pago='expensa').exists()
                if existe:
                    continue
                Pagos.objects.create(
                    persona=persona,
                    tipo_pago='expensa',
                    expensa=None,  # Si tienes expensas mensuales, puedes asociar aquí
                    multa=None,
                    reserva=None,
                    monto=Decimal(random.randint(200, 800)),
                    fecha_pago=fecha_pago,
                    metodo_pago=random.choice(metodos_pago),
                    numero_comprobante=faker.unique.bothify(text='CP-#####'),
                    comprobante_archivo=None,
                    estado=random.choice(estados),
                    procesado_por=None
                )
                creados += 1
                if creados % 50 == 0:
                    self.stdout.write(f'   {creados} pagos creados...')
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total pagos creados: {creados}'))
