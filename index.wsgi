import sae 
from onlineproject import wsgi 
application = sae.create_wsgi_app(wsgi.application) 

