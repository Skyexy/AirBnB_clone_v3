#!/usr/bin/python3
"""
New view for State objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort
from api.v1.views import app_views
from models import storage


@app_views.route('/api/v1/states', strict_slashes=False)
def all_states():
    """ retrieve list of all State objects """
    all_states = []
    for state in storage.all('State').values():
        all_states.append(state.to_dict())
    return jsonify(all_states)

@app_views.route('/api/v1/states/<state_id>', strict_slashes=False)
def retrieve_state(state_id):
    """ retrieve a particular State """
    try:
        state = jsonify(storage.get('State', state_id).to_dict())
        return state
    except:
        abort(404)

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete a State """
    state = storage.get('State', state_id)
    if state:
        state.delete()
        storage.save()
        return {}
    abort(404)

@app_views.route('/api/v1/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """ create a State """
    
