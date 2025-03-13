from django.db import models
from .utils import from_cyrillic_to_eng

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=50, verbose_name="Enter the city where you live", 
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = "Name of city where you live:"
        verbose_name_plural = "The names of cities where you live"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self. slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)
    
class ProgLanguage(models.Model):
    name = models.CharField(max_length=50, verbose_name="Enter your programming language", 
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = "Name of programming language which you use"
        verbose_name_plural = "The names of programming languages that you use"

    def __str__(self):
        return self.name
    
    # In my opininion, in this func we 

class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name="Vacancy title")
    company_name = models.CharField(max_length=250, verbose_name="Name of the company")
    description = models.TextField(verbose_name="Vacancy description")
    city = models.ForeignKey("City", on_delete=models.CASCADE, verbose_name="City")
    programming_language = models.ForeignKey("ProgLanguage", on_delete=models.CASCADE, verbose_name="Programming Language")

    timestamp = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancions"

    def __str__(self):
        return self.title

