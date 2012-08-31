import xlrd
import json

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

def get_products_list(xls_path):
    wb = open_xls_file(xls_path)
    sh = get_xls_sheet(wb)
    products = {}
    for aRow in range(8,161):
        xls_prd_row = sh.row_values(aRow)
        if xls_prd_row[1] != '':
            products[aRow] = xls_prd_row
    return products

def get_products_json(products):
    products_json = []
    for keys in products:
        product_row = products.get(keys)
        aProduct = {'id': keys, 'name': product_row[1], 'company': product_row[2]}
        products_json.append(aProduct)
    return products_json

xls_path = '/home/kittugadu/jef-poc/master calc UPS.xls'
