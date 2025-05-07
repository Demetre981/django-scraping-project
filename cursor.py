import codecs
import os, sys

from django.db import DatabaseError

proj_path = os.path.dirname(os.path.abspath("manage.py"))
sys.path.append(proj_path)
os.environ["DJANGO_SETTINGS_MODULE"] = "app.settings"

import django
django.setup()
## тут ми підключаємо всі налаштування джанго, бо ми робимо ззовні проекту
from django.db import DatabaseError
from parser import *
from api.models import Vacancy, ProgLanguage, City

parser = ((work, "https://www.work.ua/jobs-remote-python/"), 
          (dou, "https://jobs.dou.ua/vacancies/?category=Python"),
          (djinni, "https://djinni.co/jobs/?primary_keyword=Python&region=UKR&location=kyiv")
          )

city = City.objects.filter(slug="kiev").first()
language = ProgLanguage.objects.filter(name="Python").first()

jobs, errors = [], []
for func, url in parser:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, programming_language=language)
    try:

        v.save()
    except DatabaseError:
        pass
print(type(v))
        


# h = codecs.open("work.txt", "w", "utf-8")
# h.write(str(jobs))
# h.close