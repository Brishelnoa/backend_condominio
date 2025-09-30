from django.core.management.base import BaseCommand
from core.models.propiedades_residentes import TiposInfracciones
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crea tipos de infracciones básicos si no existen.'

    def handle(self, *args, **kwargs):
        tipos_basicos = [
            {'codigo': 'RUIDO', 'nombre': 'Ruido excesivo', 'descripcion': 'Generar ruidos molestos fuera de horario permitido.', 'monto_multa': 200},
            {'codigo': 'ESTAC', 'nombre': 'Mal estacionamiento', 'descripcion': 'Estacionar en lugares no permitidos.', 'monto_multa': 150},
            {'codigo': 'BASURA', 'nombre': 'Disposición incorrecta de basura', 'descripcion': 'No sacar la basura en horario o lugar adecuado.', 'monto_multa': 100},
            {'codigo': 'MASCOTA', 'nombre': 'Mascota sin control', 'descripcion': 'Mascota suelta o sin correa en áreas comunes.', 'monto_multa': 120},
            {'codigo': 'DANIO', 'nombre': 'Daño a propiedad común', 'descripcion': 'Causar daño a áreas o bienes comunes.', 'monto_multa': 300},
        ]
        creados = 0
        self.stdout.write('🚨 Poblando tipos de infracciones...')
        for tipo in tipos_basicos:
            if TiposInfracciones.objects.filter(codigo=tipo['codigo']).exists():
                continue
            TiposInfracciones.objects.create(
                codigo=tipo['codigo'],
                nombre=tipo['nombre'],
                descripcion=tipo['descripcion'],
                monto_multa=Decimal(tipo['monto_multa']),
                genera_restriccion=False,
                tipo_restriccion=None,
                detectable_por_ia=False,
                nivel_confianza_minima=Decimal('0.85'),
                requiere_verificacion_humana=True,
                activo=True
            )
            creados += 1
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total tipos de infracciones creados: {creados}'))
