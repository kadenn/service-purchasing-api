from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///offers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), unique=True)
    when = db.Column(db.String(80))
    where = db.Column(db.String(80))
    note = db.Column(db.String(80))

    def __init__(self, category, when, where, note):
        self.category = category
        self.when = when
        self.where = where
        self.note = note


class OfferSchema(ma.Schema):
    class Meta:
        fields = ('id', 'category', 'when', 'where', 'note')


offer_schema = OfferSchema()
offers_schema = OfferSchema(many=True)


class OfferManager(Resource):
    @staticmethod
    def get():
        try:
            id = request.args['id']
        except Exception as _:
            id = None

        if not id:
            offers = Offer.query.all()
            return jsonify(offers_schema.dump(offers))
        offer = Offer.query.get(id)

        response = jsonify(offer_schema.dump(offer))

        return response

    @staticmethod
    def post():
        category = request.json['category']
        when = request.json['when']
        where = request.json['where']
        note = request.json['note']

        offer = Offer(category, when, where, note)
        db.session.add(offer)
        db.session.commit()

        response = jsonify({'Message': f'New Offer insterted to database.'})

        return response

    @staticmethod
    def delete():
        try:
            id = request.args['id']
        except Exception as _:
            id = None

        if not id:
            last_offer = db.session.query(
                Offer).order_by(Offer.id.desc()).first()
            db.session.delete(last_offer)
            db.session.commit()
            return jsonify({'Message': f'Last offer deleted.'})

        offer = Offer.query.get(id)
        db.session.delete(offer)
        db.session.commit()
        return jsonify({'Message': f'Offer {str(id)} deleted.'})


api.add_resource(OfferManager, '/api/offers')

if __name__ == '__main__':
    app.run(debug=True)

# Command to start server: python3 app.py
