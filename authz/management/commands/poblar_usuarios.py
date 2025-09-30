from django.core.management.base import BaseCommand
from authz.models import Persona, Usuario
from django.db import transaction

class Command(BaseCommand):
    help = 'Crea usuarios para personas que no tengan usuario asociado, sin modificar los existentes.'

    def handle(self, *args, **kwargs):
        password_generico = 'usuario123'
        personas = Persona.objects.all()
        usuarios_existentes = set(Usuario.objects.values_list('persona_id', flat=True))
        creados = 0
        self.stdout.write('👤 Poblando usuarios...')
        with transaction.atomic():
            for persona in personas:
                if persona.id in usuarios_existentes:
                    continue
                # El email puede no ser único, pero intentamos usarlo
                email = persona.email or f"usuario{persona.id}@test.com"
                try:
                    Usuario.objects.create_user(
                        email=email,
                        password=password_generico,
                        persona=persona,
                        estado='ACTIVO'
                    )
                    creados += 1
                    if creados % 25 == 0:
                        self.stdout.write(f'   {creados} usuarios creados...')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'No se pudo crear usuario para persona {persona.id}: {e}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Proceso finalizado. Total usuarios creados: {creados}'))
        self.stdout.write(self.style.WARNING(f'Contraseña genérica para todos: {password_generico}'))
