from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Pobla la base de datos con viviendas de prueba usando Faker'

    def handle(self, *args, **kwargs):
        from core.models import Vivienda
        from faker import Faker
        from decimal import Decimal
        import random

        faker = Faker()
        total_viviendas = 200
        omitidas = {"A-101", "C-103"}
        creadas = 0
        intentos = 0
        max_intentos = 1000
        viviendas_creadas = set(Vivienda.objects.values_list('numero_casa', flat=True))

        self.stdout.write("🏠 Poblando viviendas...")
        while creadas < total_viviendas and intentos < max_intentos:
            bloque = random.choice(['A', 'B', 'C', 'D', 'E'])
            tipo_vivienda = random.choice(['casa', 'departamento', 'local'])
            if tipo_vivienda == 'casa':
                numero = f"{bloque}-{random.randint(100, 199)}"
            elif tipo_vivienda == 'departamento':
                numero = f"{bloque}-DPT-{random.randint(1, 50)}"
            else:
                numero = f"{bloque}-LOC-{random.randint(1, 20)}"
            if numero in omitidas or numero in viviendas_creadas:
                intentos += 1
                continue
            metros = round(random.uniform(45, 180), 2)
            tarifa = round(random.uniform(100, 500), 2)
            tipo_cobranza = random.choice(['por_casa', 'por_metro_cuadrado'])
            estado = 'activa'
            Vivienda.objects.create(
                numero_casa=numero,
                bloque=bloque,
                tipo_vivienda=tipo_vivienda,
                metros_cuadrados=Decimal(str(metros)),
                tarifa_base_expensas=Decimal(str(tarifa)),
                tipo_cobranza=tipo_cobranza,
                estado=estado
            )
            viviendas_creadas.add(numero)
            creadas += 1
            if creadas % 25 == 0:
                self.stdout.write(f"   {creadas} viviendas creadas...")
            intentos += 1
        self.stdout.write(self.style.SUCCESS(f"✅ Proceso finalizado. Total viviendas creadas: {creadas}"))
        self.stdout.write(self.style.WARNING(f"Viviendas omitidas: {', '.join(omitidas)}"))
