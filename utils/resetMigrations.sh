#!/bin/bash
mv back_office/migrations/load_initial_data.py back_office/
mv finances/migrations/load_initial_data.py finances/
mv inventories/migrations/load_initial_data.py inventories/

rm -f {back_office,finances,operations,inventories}/migrations/0*.py

source venv/bin/activate
python manage.py makemigrations
deactivate

mv back_office/load_initial_data.py back_office/migrations/
mv finances/load_initial_data.py finances/migrations/
mv inventories/load_initial_data.py inventories/migrations/

#python manage.py createsuperuser --noinput --username root --first_name root --last_name toor --email pepedou@gmail.com
#python manage.py changepassword root
#deactivate
