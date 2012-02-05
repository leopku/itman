from django.template import Library

register = Library()

@register.inclusion_tag('lib/admin_edit.html',takes_context=True)
def admin_edit(context, obj):
    user = context['request'].user
    
    package = obj.__class__._meta.app_label
    name = obj.__class__.__name__.lower()
 
    permitted = user.has_perm("%s.change_%s" % (package, name)) and user.is_staff
    
    edit_url = "/admin/%s/%s/%s/" % (package, name, obj.pk)
        
    return {'permitted': permitted,
            'edit_url': edit_url}