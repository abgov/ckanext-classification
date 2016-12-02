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
        "form_snippet": "classification.html",
        "choices": [
          {"value": "1", "label": "1"},
          {"value": "2", "label": "2"},
          {"value": "3", "label": "3"},
          {"value": "4", "label": "4"},
          {"value": "5", "label": "5"}
        ]
        }

2. Go to organization management page, you can find a tag named "Resource Classification".
Config the users in there. And back to package and create or edit a resource. The classification
of that resource will be controlled in the range that is defined in the config.


--------
Notice
--------

1. All the field names should not be changed.

2. If change the options of process field, fanstatic/css/main.css must be maintained.



