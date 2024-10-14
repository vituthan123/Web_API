import requests
from unidecode import unidecode
import re
import multiprocessing

def get_parentCate_web(header):
    url = 'https://api.tiki.vn/raiden/v2/menu-config?platform=desktop'
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        try:
            data = response.json()
            menu_block = data.get("menu_block", {})
            items = menu_block.get("items", [])
            category_parent = []
            for item in items:
                parent_ID = item.get("link", "").split("/")[-1][1:] 
                category_Name = item.get("text", "")
                edit_url_Key = re.sub(r'[^\w\s]', '', unidecode(category_Name).lower())
                url_Key = re.sub(r'[-\s]+', '-', edit_url_Key)
                icon_URL = item.get("icon_url", "")
                category_parent.append({
                    "parentID": parent_ID,
                    "cateName": category_Name,
                    "urlKey": url_Key,
                    "iconURL": icon_URL
                })
            return category_parent
        except Exception as e:
            print("Đã xảy ra lỗi khi xử lý JSON:", e)
            return None
    else:
        print("Không thể tìm nạp dữ liệu từ URL được cung cấp.")


def get_childCate_web(header):
    #Lấy ID của danh mục cha
    list_parentID = []
    parentCate = get_parentCate_web(header)
    for item in parentCate:
        list_parentID.append(item["parentID"])
    all_category_child = []
    
    for parentID in list_parentID:
        url = f'https://tiki.vn/api/v2/categories?parent_id={parentID}'
        response = requests.get(url, headers=header)
        
        if response.status_code == 200:
            try:
                data = response.json()
                items = data.get("data", [])
                category_child = []
                for item in items:
                    childID = item.get("id", "")
                    cateName = item.get("name", "")
                    urlKey = item.get("url_key", "")
                    category_child.append({
                        "childID": childID,
                        "cateName": cateName,
                        "urlKey": urlKey,
                        "parentID": parentID
                    })
                all_category_child.extend(category_child)
            except Exception as e:
                print(f"Đã xảy ra lỗi khi xử lý JSON cho parentID {parentID}:", e)
        else:
            print(f"Không thể tìm nạp dữ liệu từ URL cho parentID {parentID}.")
    return all_category_child



def getID_Cate(header):
    # Lấy ID của danh mục
    list_cate = []
    all_cate = get_childCate_web(header)

    for item in all_cate:
        list_item = {"cateID":item["childID"], "urlKey":item["urlKey"], "childID":item["childID"], "parentID":item["parentID"]}
        list_cate.append(list_item)
    return list_cate

def scrape_product(url, header, childID, parentID, all_product):
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        try:
            data = response.json()
            items = data.get("data", [])
            productID_seen = set()
            for item in items:
                productID = item.get("id", "")
                if productID in productID_seen:
                    continue # Nếu sản phẩm đã tồn tại, bỏ qua sản phẩm này
                else:
                    productID_seen.add(productID)
                productName = item.get("name", "")
                price = item.get("price", "")
                quantitySold_value = item.get("quantity_sold", {})
                quantitySold = quantitySold_value.get("value", "")
                imgURL = item.get("thumbnail_url", "")
                all_product.append({
                    "productID": productID,
                    "productName": productName,
                    "price": price,
                    "quantitySold": quantitySold,
                    "imgURL": imgURL,
                    "childID": childID,
                    "parentID": parentID
                })
                
        except Exception as e:
            print(f"Đã xảy ra lỗi khi xử lý JSON cho URL {url}: {e}")
    else:
        print(f"Không thể tìm nạp dữ liệu từ URL {url}.")

def get_Product_Web(header):
    #Lấy ID của danh mục cha
    list_cate = []
    list_cate = getID_Cate(header)
    
    all_product = multiprocessing.Manager().list()

    processes = []
    for cate in list_cate:
        cateID = cate['cateID']
        urlKey = cate['urlKey']
        childID = cate['childID']
        parentID = cate['parentID']
        url = f"https://tiki.vn/api/personalish/v1/blocks/listings?limit=10&include=advertisement&aggregations=2&version=home-persionalized" \
            f"&trackity_id=47d1d1db-6b05-d442-2aad-6d68de94ddae" \
            f"&category={cateID}" \
            f"&page=1" \
            f"&urlKey={urlKey}"

        process = multiprocessing.Process(target=scrape_product, args=(url, header, childID, parentID, all_product))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return list(all_product)

