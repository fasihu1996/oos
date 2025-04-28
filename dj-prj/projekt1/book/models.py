from django.db import models

# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Author(models.Model):
    fn = models.CharField(max_length=30)
    ln = models.CharField(max_length=30)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.fn} {self.ln}"

class Book(models.Model):
    title = models.CharField(max_length=30)
    isbn = models.CharField(max_length=13)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        # hier list comprehension für erzeugung von authorenliste
        a_string = ", ".join([f"{a.fn} {a.ln}" for a in self.authors.all()])
        return f"{self.title} ({a_string}"
