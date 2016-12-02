import ckan.lib.base as base
from ckan.common import _, request, c
import ckan.lib.helpers as helpers
import ckan.model as model
import ckan.plugins.toolkit as toolkit


class SecurityClassificationController(base.BaseController):
    """ This controller controls the actions of adding and removing
	    users for specific security classification. It is implemented
	    in organization edit function.
    """ 
    def _get_context_controller(self):
        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user or toolkit.c.author}
        try:
            toolkit.check_access('member_create', context, {})
        except toolkit.NotAuthorized:
            toolkit.abort(401, toolkit._('User not authorized to manage page'))

        controller = 'ckanext.classification.controllers:SecurityClassificationController'
        return context, controller

    
    def _action(self, action, context, username, groupname, 
                dataset_type, classification, success_msg):
        try:
            toolkit.get_action(action)(context,
                            data_dict={'username': username, 
                                       'groupname': groupname, 
                                       'dataset_type': dataset_type,
                                       'classification': classification}
            )
        except toolkit.NotAuthorized:
            toolkit.abort(401,
                          toolkit._('Unauthorized to perform that action'))
        except toolkit.ObjectNotFound as e :
            error_message = (e.message or e.error_summary
                         or e.error_dict)
            helpers.flash_error(error_message)
        except toolkit.ValidationError as e:
            error_message = e.error_dict
            helpers.flash_error(error_message['message'])
        else:
            helpers.flash_success(toolkit._(success_msg))


    def manage(self, id):
        context, controller = self._get_context_controller()
        username = toolkit.request.params.get('username')
        dataset_type = toolkit.request.params.get("field-dataset_type")
        classification = toolkit.request.params.get('field-classification')
        group_object = model.Group.get(id)
        groupname = group_object.name

        toolkit.c.group_dict = group_object

        if toolkit.request.method == 'POST':
            if username:
                user_object = model.User.get(username)
                if not user_object:
                    helpers.flash_error("User \"{0}\" not exist!".format(username))
                else:
                    self._action('security_member_create', 
                             context, 
                             username, 
                             groupname, 
                             dataset_type,
                             classification,
                             "User \"{0}\" is now a member of resource classification on type \"{1}\"".format(username, dataset_type))
            else:
                helpers.flash_error("Please input username first.")
            return toolkit.redirect_to(toolkit.url_for(controller=controller,
                                                       action='manage', 
                                                       id=id))

        security_members_list = toolkit.get_action('security_member_list')(context, 
                                                    data_dict={'groupname': groupname})
        return toolkit.render(
            'organization/manage_security_members.html',
            extra_vars={
                'security_members_list': security_members_list,
            }
        )


    def remove(self, id):
        if 'cancel' in toolkit.request.params:
            toolkit.redirect_to(controller=controller, action='manage', id=id)

        context, controller = self._get_context_controller()
        user_id = toolkit.request.params['user']
        user_object = model.User.get(user_id)
        username = user_object.name
        group_object = model.Group.get(id)
        groupname = group_object.name
        dataset_type = toolkit.request.params['dataset_type']
        classification = toolkit.request.params['classification']
        
        if toolkit.request.method == 'POST' and user_id:
            self._action('security_member_delete', 
                         context, 
                         username, 
                         groupname, 
                         dataset_type,
                         classification,
                         "User \"{0}\" is no longer a member of resource classification on type \"{1}\"".format(username, dataset_type))

        return toolkit.redirect_to(
                helpers.url_for(controller=controller, action='manage', id=id))
