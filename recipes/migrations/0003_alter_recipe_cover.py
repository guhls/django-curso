# Generated by Django 4.1 on 2022-08-30 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0002_recipe_cover_alter_recipe_is_published"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="cover",
            field=models.ImageField(
                blank=True, default="", upload_to="recipes/covers/%Y/%m/%d/"
            ),
        ),
    ]
