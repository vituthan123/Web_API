from fastapi import FastAPI, HTTPException, Request
from getData import get_parentCate_web, get_childCate_web, get_Product_Web

app = FastAPI()

header = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }


@app.get("/CrawData")
async def CrawDataWeb():
    try:

        parent_category = get_parentCate_web(header)
        child_category = get_childCate_web(header)
        product_cate = get_Product_Web(header)

        return {"parent_category":parent_category, "child_category":child_category, "product_cate":product_cate}
    except Exception as e:
        # Nếu có lỗi xảy ra trong quá trình truy vấn, ném HTTPException với mã lỗi 500
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/getParentCate")
async def getParentCate():
    try:
        parent_category = []
        parent_category = get_parentCate_web(header)
        return parent_category
    except Exception as e:
            # Nếu có lỗi xảy ra trong quá trình truy vấn, ném HTTPException với mã lỗi 500
        raise HTTPException(status_code=500, detail=str(e))   

@app.get("/getChildCate")
async def getChildCate():
    try:
        child_category = []
        child_category = get_childCate_web(header)
        return child_category
    except Exception as e:
            # Nếu có lỗi xảy ra trong quá trình truy vấn, ném HTTPException với mã lỗi 500
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/getProduct")
async def getProduct():
    try:
        products = []
        products = get_Product_Web(header)
        return products
    except Exception as e:
            # Nếu có lỗi xảy ra trong quá trình truy vấn, ném HTTPException với mã lỗi 500
        raise HTTPException(status_code=500, detail=str(e))
