# from functools import wraps
# from django.http import HttpResponseRedirect


# def only_creators(function):
#     @wraps(function)
#     def wrap(request, *args, **kwargs):
#         profile = request.user.get_profile()
#         if profile.usertype == 'Superuser status':
#               return function(request, *args, **kwargs)
#         else:
#             return HttpResponseRedirect('/')

#   return wrap
