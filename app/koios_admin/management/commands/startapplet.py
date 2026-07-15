from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand

TEMPLATE_DIR = Path(__file__).parent.resolve() / '..' / 'templates'

class Command(BaseCommand):
    help = "Create a Koios applet with the required files."

    def add_arguments(self, parser):
        parser.add_argument("name")


    def handle(self, *args, **options):
        name    = options["name"]
        app_dir = Path(name)
        # Default startapp
        call_command("startapp", name)
        # Custom templates
        self.write_templates(name)



    def write_templates(self, name):
        def write_template(tpl_path, applet_name):
            app_dir   = Path(applet_name)
            file_path = app_dir / tpl_path.name[:-4]
            data      = open(tpl_path).read().format(name=name)
            file_path.write_text(data, encoding="utf-8")
            self.stdout.write(self.style.SUCCESS(f"Created {tpl_path.name[:-4]}"))

        for template in TEMPLATE_DIR.glob("*.tpl"):
            write_template(template, name)

        (Path(name) / 'static' / name).mkdir(parents=True)
        (Path(name) / 'templates' / name).mkdir(parents=True)
