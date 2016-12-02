=============
ckanext-classification
=============

This extension will plug in a security classification field to resource form
to control the classification of the resource. Also the plugin can config user
in organization management with highest classification. All the resources equal
or lower than this highest classification will be shown or created or edited by
the user.


------------
Requirements
------------

Ckan-2.6
ckanext-scheming

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-classification:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-classification Python package into your virtual environment::

     pip install ckanext-classification

3. Add ``classification`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Document any optional config settings here. For example::

1. Add this line into your ini config file:
   
   scheming.presets = ckanext.scheming:presets.json

2. Add this line into your ini config file:

   scheming.dataset_schemas =  ckanext.classification:dataset.json


------
Usage
------

1. Put this block into your json schema file (field names are fixed).

     {
      "field_name": "classification",
      "label": "Security Classification",
      "help_text": "The classification which is used upon this resource",
      "help_inline": false,
      "required": true,
      "validators": "scheming_required",
      "form_snippet": "classification.html",
      "choices": [
        {"value": "1", "label": "1"},
        {"value": "2", "label": "2"},
        {"value": "3", "label": "3"},
        {"value": "4", "label": "4"},
        {"value": "5", "label": "5"}
      ]
    }

--------
Notice
--------

1. All the field names should not be changed.

2. If change the options of process field, fanstatic/css/main.css must be maintained.

------------------------
Development Installation
------------------------

To install ckanext-classification for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/yongjiel/ckanext-classification.git
    cd ckanext-classification
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.classification --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-classification on PyPI
---------------------------------

ckanext-classification should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-classification. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-classification
----------------------------------------

ckanext-classification is availabe on PyPI as https://pypi.python.org/pypi/ckanext-classification.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
