import json
import os
from django.core.management.base import BaseCommand
from member.models import Department, Commune, Arrondissement, Neighborhood

class Command(BaseCommand):
    help = "Load Bénin locations from nested JSON into database"

    def handle(self, *args, **kwargs):
        # Skip if data already exists in database
        if Department.objects.exists():
            self.stdout.write(self.style.SUCCESS("Les données géographiques du Bénin sont déjà chargées. Passage."))
            return

        # Chemin relatif vers le JSON dans le même dossier que cette commande
        dir_path = os.path.dirname(os.path.realpath(__file__))
        json_file = os.path.join(dir_path, 'decoupage_territorial_benin.json')

        with open(json_file, encoding='utf-8') as f:
            data = json.load(f)

        for dep in data:
            department_obj, _ = Department.objects.get_or_create(
                name=dep['lib_dep'],
                country='BJ'
            )

            for com in dep.get('communes', []):
                commune_obj, _ = Commune.objects.get_or_create(
                    name=com['lib_com'],
                    department=department_obj
                )

                for arr in com.get('arrondissements', []):
                    arr_obj, _ = Arrondissement.objects.get_or_create(
                        name=arr['lib_arrond'],
                        commune=commune_obj
                    )

                    for quart in arr.get('quartiers', []):
                        Neighborhood.objects.get_or_create(
                            name=quart['lib_quart'],
                            arrondissement=arr_obj
                        )

        self.stdout.write(self.style.SUCCESS('Toutes les données du Bénin ont été chargées dans la base !'))
