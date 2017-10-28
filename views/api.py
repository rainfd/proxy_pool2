from flask import Flask, request, render_template
from flask.views import MethodView
from flask import jsonify
from werkzeug.wrappers import Response

from proxygetter.ext import proxydb


def jsonify_status(obj, status=200):
    result = jsonify(obj)
    result.status = status
    return result


# jsonify = jsonify_status


def create_app():
    app = Flask(__name__)
    return app


json_api = create_app()


class ProxyAPI(MethodView):

    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        https = request.args.get('https', None)
        anonymous = request.args.get('anonymous', None)
        filter = {

        }
        if https == 'true':
            filter['https'] = True
        elif https == 'false':
            filter['https'] = False
        if anonymous == 'true':
            filter['anonymous'] = True
        elif anonymous == 'false':
            filter['anonymous'] = False
        start = page_size * (page - 1)
        end = page_size * page
        proxies = proxydb.find(filter)
        return jsonify({
            'proxies': list(proxies[start:end]),
            'total': proxies.count()
        })


# Local test CORS
@json_api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@json_api.errorhandler(500)
@json_api.errorhandler(404)
def error_handler(error):
    if hasattr(error, 'name'):
        msg = error.name
        code = error.code
    else:
        # msg = error.__name__
        msg = str(error)
        code = 500
    return jsonify({'message': msg}), code



json_api.add_url_rule('/proxy', view_func=ProxyAPI.as_view('proxy'))
