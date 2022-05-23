from django.shortcuts import redirect

def auth_middleware(get_response):

    def middleware(request):

        returnUrl=request.META['PATH_INFO']
        print(request.META['PATH_INFO'])

        if not request.session.get('customer'):
            return redirect(f'/signin?return_url={returnUrl}')
        else:
            pass
        response = get_response(request)

        return response

    return middleware
