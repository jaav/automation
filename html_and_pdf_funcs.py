from xhtml2pdf import pisa
from cStringIO import StringIO
import datetime

def publish_pdf(html_string, dest_path, pdf_name="offer.pdf"):
    pisa.pisaDocument(StringIO(html_string),file(dest_path+pdf_name,'wb'))

##{{offer_id}}
##{{offer_date}}
##{{offer_desc}}
##{{customer_name}}
##{{customer_address}}
##{{item_table}}
##{additional_info}}

def get_html_template():
    return open('invoice.template').read()

def write_offer_pdf(dest_path,offer_id, customer_name, customer_address, offer_desc, additional_info, products):
    html_string = get_html_template()
    now = datetime.datetime.now();offer_date = now.strftime('%Y-%b-%d')
    html_string.replace('{{offer_id}}',offer_id)
    html_string.replace('{{offer_date}}',offer_date)
    html_string.replace('{{offer_desc}}',offer_desc)
    html_string.replace('{{customer_name}}',customer_name)
    html_string.replace('{{customer_address}}',customer_address)
    html_string.replace('{{item_table}}',get_items_table(products))
    html_string.replace('{{additional_info}}',additional_info)
    publish_pdf(html_string,dest_path)

def get_items_table(products):
    items_table = ''
    for product in products:
        unit_price = product.get('unit_price')
        total_price = int(product.get('quantity')) * unit_price
        items_table += '<tr class="odd">'
        items_table += '<td>' + product.get('name') + '</td>'
        items_table += '<td>' + product.get('quantity') + '</td>'
        items_table += '<td>' + unit_price + '</td>'
        items_table += '<td>' + total_price + '</td>'
        items_table += '</tr>'
    return items_table
