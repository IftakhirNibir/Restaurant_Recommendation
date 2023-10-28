import os
import csv
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

# Import Django modules
import django
django.setup()
from myapp.models import Restaurant_DB

def insert_csv_data():
  with open('popularity.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
       try:
          restaurant_db = Restaurant_DB()
          restaurant_db.name = row[1]
          restaurant_db.rating = float(row[2])
          restaurant_db.address = row[3]
          restaurant_db.delivery = row[4]
          restaurant_db.cuisine= row[5]
          restaurant_db.save()
       except ValueError:
        # Skip the row if the rating column is a string
        continue
      
if __name__ == '__main__':
    insert_csv_data()
