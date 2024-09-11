from flask import Flask, jsonify, make_response, request
from backend.orders import order_bp
from monitor.monitor import monitor_bp
app = Flask(__name__)

app.register_blueprint(order_bp)
app.register_blueprint(monitor_bp)

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)
