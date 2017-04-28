# -*- encoding: UTF-8 -*-
# --------------------------
import cherrypy
import json
from xenSplittingService.splitting_service import ContentSplit
# --------------------------


@cherrypy.expose
class webSplitService(object):
    def __init__(self):
        self.splitter = ContentSplit()

    @cherrypy.tools.accept(media='text/plain')
    # def GET(self):
    #     return 'Please use method POST'

    def GET(self, words, method, allow_english_output=True):
        if int(method) == 0:
            cherrypy.session['my_string'] = \
                json.dumps({'content': self.splitter.split(words, enable_english_output=bool(allow_english_output))})
        elif int(method) == 1:
            cherrypy.session['my_string'] = \
                json.dumps({'content': self.splitter.split_firmname(words, enable_english_output=bool(allow_english_output))})
        elif int(method) == 9:
            self.splitter.add_blocked_company_keyword(words, force_add=False)
        elif int(method) == 8:
            self.splitter.add_company_service_type(words, force_add=False)
        elif int(method) == 7:
            self.splitter.add_company_type(words, force_add=False)
        else:
            cherrypy.session['my_string'] = 'Not the legal method'
        return cherrypy.session['my_string']

if __name__ == '__main__':
    root = webSplitService()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(root, '/', conf)