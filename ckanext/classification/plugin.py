import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.classification.helpers as helpers
from model.security_member_model import (
    get_member_classification, 
    add_member_classification
)
from model import security_member_model
from ckan.config.routing import SubMapper
from ckanext.classification.logic import action


class ClassificationPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IPackageController, inherit=True)

    """  
    IConfigurer
    """
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'classification')


    """
    ITemplateHelpers
    """
    def get_helpers(self):
        return {
            'classification_is_admin': helpers.is_admin,
            'classification_get_all_classifications': helpers.get_all_classifications,
            'classification_get_dataset_types_w_classification': helpers.get_dataset_types_w_classification,
            'classification_get_org': helpers.get_org,
            'classification_get_current_user_id': helpers.get_current_user_id,
            'classification_get_classification': helpers.get_classification,
            'classification_get_all_classifications_label': helpers.get_all_classifications_label,
            'classification_get_label': helpers.get_label_by_type_value
        }

    """
    IConfigurable
    """
    def configure(self, config):
        security_member_model.setup()


    """
    IRoutes
    """
    def before_map(self, map):
        controller = 'ckanext.classification.controllers:SecurityClassificationController'
        with SubMapper(map, controller=controller) as m:
            m.connect('security_members', '/organization/{id}/security_members',
                      action='manage', ckan_icon='user')
            m.connect('security_members_remove', '/organization/{id}/security_members_remove',
                      action='remove')

        return map


    
    """
    IActions
    """
    def get_actions(self):
        actions = dict((name, function) for name, function
                       in action.__dict__.items()
                       if callable(function))
        return actions


    """
    IPackageController
    """
    def after_show(self, context, pkg_dict):
    	""" check if the resources classification is in user's assigned classification 
            range and filter out the resources needed.
    	"""
        current_user_id = helpers.get_current_user_id()
    	classification = helpers.get_classification(current_user_id, 
    		                                        pkg_dict['owner_org'], 
    		                                        pkg_dict['type'])
        if not classification:
            classification = 1
        resources = []
        for res in pkg_dict['resources']:
            if res:
                classif = res.get('classification')
                if classif and int(classif) <= classification or not classif:
                    # set up classification for old dataset with no classification field
                    if not classif:
                        res['classification'] = 1
                    resources.append(res)
        pkg_dict['resources'] = resources
        return pkg_dict

    def before_view(self, pkg_dict):
        #handle old data with no classification field
        flag_no_classification = False
        resources = []
        for res in pkg_dict['resources']:
            if res:
                classif = res.get('classification')
                # set up classification for old dataset with no classification field
                if not classif:
                    res['classification'] = 1
                    flag_no_classification = True
                resources.append(res)
        pkg_dict['resources'] = resources
        if flag_no_classification: 
            toolkit.get_action('package_update')(data_dict=pkg_dict)
        return pkg_dict
        