#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return make_response(earthquake.to_dict(), 200)
    return make_response({'message': 'Earthquake 9999 not found.'}, 404)

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquake_magnitude(magnitude):
    quakes = db.session.query(Earthquake).filter(Earthquake.magnitude >= magnitude).all()
    quakes_list = [quake.to_dict() for quake in quakes]
    if quakes:
        return make_response(
        {
            'count': len(quakes),
            'quakes': quakes_list
        }, 
        200
    )

    return make_response({'count': 0, 'quakes': []}, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
