from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy in-memory list to simulate products
fake_products = []

@app.route('/')
def home():
    return jsonify({'message': 'Flask app is running on Render without MySQL.'})

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(fake_products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    fake_products.append(data)
    return jsonify({'message': 'Product added'}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
