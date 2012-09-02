import xlrd
from xlutils.copy import copy
import json
import uuid
import shutil
import os
import datetime
import html_and_pdf_funcs

offer_xls_dict = "offer_xls_mapping.json"
docs_path = "/home/kittugadu/jef-poc/"
master_xls_name = 'master calc UPS.xls'
xls_path = docs_path + master_xls_name
customers_json_file = 'customers.json'
offer_doc_name = "offer.xls"
product_quantity_col = 5

def say_hello_world():
    return 'Hello, World!!!'

def open_xls_file(xls_file_path):
    wb = xlrd.open_workbook(xls_file_path)
    return wb

def get_xls_sheet(wb,name="default"):
    if name=='default':
        return wb.sheet_by_index(0)
    else:
        return wb.sheet_by_name(name)

def get_products():
    products = get_products_json(get_products_list(xls_path))
    return json.dumps(products)

def get_products_list(xls_path):
    wb = open_xls_file(xls_path)
    sh = get_xls_sheet(wb)
    products = {}
    for aRow in range(8,161):
        xls_prd_row = sh.row_values(aRow)
        if xls_prd_row[1] != '':
            products[aRow] = xls_prd_row
    return products

def get_unit_price(product_row):
    pass


def get_products_json(products):
    products_json = []
    for keys in products:
        product_row = products.get(keys)
        aProduct = {'id': keys, 'name': product_row[1], 
                'company': product_row[2], 'unit_price': get_unit_price(product_row)}
        products_json.append(aProduct)
    return products_json

def _offer(offer_json):
    if not offer_json('id'):
        new_offer(offer_json)
    else:
        update_offer(offer_json)


def new_offer(offer_json):
    offer_uuid = str(uuid.uuid1())
    offer_id = offer_json.get('id')
    customer_id = offer_json.get('customer_id')
    offer_desc = offer_json.get('offer_desc')
    additional_info = offer_json.get('additional_info')
    products = offer_json.get('products')
    offer_desc = offer_json.get('desc')
    print customer_id, additional_info, offer_desc
    for product in products:
        id = product.get('id')
        quantity = product.get('quantity')
        print id, quantity
    path =  save_offer(customer_id, offer_id, additional_info, products, offer_desc)
    add_to_offer_path_mapping(path, offer_uuid)
    return path

def add_to_offer_path_mapping(path, offer_uuid):
    mapping = json.load(open(offer_xls_dict))
    mapping.append({'uuid': offer_uuid, 'path': path})
    open(offer_xls_dict,'w').write(json.dumps(mapping))

def update_offer(offer_json):
    pass


def copy_master_xls(dest_xls_path):
    if not os.path.exists(dest_xls_path):
        os.makedirs(dest_xls_path)
    shutil.copy2(xls_path, dest_xls_path + master_xls_name)

def save_offer(customer_id, offer_id, products, additional_info, offer_desc):
    #number-customer_name-date
    now = datetime.datetime.now()
    dest_path = offer_id + getCustomerName(customer_id) +  now.strftime("%Y_%b_%d_%H_%M")
    copy_master_xls(docs_path + dest_path)
    write_to_offer_xls(docs_path + dest_path, products)
    write_offer_pdf(docs_path + dest_path, products, customer_id, additional_info, offer_desc, offer_id)
    return docs_path+dest_path



def write_to_offer_xls(offer_xls_path, products):
    fixed_master_xls = offer_xls_path + master_xls_name
    wb = open_xls_file(fixed_master_xls)
    w = copy(wb)
    sh = w.get_sheet(0)
    for product in products:
        row_id = product.get('id')
        quantity = product.get('quantity')
        sh.write(row_id, product_quantity_col, int(quantity))
    w.save(offer_xls_path + offer_doc_name)

def write_offer_pdf(docs_path, products,customer_id, additional_info, offer_desc, offer_id):
    customer_name = getCustomerName(customer_id)
    customer_address = getCustomerAddress(customer_id)
    html_and_pdf_funcs.write_offer_pdf(docs_path, offer_id, customer_name, customer_address, offer_desc, additional_info, products)


def getCustomerName(id):
    customer_list = json.load(open(customers_json_file))
    customer = ''
    for aCustomer in customer_list:
        if aCustomer.get('id') == id:
            customer = aCustomer
    return customer.get('name').replace(" ","_")

def getCustomerAddress(id):
    customer_list = json.load(open(customers_json_file))
    customer = ''
    for aCustomer in customer_list:
        if aCustomer.get('id') == id:
            customer = aCustomer
    return customer.get('address')
