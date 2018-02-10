from flask import Blueprint, render_template, request, json, url_for, flash
from werkzeug.utils import redirect

import src.models.users.decorators as user_decorators
from src.models.stores.store import Store

store_blueprint = Blueprint('stores', __name__)

@store_blueprint.route('/')
@user_decorators.requires_login
def index():
    stores = Store.all()
    return render_template('stores/store_index.html', stores=stores)

@store_blueprint.route('/store/<string:store_id>')
@user_decorators.requires_login
def store_page(store_id):
    return render_template('stores/store.html', store=Store.get_by_id(store_id))

@store_blueprint.route('/new', methods=['GET','POST'])
@user_decorators.requires_admin_permissions
def create_store():
    if request.method == 'POST':
        try:
            name = request.form['name']
            url_prefix = request.form['url_prefix']
            tag_name = request.form['tag_name']
            query = json.loads(request.form['query'])
        except:
            return render_template('/stores/new_store.html',
                                   error_message="Could not accept input as Store data. Please check for invalid data before saving")
        Store(name, url_prefix, tag_name, query).save_to_mongo()
        return redirect(url_for('.index'))

    return render_template('/stores/new_store.html')


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_admin_permissions
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method=='POST':
        try:
            name = request.form['name']
            url_prefix = request.form['url_prefix']
            tag_name = request.form['tag_name']
            query = json.loads(request.form['query'])

            store.name=name
            store.url_prefix= url_prefix
            store.tag_name= tag_name
            store.query = query
            store.save_to_mongo()
        except:
            return render_template('/stores/edit_store.html',
                                   error_message="Could not accept input as Store data. Please check for invalid data before saving", store=store)

        return redirect(url_for('.index'))


    return render_template('/stores/edit_store.html', store=store)

@store_blueprint.route('/delete/<string:store_id>')
@user_decorators.requires_admin_permissions
def delete_store(store_id):
    Store.get_by_id(store_id).delete()
    return redirect(url_for('.index'))

