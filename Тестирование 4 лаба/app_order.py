from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

@app.route('/order')
def order_form():
    return render_template('order_form.html')

@app.route('/submit-order', methods=['POST'])
def submit_order():
    # Получение данных из формы
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()
    comment = request.form.get('comment', '').strip()
    
    # Валидация данных
    errors = {}
    
    if not name:
        errors['name'] = 'Поле "Имя" обязательно для заполнения'
    
    if not email:
        errors['email'] = 'Поле "Email" обязательно для заполнения'
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors['email'] = 'Введите корректный email адрес'
    
    if not phone:
        errors['phone'] = 'Поле "Телефон" обязательно для заполнения'
    elif not re.match(r'^\+?[1-9]\d{1,14}$', phone):
        errors['phone'] = 'Введите корректный номер телефона'
    
    if not address:
        errors['address'] = 'Поле "Адрес" обязательно для заполнения'
    
    if errors:
        return jsonify({'success': False, 'errors': errors})
    
    # Если все данные валидны, возвращаем успешный ответ
    return jsonify({
        'success': True, 
        'message': 'Заказ успешно оформлен! Мы свяжемся с вами в ближайшее время.'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)