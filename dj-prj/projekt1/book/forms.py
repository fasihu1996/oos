from book.models import *
from django.forms import *


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        exclude = ()
        labels = {"fn": "First name",
                  "ln": "Last name"}
