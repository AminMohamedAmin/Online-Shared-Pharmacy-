from django.db import models

# Create your models here.


class Department(models.Model):
    department_code = models.CharField(max_length=150, unique=True)
    department_name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    department_items = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('department_code',)
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.department_code


class Medicine(models.Model):
    department = models.ForeignKey(Department, related_name='medicine', on_delete=models.CASCADE)
    medicine_code = models.CharField(max_length=150, unique=True)
    medicine_name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    medicine_quantity = models.IntegerField(default=0)
    medicine_price = models.DecimalField(max_digits=10, decimal_places=2)
    medicine_desc = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('department',)
        index_together = (('id', 'slug'),)
        verbose_name = "Medicine"
        verbose_name_plural = "Medicines"

    def __str__(self):
        return self.medicine_code

class Delivery(models.Model):
    name = models.CharField(max_length=150)
    NID = models.CharField(max_length=150, unique=True)
    address = models.CharField(max_length=150)
    code = models.CharField(max_length=150, unique=True)
    created = models.DateTimeField(auto_now_add=True)
