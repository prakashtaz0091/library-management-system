from django.http import HttpResponseForbidden


def has_to_be_librarian(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.profile.is_librarian:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return wrapper