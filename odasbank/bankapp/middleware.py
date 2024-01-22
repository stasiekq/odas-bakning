from django.http import HttpResponseForbidden
from django.shortcuts import redirect

class AdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not request.user.has_perm('auth.view_user'):
            return redirect('home')

        response = self.get_response(request)
        return response
