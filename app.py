from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Railway MySQL Configuration
db_config = {
    'user': 'root',
    'password': 'AFRhgoCCClytMTILFIMAUPYXhCZkWXIu',
    'host': 'maglev.proxy.rlwy.net',
    'database': 'railway',
    'port': 31418
}

@app.route('/')
def home():
    return "<h2>✅ Welcome to the Inventory API!</h2><p>Use <code>/products</code> to GET or POST product data.</p>"

@app.route('/products', methods=['GET'])
def get_products():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, stock, price) VALUES (%s, %s, %s)",
            (data['name'], data['stock'], data['price'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Product added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
