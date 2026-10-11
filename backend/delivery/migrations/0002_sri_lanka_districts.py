from django.db import migrations

# Sri Lanka's 25 districts. All start switched off with no fee; the owner
# turns on the ones the shop delivers to and sets fees and delivery times.
DISTRICTS = [
    "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Galle",
    "Gampaha", "Hambantota", "Jaffna", "Kalutara", "Kandy", "Kegalle",
    "Kilinochchi", "Kurunegala", "Mannar", "Matale", "Matara", "Monaragala",
    "Mullaitivu", "Nuwara Eliya", "Polonnaruwa", "Puttalam", "Ratnapura",
    "Trincomalee", "Vavuniya",
]


def add_sri_lanka(apps, schema_editor):
    Country = apps.get_model("delivery", "Country")
    District = apps.get_model("delivery", "District")
    sri_lanka, _ = Country.objects.get_or_create(
        code="LK", defaults={"name": "Sri Lanka", "delivery_enabled": True}
    )
    for name in DISTRICTS:
        District.objects.get_or_create(country=sri_lanka, name=name)


def remove_sri_lanka(apps, schema_editor):
    Country = apps.get_model("delivery", "Country")
    District = apps.get_model("delivery", "District")
    District.objects.filter(country__code="LK", name__in=DISTRICTS).delete()
    Country.objects.filter(code="LK").delete()


class Migration(migrations.Migration):
    dependencies = [("delivery", "0001_initial")]

    operations = [migrations.RunPython(add_sri_lanka, remove_sri_lanka)]
