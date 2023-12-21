from app import app, render_template, text, engine, request, Response
import pdfkit
import os
from datetime import datetime


@app.route('/pos')
def pos_index():
    return render_template('pos_screen.html')


@app.route("/pdf")
def index_pdf():
    directory = os.path.join(os.getcwd(), 'pdf')

    file_path = os.path.join(directory, 'invoice.pdf')

    data = [
        {'id': 1, 'name': 'កូកាកូឡា', 'qty': 20, 'price': 0.25},
        {'id': 1, 'name': 'sting', 'qty': 10, 'price': 0.25},
        {'id': 1, 'name': 'abc', 'qty': 3, 'price': 25},
        {'id': 1, 'name': 'Anchor', 'qty': 6, 'price': 25},
        {'id': 1, 'name': 'KRUD', 'qty': 4, 'price': 25},
        {'id': 1, 'name': 'VATANAK', 'qty': 1, 'price': 25},
        {'id': 1, 'name': 'DRAGON', 'qty': 2, 'price': 25},
    ]
    now = datetime.now()
    created_at = now.strftime("%Y-%m-%d %H:%M")
    server_url = request.url_root
    html = render_template("invoice.html", data=data,
                           now=created_at, server_url=server_url)
    options = {
        'page-height': '8.3in',
        'page-width': '5.8in',
        'margin-top': '0.1in',
        'margin-right': '0in',
        'margin-bottom': '0.1in',
        'margin-left': '0in',
    }

    config = pdfkit.configuration(
        wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    pdf = pdfkit.from_string(
        html, file_path, options, configuration=config)
    pdf_preview = pdfkit.from_string(
        html, '', options, configuration=config)
    return Response(pdf_preview, mimetype="application/pdf")


# @app.route('/pos/create_transaction', methods=['post'])
# def create_transaction():
#     total_price = request.form.get('total_price')
#     received_amount = request.form.get('received_amount')
#     selected_product = request.form.get('selected_product')

#     # insert sale transaction
#     result = connection.execute(
#         text("INSERT INTO sale (date, customer_id) VALUES ('2023-12-16', 1)"))
#     sale_id = result.lastrowid
#     connection.commit()
#     return '12'


@app.route('/getAllProduct')
def getAllProduct():
    try:
        con = engine.connect()

        products = con.execute(text(
            'SELECT product.*, category.* FROM product JOIN category ON product.category_id = category.category_id ;'))
        categories = con.execute(text('SELECT * from category;'))
        con.commit()
        category_list = [{'id': category.category_id,
                          'name': category.category_name} for category in categories]

        product_list = []
        for product in products:
            product_list.append(
                {
                    'id': product.product_id,
                    'name': product.product_name,
                    'discount': product.discount,
                    'price': product.price,
                    'image': product.image,
                    'category_name': product.category_name,
                    'category_id': product.category_id,
                }
            )

        result = [
            product_list,
            category_list
        ]

        return result

    finally:
        con.close()