from django.core.management.base import BaseCommand
from core.models.propiedades_residentes import EspacioComun
from faker import Faker
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crea espacios comunes básicos si no existen.'

    def handle(self, *args, **kwargs):
        faker = Faker()
        espacios_basicos = [
            {'nombre': 'Salón de Eventos', 'capacidad_maxima': 100, 'precio_por_hora': 200, 'precio_evento_completo': 1200},
            {'nombre': 'Piscina', 'capacidad_maxima': 40, 'precio_por_hora': 100, 'precio_evento_completo': 600},
            {'nombre': 'Cancha Polifuncional', 'capacidad_maxima': 30, 'precio_por_hora': 80, 'precio_evento_completo': 400},
            {'nombre': 'Quincho', 'capacidad_maxima': 20, 'precio_por_hora': 60, 'precio_evento_completo': 300},
            {'nombre': 'Gimnasio', 'capacidad_maxima': 25, 'precio_por_hora': 50, 'precio_evento_completo': 250},
        ]
        creados = 0
        self.stdout.write('🏢 Poblando espacios comunes...')
        for espacio in espacios_basicos:
            if EspacioComun.objects.filter(nombre=espacio['nombre']).exists():
                continue
            EspacioComun.objects.create(
                nombre=espacio['nombre'],
                descripcion=faker.sentence(),
                capacidad_maxima=espacio['capacidad_maxima'],
                precio_por_hora=Decimal(espacio['precio_por_hora']),
                precio_evento_completo=Decimal(espacio['precio_evento_completo']),
                es_gratuito=False,
                horario_apertura='06:00',
                horario_cierre='22:00',
                dias_disponibles=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
                requiere_pago=True,
                requiere_deposito_garantia=False,
                monto_deposito=Decimal('0.00'),
                genera_ingresos=True,
                reserva_maxima_dias_anticipacion=30,
                reserva_minima_horas_anticipacion=24,
                activo=True,
                imagen_url=None,
                reglas_uso=faker.sentence()
            )
            creados += 1
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total espacios comunes creados: {creados}'))
