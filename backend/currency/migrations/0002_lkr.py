from django.db import migrations


def add_lkr(apps, schema_editor):
    Currency = apps.get_model("currency", "Currency")
    Currency.objects.get_or_create(code="LKR", defaults={"name": "Sri Lankan rupee", "symbol": "Rs"})


def remove_lkr(apps, schema_editor):
    apps.get_model("currency", "Currency").objects.filter(code="LKR").delete()


class Migration(migrations.Migration):
    dependencies = [("currency", "0001_initial")]

    operations = [migrations.RunPython(add_lkr, remove_lkr)]
