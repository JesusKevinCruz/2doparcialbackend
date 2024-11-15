from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from collections import OrderedDict

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

class Vehiculo(db.Model):
    __tablename__ = 'vehiculo'
    
    placa = db.Column(db.String(20), primary_key=True)
    color = db.Column(db.String(50))
    modelo = db.Column(db.Integer)
    marca = db.Column(db.String(50))

    def __repr__(self):
        return f"<Vehiculo {self.placa}>"

    def to_dict(self):
        return OrderedDict({
            'placa': self.placa,
            'color': self.color,
            'modelo': self.modelo,
            'marca': self.marca
        })

@app.route('/')
def hello_world():
    return '¡Hola, Mundo!'

@app.route('/api/vehiculo', methods=['GET'])
def get_vehiculos():
    vehiculos = Vehiculo.query.all()  
    vehiculos_dict = [vehiculo.to_dict() for vehiculo in vehiculos]
    print(vehiculos_dict) 
    
    return jsonify({'vehiculos': vehiculos_dict})


@app.route('/api/vehiculo', methods=['POST'])
def create_vehiculo():
    if request.is_json:
        data = request.get_json()  
        
        placa = data.get('placa')
        color = data.get('color')
        modelo = data.get('modelo')
        marca = data.get('marca')
        
        if Vehiculo.query.filter_by(placa=placa).first():
            return jsonify({"error": "El vehículo con esta placa ya existe"}), 400
        
        nuevo_vehiculo = Vehiculo(placa=placa, color=color, modelo=modelo, marca=marca)
        db.session.add(nuevo_vehiculo)
        db.session.commit() 

        return jsonify({"message": "Vehículo creado correctamente"}), 201
    else:
        return jsonify({"error": "La solicitud no contiene JSON"}), 400


@app.route('/api/vehiculo/<placa>', methods=['GET'])
def get_vehiculo_by_placa(placa):
    vehiculo = Vehiculo.query.filter_by(placa=placa).first() 
    if vehiculo:
        return jsonify(vehiculo.to_dict())
    else:
        return jsonify({"error": "Vehículo no encontrado"}), 404

@app.route('/api/vehiculo/<placa>', methods=['PUT'])
def update_vehiculo(placa):
    if request.is_json:
        data = request.get_json()

        vehiculo = Vehiculo.query.filter_by(placa=placa).first()
        if vehiculo:
            vehiculo.color = data.get('color', vehiculo.color)
            vehiculo.modelo = data.get('modelo', vehiculo.modelo)
            vehiculo.marca = data.get('marca', vehiculo.marca)

            db.session.commit()  
            return jsonify({"message": "Vehículo actualizado correctamente"})
        else:
            return jsonify({"error": "Vehículo no encontrado"}), 404
    else:
        return jsonify({"error": "La solicitud no contiene JSON"}), 400


@app.route('/api/vehiculo/<placa>', methods=['DELETE'])
def delete_vehiculo(placa):
    vehiculo = Vehiculo.query.filter_by(placa=placa).first()
    if vehiculo:
        db.session.delete(vehiculo)
        db.session.commit()
        return jsonify({"message": "Vehículo eliminado correctamente"})
    else:
        return jsonify({"error": "Vehículo no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
