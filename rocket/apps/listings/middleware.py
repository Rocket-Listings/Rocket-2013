class GlobalCookieMiddleware(object):
    def process_response(self, request, response):
        response.set_cookie('hermes-enabled', value='true')
        return response
