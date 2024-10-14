
import schedule
import requests
import time
import threading
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


from savetoDB import *
from getDataDB import *

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Địa chỉ của trang web
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)
header = {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }


@app.get("/CrawToDB")
def CrawToDB():
    try:
        # Gửi yêu cầu GET để lấy dữ liệu
        response = requests.get("http://6.6.0.3:5555/CrawData", headers=header)
        # Kiểm tra xem yêu cầu đã được xử lý thành công hay không
        if response.status_code == 200:
            # Truy cập vào dữ liệu JSON từ phản hồi HTTP
            data = response.json()
            parent_category = data['parent_category']
            child_category = data['child_category']
            product_cate = data['product_cate']
            # Lưu dữ liệu danh mục cha vào cơ sở dữ liệu
            save_parentCate_mysql(parent_category)
            save_childCate_mysql(child_category)
            save_product_mysql(product_cate)
            return {"Message": "Dữ liệu đã được lưu vào cơ sở dữ liệu thành công!"}
        else:
            # Nếu yêu cầu không thành công, ném một HTTPException với mã lỗi tương ứng
            raise HTTPException(status_code=response.status_code, detail="Yêu cầu không thành công: " + str(response.status_code))
    except Exception as e:
        # Nếu có bất kỳ lỗi nào xảy ra, ném một HTTPException với mã lỗi 500 và chi tiết lỗi
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/productCateAll")
async def productCateAll(page: int = 1, page_size: int = 10):
    try:
        # Lấy danh mục cha từ DB
        parentCate_DB = get_parentCate_DB()
        # Lấy tất cả sản phẩm
        productAll_DB, total_page = get_ProductAll_DB(page, page_size)
        
        # Tạo dictionary chứa dữ liệu muốn trả về
        response_data = {
            "parentCate": parentCate_DB, 
            "products": productAll_DB, 
            "index_page": page, 
            "total_page": total_page
        }
        
        # Trả về response JSON
        return JSONResponse(content=response_data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.get("/productParentCate")
async def productParentCate(parentID: int, page: int = 1, page_size: int = 10):
    try:
        cate_childs = get_childCate_DB(parentID)
        productParentCates, total_page = get_ProductCateParent_DB(parentID, page, page_size)
        
        # Tạo dictionary chứa dữ liệu muốn trả về
        response_data = {
            "childCate": cate_childs, 
            "products": productParentCates, 
            "parentID": parentID,
            "index_page": page, 
            "total_page": total_page
        }
        
        # Trả về response JSON
        return JSONResponse(content=response_data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

@app.get("/productChildCate")
def productCateChild(childID: int, page: int = 1, page_size: int = 10):
    try:
        #Lấy dữ liệu từ DB
        # cate_childs = get_childCate_DB(parentID)
        productChildCates, total_page = get_ProductCateChild_DB(childID, page, page_size)
        response_data = {
            # "childCate": cate_childs, 
            "products": productChildCates, 
            # "parentID": parentID,
            "childID": childID,
            "index_page": page, 
            "total_page": total_page
        }
        
        # Trả về response JSON
        return JSONResponse(content=response_data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.get("/productSearch")
async def productSearch(key:str, page: int = 1, page_size: int = 10):
    try:
        
        #Lấy danh mục cha từ DB
        parentCate_DB = get_parentCate_DB()
        productSearchs, total_page = get_Product_Search(key, page, page_size)
        response_data = {
            "parentCate": parentCate_DB, 
            "products": productSearchs, 
            "index_page": page, 
            "total_page": total_page
        }
        
        # Trả về response JSON
        return JSONResponse(content=response_data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


# @app.get("/CrawAuto")
def auto_craw():
    # Thiết lập công việc để chạy tự động
    
    # schedule.every(60).seconds.do(CrawToDB)
    schedule.every(2).minutes.do(CrawToDB)
    # schedule.every(2).hours.do(CrawToDB)
    # schedule.every().day.at("03:35 PM").do(CrawToDB)

    # Vòng lặp để duy trì chương trình chạy và kiểm tra lịch trình
    while True:
        schedule.run_pending()
        time.sleep(1)  # Chờ 10 giây trước khi kiểm tra lịch trình tiếp theo

# Bắt đầu lập lịch chạy công việc
def start_scheduler():
    print("Tự động cào dữ liệu...")
    auto_craw()

# Lần đầu tiên khởi động lập lịch khi ứng dụng bắt đầu
start_scheduler_thread = threading.Thread(target=start_scheduler)
start_scheduler_thread.start()
            