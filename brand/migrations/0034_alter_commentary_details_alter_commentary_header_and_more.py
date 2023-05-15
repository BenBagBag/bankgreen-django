# Generated by Django 4.1.7 on 2023-05-15 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("brand", "0033_alter_institutioncredential_prismic_api_id")]

    operations = [
        migrations.AlterField(
            model_name="commentary",
            name="details",
            field=models.TextField(
                blank=True,
                help_text="This text has been or is in the process of being migrated to prismic and is now read only.",
            ),
        ),
        migrations.AlterField(
            model_name="commentary",
            name="header",
            field=models.TextField(
                blank=True,
                help_text="This text has been or is in the process of being migrated to prismic and is now read only.",
            ),
        ),
        migrations.AlterField(
            model_name="commentary",
            name="subtitle",
            field=models.TextField(
                blank=True,
                help_text="This text has been or is in the process of being migrated to prismic and is now read only.",
            ),
        ),
        migrations.AlterField(
            model_name="commentary",
            name="summary",
            field=models.TextField(
                blank=True,
                help_text="This text has been or is in the process of being migrated to prismic and is now read only.",
            ),
        ),
    ]
