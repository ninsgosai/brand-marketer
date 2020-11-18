from django.shortcuts import redirect

def is_admin(my_function):
    def wrapper(request, *args, **kwargs):
        if request.user and request.user.is_superuser:
            return my_function(request, *args, **kwargs)
        else:
            return redirect('loginadmin')
    return wrapper