from django.core.management.base import BaseCommand, CommandError
from ...views.template import create_template
from ...models import Board


class Command(BaseCommand):
    help = "Delete templates"

    def handle(self, *args, **options):
        templates = Board.objects.filter(is_template=True).all()
        if len(templates) == 0:
            self.stdout.write(self.style.WARNING("There is no template to delete"))
        for t in templates:
            t.delete()
            self.stdout.write("%s template " %t.name + self.style.SUCCESS("deleted successfully"))