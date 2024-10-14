from connection import conn

def save_parentCate_mysql(parentCategory):
    connect = conn()
    if connect.is_connected():
        cursor = connect.cursor()
        try:
            # Lưu trữ dữ liệu vào bảng 'parentCategory'
            for item in parentCategory:
                query = "INSERT IGNORE INTO parentCategory (parentID, cateName, urlKey, iconURL) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (item['parentID'], item['cateName'], item['urlKey'], item['iconURL']))
            # Commit thay đổi vào cơ sở dữ liệu
            connect.commit()
            print("Dữ liệu đã được lưu vào cơ sở dữ liệu thành công!")
        except Exception as e:
            print("Lỗi khi lưu trữ dữ liệu:", e)
            # Rollback nếu có lỗi xảy ra
            connect.rollback()
        finally:
            # Đóng cursor và kết nối
            cursor.close()
            connect.close()
            print("Kết nối đến cơ sở dữ liệu đã được đóng.")


def save_childCate_mysql(childCategory):
    connect = conn()
    if connect.is_connected():
        cursor = connect.cursor()
        try:
            # Lưu trữ dữ liệu vào bảng 'childCategory'
            for item in childCategory:
                query = "INSERT IGNORE INTO childCategory (childID, cateName, urlKey, parentID) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (item['childID'], item['cateName'], item['urlKey'], item['parentID']))
            # Commit thay đổi vào cơ sở dữ liệu
            connect.commit()
            print("Dữ liệu đã được lưu vào cơ sở dữ liệu thành công!")
        except Exception as e:
            print("Lỗi khi lưu trữ dữ liệu:", e)
            # Rollback nếu có lỗi xảy ra
            connect.rollback()
        finally:
            # Đóng cursor và kết nối
            cursor.close()
            connect.close()
            print("Kết nối đến cơ sở dữ liệu đã được đóng.")


def save_product_mysql(products):
    connect = conn()
    if connect.is_connected():
        cursor = connect.cursor()
        try:
            # Lưu trữ dữ liệu vào bảng 'productCate'
            for item in products:
                query = "INSERT IGNORE INTO productCate (productID, productName, price, quantitySold, imgURL, childID, parentID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (item['productID'], item['productName'], item['price'], item['quantitySold'], item['imgURL'], item['childID'], item['parentID']))
            # Commit thay đổi vào cơ sở dữ liệu
            connect.commit()
            print("Dữ liệu đã được lưu vào cơ sở dữ liệu thành công!")
        except Exception as e:
            print("Lỗi khi lưu trữ dữ liệu:", e)
            # Rollback nếu có lỗi xảy ra
            connect.rollback()
        finally:
            # Đóng cursor và kết nối
            cursor.close()
            connect.close()
            print("Kết nối đến cơ sở dữ liệu đã được đóng.")
