from fastapi import HTTPException
from connection import conn
import math

def get_parentCate_DB():
    try:
        connect = conn()
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM parentCategory")
            
            parent_categorys = cursor.fetchall()  # Lấy tất cả các dòng dữ liệu từ truy vấn
            list_cate_parent = []
            for item in parent_categorys:
                parent_cate_dict = {
                    "parentID": item[0],
                    "cateName": item[1],
                    "urlKey": item[2],
                    "iconURL": item[3]
                }
                list_cate_parent.append(parent_cate_dict)
            
            return list_cate_parent
    except Exception as e:
        # Nếu có lỗi xảy ra trong quá trình truy vấn, ném HTTPException với mã lỗi 500
        raise HTTPException(status_code=500, detail=str(e))


def get_childCate_DB(parentID):
    try:
        connect = conn()
        with connect.cursor() as cursor:
            cursor.execute("SELECT * FROM childCategory WHERE parentID = %s" % parentID)
            
            child_categorys = cursor.fetchall()  # Lấy tất cả các dòng dữ liệu từ truy vấn
            list_cate_child = []
            for item in child_categorys:
                child_cate_dict = {
                    "childID": item[0],
                    "cateName": item[1],
                    "urlKey": item[2],
                    "parentID": item[3],
                }
                list_cate_child.append(child_cate_dict)
            
            return list_cate_child
    except Exception as e:
        # Nếu có lỗi xảy ra trong quá trình truy vấn, ném HTTPException với mã lỗi 500
        raise HTTPException(status_code=500, detail=str(e))

def get_ProductAll_DB(page: int = 1, page_size: int = 10):
    try:
        connect = conn()
        with connect.cursor() as cursor:
            cursor.execute("SELECT productID, productName, price, quantitySold, imgURL FROM productCate")
            
            products = cursor.fetchall()  # Lấy tất cả các dòng dữ liệu từ truy vấn
            list_productAll = []
            for item in products:
                product_dict = {
                    "productID": item[0],
                    "productName": item[1],
                    "price": item[2],
                    "quantitySold": item[3],
                    "imgURL": item[4]
                }
                list_productAll.append(product_dict)
            total_page = math.ceil((len(list_productAll) / page_size))
            start_row_index = (page - 1) * page_size
            
            return list_productAll[start_row_index:start_row_index + page_size], total_page
            # return list_product
    except Exception as e:
        # Nếu có lỗi xảy ra trong quá trình truy vấn, ném HTTPException với mã lỗi 500
        raise HTTPException(status_code=500, detail=str(e))



def get_ProductCateParent_DB(parentID, page: int = 1, page_size: int = 10):
    try:
        connect = conn()
        with connect.cursor() as cursor:
            cursor.execute("SELECT productID, productName, price, quantitySold, imgURL FROM productCate WHERE parentID = %s" % parentID)
            
            products = cursor.fetchall()  # Lấy tất cả các dòng dữ liệu từ truy vấn
            list_productCate = []
            for item in products:
                product_dict = {
                    "productID": item[0],
                    "productName": item[1],
                    "price": item[2],
                    "quantitySold": item[3],
                    "imgURL": item[4]
                }
                list_productCate.append(product_dict)
            total_page = math.ceil((len(list_productCate) / page_size))
            start_row_index = (page - 1) * page_size
            
            return list_productCate[start_row_index:start_row_index + page_size], total_page
    except Exception as e:
        # Nếu có lỗi xảy ra trong quá trình truy vấn, ném HTTPException với mã lỗi 500
        raise HTTPException(status_code=500, detail=str(e))
    


def get_ProductCateChild_DB(childID, page: int = 1, page_size: int = 9):
    try:
        connect = conn()
        with connect.cursor() as cursor:
            cursor.execute("SELECT productID, productName, price, quantitySold, imgURL FROM productCate WHERE childID = %s" % childID)
            
            products = cursor.fetchall()  # Lấy tất cả các dòng dữ liệu từ truy vấn
            list_productChildCate = []
            for item in products:
                product_dict = {
                    "productID": item[0],
                    "productName": item[1],
                    "price": item[2],
                    "quantitySold": item[3],
                    "imgURL": item[4]
                }
                list_productChildCate.append(product_dict)
            total_page = math.ceil((len(list_productChildCate) / page_size))
            start_row_index = (page - 1) * page_size
            
            return list_productChildCate[start_row_index:start_row_index + page_size], total_page
    except Exception as e:
        # Nếu có lỗi xảy ra trong quá trình truy vấn, ném HTTPException với mã lỗi 500
        raise HTTPException(status_code=500, detail=str(e))
    

def get_Product_Search(key: str, page: int = 1, page_size: int = 10):
    try:
        connect = conn()
        with connect.cursor() as cursor:
            cursor.execute("SELECT productID, productName, price, quantitySold, imgURL FROM productCate WHERE productName LIKE %s", (key + '%',))

            products = cursor.fetchall()  # Lấy tất cả các dòng dữ liệu từ truy vấn
            list_productSearch = []
            for item in products:
                product_dict = {
                    "productID": item[0],
                    "productName": item[1],
                    "price": item[2],
                    "quantitySold": item[3],
                    "imgURL": item[4]
                }
                list_productSearch.append(product_dict)
            total_page = math.ceil((len(list_productSearch) / page_size))
            start_row_index = (page - 1) * page_size
            
            return list_productSearch[start_row_index:start_row_index + page_size], total_page
    except Exception as e:
        # Nếu có lỗi xảy ra trong quá trình truy vấn, ném HTTPException với mã lỗi 500
        raise HTTPException(status_code=500, detail=str(e))