clean:
	find . | grep -E "__pycache__|\.pyc|\.pyo$\" | xargs rm -rf;clear

run:
	make clean;fuser -k 8000/tcp;python manage.py runserver --settings=settings.local

m:
	python manage.py migrate --settings=settings.local

mm:
	python manage.py makemigrations --settings=settings.local

