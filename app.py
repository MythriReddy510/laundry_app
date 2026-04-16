from flask import Flask, request, jsonify

app = Flask(__name__)

orders = []
order_id_counter = 1

@app.route('/')
def home():
    return "Laundry API Running"



@app.route('/create_order', methods=['POST'])
def create_order():
    global order_id_counter

    data = request.json

    customer_name = data['customer_name']
    phone = data['phone']
    garments = data['garments']

    total = 0
    for item in garments:
        total += item['quantity'] * item['price']

    order = {
        "order_id": order_id_counter,
        "customer_name": customer_name,
        "phone": phone,
        "garments": garments,
        "total": total,
        "status": "RECEIVED"
    }

    orders.append(order)
    order_id_counter += 1

    return jsonify(order)

@app.route('/update_status/<int:order_id>', methods=['PUT'])
def update_status(order_id):
    data = request.json
    new_status = data['status']

    for order in orders:
        if order['order_id'] == order_id:
            order['status'] = new_status
            return jsonify(order)

    return jsonify({"message": "Order not found"})

@app.route('/orders', methods=['GET'])
def get_orders():
    status = request.args.get('status')
    phone = request.args.get('phone')

    result = orders

    if status:
        result = [o for o in result if o['status'] == status]

    if phone:
        result = [o for o in result if o['phone'] == phone]

    return jsonify(result)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    total_orders = len(orders)
    total_revenue = sum(o['total'] for o in orders)

    status_count = {}
    for o in orders:
        status = o['status']
        status_count[status] = status_count.get(status, 0) + 1

    return jsonify({
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "orders_per_status": status_count
    })




if __name__ == '__main__':
    app.run(debug=True)