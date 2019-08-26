from django.db import models


class Citizen(models.Model):
    id = models.CharField(max_length=128, primary_key=True,)
    citizen_id = models.IntegerField()
    town = models.CharField(max_length=1000, default='',)
    street = models.CharField(max_length=1000, default='',)
    building = models.CharField(max_length=1000, default='',)
    apartment = models.CharField(max_length=1000, default='',)
    name = models.CharField(max_length=1000, default='',)
    birth_date = models.DateField()
    gender = models.CharField(max_length=8, default='',)
    import_id = models.ForeignKey(
        'Import',
        on_delete=models.CASCADE,
        related_name='citizens',
    )
    relatives = models.ManyToManyField(
        'self',
        through='Relationship',
        related_name='related_to',
        symmetrical=False,
    )

    class Meta:
        unique_together = ['import_id', 'citizen_id', ]


class Import(models.Model):
    import_id = models.AutoField(primary_key=True,)


class Relationship(models.Model):
    from_citizen = models.ForeignKey(
        Citizen,
        related_name='from_people',
        on_delete=models.CASCADE,
    )
    to_citizen = models.ForeignKey(
        Citizen,
        related_name='to_people',
        on_delete=models.CASCADE,
    )
