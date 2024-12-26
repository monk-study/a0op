import json
from IPython.display import display_javascript

js_code = """
var cookies = document.cookie.split(';').map(c => c.trim());
var authCookie = cookies.find(c => c.startsWith('authservice_session='));
if (authCookie) {
    var cookieValue = authCookie.split('=')[1];
    IPython.notebook.kernel.execute('auth_cookie = "' + cookieValue + '"');
}
"""
display_javascript(js_code, raw=True)

client = kfp.Client(
    host='http://ml-pipeline.kubeflow.svc.cluster.local:8888',
    cookies={'authservice_session': auth_cookie}
)
