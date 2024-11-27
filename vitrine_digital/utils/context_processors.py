def sidebar_template(request):
    if request.user.is_authenticated:
        if request.user.has_perm('add_empresa'):
            return {'sidebar_template': 'sidebar-empresa.html'}
        else:
            return {'sidebar_template': 'sidebar-cliente.html'}
    else:
        return {'sidebar_template': 'sidebar-noauth.html'}