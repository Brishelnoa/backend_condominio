from django.core.management.base import BaseCommand
from authz.models import Usuario, RelacionesPropietarioInquilino
from core.models import Vivienda
from faker import Faker
import random
from datetime import date, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crea 1 a 2 inquilinos por propietario, sin modificar relaciones existentes.'

    def handle(self, *args, **kwargs):
        faker = Faker()
        propietarios = Usuario.objects.filter(persona__tipo_persona='propietario')
        viviendas = list(Vivienda.objects.all())
        creados = 0
        self.stdout.write('🏢 Poblando relaciones propietario-inquilino...')
        for propietario in propietarios:
            # Seleccionar viviendas aleatorias para este propietario
            random.shuffle(viviendas)
            num_inquilinos = random.randint(1, 2)
            for _ in range(num_inquilinos):
                # Crear usuario inquilino
                persona_inq = propietario.persona
                inquilino = Usuario.objects.create_user(
                    email=faker.unique.email(),
                    password='usuario123',
                    persona=None,  # Si quieres asociar una persona, crea una nueva Persona aquí
                    estado='ACTIVO'
                )
                vivienda = random.choice(viviendas)
                # Verificar que no exista ya la relación activa
                existe = RelacionesPropietarioInquilino.objects.filter(
                    propietario=propietario,
                    inquilino=inquilino,
                    vivienda=vivienda,
                    activo=True
                ).exists()
                if existe:
                    continue
                fecha_inicio = faker.date_between(start_date='-2y', end_date='today')
                monto_alquiler = Decimal(random.randint(200, 2000))
                RelacionesPropietarioInquilino.objects.create(
                    propietario=propietario,
                    inquilino=inquilino,
                    vivienda=vivienda,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=None,
                    activo=True,
                    monto_alquiler=monto_alquiler,
                    observaciones='',
                )
                creados += 1
                if creados % 25 == 0:
                    self.stdout.write(f'   {creados} relaciones creadas...')
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total relaciones creadas: {creados}'))
