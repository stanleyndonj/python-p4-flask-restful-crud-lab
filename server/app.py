#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize database and migration
migrate = Migrate(app, db)
db.init_app(app)

# Initialize API
api = Api(app)

# Define the Plants resource
class Plants(Resource):
    def get(self):
        # Get all plants
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        # Create a new plant
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)

# Add the Plants resource to the API
api.add_resource(Plants, '/plants')

# Define the PlantByID resource
class PlantByID(Resource):
    def get(self, id):
        # Get plant by ID
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            return make_response(jsonify(plant.to_dict()), 200)
        return make_response({'error': 'Plant not found'}, 404)

    def patch(self, id):
        # Update plant details by ID
        data = request.get_json()
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            for attr in data:
                setattr(plant, attr, data[attr])
            db.session.add(plant)
            db.session.commit()
            return make_response(plant.to_dict(), 200)
        return make_response({'error': 'Plant not found'}, 404)

    def delete(self, id):
        # Delete plant by ID
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            db.session.delete(plant)
            db.session.commit()
            return make_response('', 204)
        return make_response({'error': 'Plant not found'}, 404)

# Add the PlantByID resource to the API
api.add_resource(PlantByID, '/plants/<int:id>')

# Run the app
if __name__ == '__main__':
    app.run(port=5555, debug=True)
