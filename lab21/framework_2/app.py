from api import API
import json
from middleware import Middleware
from orm import Database
from waitress import serve

app = API()
db = Database()


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request", req.url)

    def process_response(self, req, res):
        print("Processing response", req.url)


app.add_middleware(SimpleCustomMiddleware)


@app.route("/posts/{pk}")
def posts_work_by_id(request, response, pk):
    method = request.method
    if method == "GET":
        response.text, response.status_code = get_post_by_id(pk)
    elif method == "PUT":
        response.text, response.status_code = update_post_by_id(pk, json.loads(request.body.decode("UTF-8")))
    elif method == "PATCH":
        response.text, response.status_code = patch_post_by_id(pk, json.loads(request.body.decode("UTF-8")))
    elif method == "DELETE":
        response.text, response.status_code = delete_post_by_id(pk)


@app.route("/posts/")
def posts(request, response):
    method = request.method
    if method == "GET":
        if request.params:
            response.text, response.status_code = found_posts_by_params(request.params)
        else:
            response.text, response.status_code = get_all_posts()
    elif method == "POST":
        data = json.loads(request.body.decode("UTF-8"))
        if type(data) is dict:
            response.text, response.status_code = insert_post(data)
        else:
            response.text, response.status_code = insert_many_posts(data)


def validate(pk=False, number_likes=False):
    if pk is not False:
        if not str(pk).isdigit():
            return 'Incorrect ID', 400
    if number_likes is not False:
        if not str(number_likes).isdigit():
            return 'Incorrect number of like', 400


def get_post_by_id(pk):
    error_message = validate(pk=pk)
    if error_message:
        return error_message
    data = db.get_record_by_id(pk)
    if data:
        return f"{json.dumps(data, indent = 5)}", 200
    return 'Data not found', 204


def update_post_by_id(pk, body_data):
    error_message = validate(pk, number_likes=body_data['likes'])
    if error_message:
        return error_message
    data = db.update_record(pk, body_data['title'], body_data['body'], body_data['likes'])
    if data:
        return f"{json.dumps(data, indent = 5)}", 201
    return 'Record to update not found ', 204


def patch_post_by_id(pk, body_data):
    title, body, likes = body_data.get('title', False), body_data.get('body', False), body_data.get('likes', False)
    if not any([title, body, likes]):
        return 'Column not found ', 400
    error_message = validate(pk, number_likes=likes)
    if error_message:
        return error_message
    data = db.patch_update_record(pk, title, body, likes)
    if data:
        return f"{json.dumps(data, indent = 5)}"
    return 'Not found record by id', 404


def found_posts_by_params(data):
    name_col = 'likes'
    number_likes = data.get(name_col, False)
    if not number_likes:
        return 'Key not found', 400
    error_message = validate(number_likes=number_likes)
    if error_message:
        return error_message
    data = db.get_record_with_like(name_col, number_likes)
    if data:
        return f"{json.dumps(data, indent = 5)}", 200
    else:
        return 'Data not found', 204


def delete_post_by_id(pk):
    error_message = validate(pk)
    if error_message:
        return error_message
    return db.delete_record(pk)


def get_all_posts():
    data = db.get_all_records()
    if data:
        return f"{json.dumps(data, indent = 5)}", 200
    return 'Data not found', 204


def insert_post(body_data):
    title, body, likes = body_data.get('title', False), body_data.get('body', False), body_data.get('likes', False)
    if not any([title, body, likes]):
        return 'Columns not found ', 400
    error_message = validate(number_likes=likes)
    if error_message:
        return error_message
    data = db.add_new_record(title, body, likes)
    return f"{json.dumps(data, indent = 5)}", 201


def insert_many_posts(body_data):
    return db.add_many_new_record(body_data)


serve(app, host="localhost", port=8000)
