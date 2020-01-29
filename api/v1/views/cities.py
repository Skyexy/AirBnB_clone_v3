#!/usr/bin/python3
"""
New view for City objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/api/v1/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    """ retrieve list of all City objects of State"""
    all_cities = []
    for city in storage.all('City').values():
        if state_id == city.state_id:
            all_cities.append(city.to_dict())
    if not all_cities:
        abort(404)
    return jsonify(all_cities)


@app_views.route('/api/v1/cities/<city_id>', strict_slashes=False)
def retrieve_city(city_id):
    """ retrieve a particular City """
    try:
        city = jsonify(storage.get('City', city_id).to_dict())
        return city
    except:
        abort(404)


@app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ delete a City """
    city = storage.get('City', city_id)
    if city:
        city.delete()
        storage.save()
        return {}
    abort(404)


@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_cities(state_id):
    """ create a City """
    city_name = request.get_json()
    if not city_name:
        abort(400, {'Not a JSON'})
    elif 'name' not in city_name:
        abort(400, {'Missing name'})
    try:
        state = jsonify(storage.get('State', state_id).to_dict())
    except:
        abort(404)
    city_name['state_id'] = state_id
    new_city = City(**city_name)
    storage.new(new_city)
    storage.save()
    return new_city.to_dict(), 201


@app_views.route('/api/v1/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ update a City """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_city = storage.get('City', city_id)
    if not my_city:
        abort(404)
    for key, value in update_attr.items():
        setattr(my_city, key, value)
    storage.save()
    return my_city.to_dict()
