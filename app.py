from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

# MySQL config using environment variables (for Railway)
db_config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'database': os.environ['DB_NAME'],
    'port': int(os.environ.get('DB_PORT', 3306))
}

@app.route('/')
def home():
    return jsonify({"message": "Inventory API is running. Use /products to GET or POST data."})

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
    data = request.get_json()
    try:
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
