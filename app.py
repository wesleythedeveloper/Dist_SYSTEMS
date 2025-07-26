from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db_config = {
    'user': 'flask_user',
    'password': 'flask_password',
    'host': 'host.docker.internal',
    'database': 'inventory_db',
    'port': 3307  # Change to 3307 if you picked a different port during install
}

@app.route('/products', methods=['GET'])
def get_products():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, stock, price) VALUES (%s, %s, %s)",  
                   (data['name'], data['stock'], data['price']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product added'}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
