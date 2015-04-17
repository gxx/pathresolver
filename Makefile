test :
	python setup.py test

coverage :
	rm -rf .coverage htmlcov
	coverage run setup.py test
	coverage report

coverage_show : coverage
	coverage html
	google-chrome htmlcov/index.html

pypi :
	python setup.py bdist upload
	python setup.py sdist upload
	python setup.py bdist_egg upload
	python setup.py bdist_wheel upload
