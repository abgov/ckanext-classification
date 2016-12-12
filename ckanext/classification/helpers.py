import  ckanext.scheming.helpers as h
import pylons.config as config
import re
from ckan.plugins import toolkit
from ckanext.classification.model import SecurityMember
import ckan.model as model
import ckan.authz as authz


def _get_classfication_field(dataset_type):
	scheme = h.scheming_get_schema('dataset', dataset_type)
	if not scheme:
		return None
	fields = scheme.get('resource_fields')
	if not fields:
		return None
	f = h.scheming_field_by_name(fields, "classification")
	if f:
		return f
	else:
		return None


def get_all_classifications_label(dataset_type):
	classification = _get_classfication_field(dataset_type)
	if not classification:
		return []
	return [ c['label'] for c in classification['choices'] ]


def get_all_classifications(dataset_type):
	classification = _get_classfication_field(dataset_type)
	if not classification:
		return []
	return [ c['value'] for c in classification['choices'] ]


def get_dataset_types_w_classification():
	types = config['scheming.dataset_schemas']
	type_list = []
	for type in types.split():
		type = re.sub(r'.*?\:(.*?).json', r'\1', type)
		type_list.append(type)

	type_w_classification_list = []
	for t in type_list:
		f = _get_classfication_field(t)
		if f:
			type_w_classification_list.append(t)
	return type_w_classification_list


def get_classification(user_id, org_id, dataset_type):
	if is_admin(user_id, org_id):
		# highest classification for admin
		all_classifications = get_all_classifications(dataset_type)
		if not all_classifications:
			return None
		return all_classifications[-1]

	instance = SecurityMember.get(model.Session,
			               user_id=user_id,
			               group_id=org_id,
			               dataset_type=dataset_type)
	if instance:
		return instance.classification
	else:
		#default for everybody
		all_classifications = get_all_classifications(dataset_type)
		if not all_classifications:
			return None
		return all_classifications[0]


def get_org(package_string):
	m = re.search(r'/dataset/new_resource/(.*)', package_string)
	if m:
		package_id = m.group(1)
	else:
		package_id = package_string

	pkg = toolkit.get_action('package_show')( data_dict={'id': package_id} )
	return pkg['owner_org']


def get_current_user_id():
	if not toolkit.c.userobj:
		return None
	return toolkit.c.userobj.id


def is_admin(user, org):
    """ check if user is admin 
        params: user: name or id,
                org : name or id,
        rtype: boolean
    """
    if not user:
    	return False 
    username = model.User.get(user).name
    user_id = model.User.get(user).id
    if authz.is_sysadmin(username):
    	return True
    if org:
        org_id = model.Group.get(org).id
        admin_ids = authz.get_group_or_org_admin_ids(org_id)
        if user_id in admin_ids:
        	return True
    return False
