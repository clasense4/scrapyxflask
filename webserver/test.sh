source ../env/bin/activate
rm -rf .coverage
nosetests test_company.py --with-coverage --cover-package=main --cover-html --logging-level=DEBUG
