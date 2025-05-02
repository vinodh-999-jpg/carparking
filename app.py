from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/parking_db"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add-slot', methods=['GET', 'POST'])
def add_slot():
    if request.method == 'POST':
        slot = {
            'slot_number': request.form['slot_number'],
            'floor': request.form['floor'],
            'vehicle_type': request.form['vehicle_type'],
            'occupied': False,
            'amount': int(request.form['amount']),
            'payment_status': request.form['payment_status'],
            'created_at': datetime.now()
        }
        mongo.db.slots.insert_one(slot)
        return redirect(url_for('view_slots'))
    return render_template('add_slot.html')

@app.route('/view-slots')
def view_slots():
    slots = mongo.db.slots.find()
    return render_template('view_slots.html', slots=slots)

@app.route('/toggle-occupy/<slot_id>')
def toggle_occupy(slot_id):
    from bson.objectid import ObjectId
    slot = mongo.db.slots.find_one({'_id': ObjectId(slot_id)})
    mongo.db.slots.update_one({'_id': ObjectId(slot_id)}, {'$set': {'occupied': not slot['occupied']}})
    return redirect(url_for('view_slots'))

if __name__ == '__main__':
    app.run(debug=True)
