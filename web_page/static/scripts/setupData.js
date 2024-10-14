const header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

async function updateIndexPage(parentID, childID, key, page, page_size) {
    try {
        const url = `http://localhost:9000/productSearch?key=${key}&page=${page}&page_size=${page_size}`;
        const response = await fetch(url, {
            method: 'GET',
            headers: header
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const page_index = data.page_index;
        
        eventSearch(page_index);
        setPage(parentID, childID, key, page_index);
    }
    catch (error){
        console.error(error);
    }
}
async function setChildCate(parentID, page, page_size) {
    try {
        // const data = await getDataDB(page, page_size);
        const url = `http://localhost:9000/productParentCate?parentID=${parentID}&page=${page}&page_size=${page_size}`;
        const response = await fetch(url, {
            method: 'GET',
            headers: header
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const categoryList = document.getElementById("category-list");

        // Xóa các phần tử con cũ trong danh sách trước khi thêm mới
        categoryList.innerHTML = "";

        // Duyệt qua mảng các danh mục và tạo các phần tử HTML tương ứng
        data.childCate.forEach(category => {
            const categoryLink = document.createElement("a");

            const categoryName = document.createElement("li");
            categoryName.className = "name-cate";
            categoryName.textContent = category.cateName;
            categoryName.title = category.cateName;

            // Thêm tên của danh mục vào thẻ a
            categoryLink.appendChild(categoryName);

            categoryLink.addEventListener("click", async function(event){
                setChildCate(category.parentID, page, 10);
                setproductAll(category.parentID, category.childID, '', page, 10);
                setPage(category.parentID, category.childID, '', page);
                refreshSearch();
                setTitleProduct(category.cateName);
            });

            // Tạo một phần tử div mới để chứa a
            const categoryItem = document.createElement("div");
            categoryItem.className = "item-content-cate";
            categoryItem.appendChild(categoryLink);

            // Thêm phần tử div mới vào danh sách danh mục
            categoryList.appendChild(categoryLink);
        });
    } catch (error) {
        console.error(error);
    }
}

async function setParentCate(key, page, page_size) {
    try {
        // const data = await getDataDB(page, page_size);
        const url = `http://localhost:9000/productSearch?key=${key}&page=${page}&page_size=${page_size}`;
        const response = await fetch(url, {
            method: 'GET',
            headers: header
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const categoryList = document.getElementById("category-list");

        // Xóa các phần tử con cũ trong danh sách trước khi thêm mới
        categoryList.innerHTML = "";

        // Duyệt qua mảng các danh mục và tạo các phần tử HTML tương ứng
        data.parentCate.forEach(category => {
            const categoryLink = document.createElement("a");

            const categoryImage = document.createElement("img");
            categoryImage.className = "image-cate";
            categoryImage.src = category.iconURL;
            categoryImage.alt = category.cateName;

            const categoryName = document.createElement("li");
            categoryName.className = "name-cate";
            categoryName.textContent = category.cateName;
            categoryName.title = category.cateName;

            // Thêm ảnh và tên của danh mục vào thẻ a
            categoryLink.appendChild(categoryImage);
            categoryLink.appendChild(categoryName);
            categoryLink.addEventListener("click", async function(event){
              setChildCate(category.parentID, page, 10);
              setproductAll(category.parentID, category.childID, key, page, 10);
              setPage(category.parentID, category.childID, key, page);
              refreshSearch();
              setTitleProduct(category.cateName);
            });


            // Tạo một phần tử div mới để chứa a
            const categoryItem = document.createElement("div");
            categoryItem.className = "item-content-cate";
            categoryItem.appendChild(categoryLink);

            // Thêm phần tử div mới vào danh sách danh mục
            categoryList.appendChild(categoryLink);
        });
    } catch (error) {
        console.error(error);
    }
}
function setTitleProduct(cateName){
    const title = document.getElementById("title-product");
    title.textContent = cateName;
}
function refreshSearch(){
    const input_search = document.getElementById("input-search");
    input_search.value  = '';
}
function formatQuantity(quantity) {
    if (quantity >= 1000) {
        return (quantity / 1000).toFixed(1) + 'k';
    } else {
        return quantity.toString();
    }
}

async function setproductAll(parentID, childID, key, page, page_size) {
    try {
        let url;
        // const data = getDataDB(page, page_size)
        if (parentID == null){
            url = `http://localhost:9000/productSearch?key=${key}&page=${page}&page_size=${page_size}`;
        }
        else{
            if (childID == null){
                url = `http://localhost:9000/productParentCate?parentID=${parentID}&page=${page}&page_size=${page_size}`;
            }
          else{
                url = `http://localhost:9000/productChildCate?childID=${childID}&page=${page}&page_size=${page_size}`;
            }
        }
        const response = await fetch(url, {
            method: 'GET',
            headers: header
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const productList = document.getElementById("item-product");
        productList.innerHTML = "";
        
        data.products.forEach(product => {
            const productBox = document.createElement("div");
            productBox.className = "item-box-product";

            const boxImg = document.createElement("div");
            boxImg.className = "box-img";
            const img = document.createElement("img");
            img.src = product.imgURL;
            img.alt = product.productName;
            img.style.width = "200px";
            img.style.height = "200px";
            boxImg.appendChild(img);

            const contentBox = document.createElement("div");
            contentBox.className = "content-box";

            const boxLabel = document.createElement("div");
            boxLabel.className = "box-label";
            const labelImg = document.createElement("img");
            labelImg.src = "/static/images/label-real.png";
            labelImg.alt = product.productName;
            labelImg.style.width = "89px";
            labelImg.style.height = "20px";
            boxLabel.appendChild(labelImg);

            const boxName = document.createElement("div");
            boxName.className = "box-name";
            const h3 = document.createElement("h3");
            h3.textContent = product.productName;
            boxName.appendChild(h3);

            const boxRatedSold = document.createElement("div");
            boxRatedSold.className = "box-rated-sold";
            const boxRated = document.createElement("div");
            boxRated.className = "box-rated";
            for (let i = 0; i < 4; i++) {
                const starImg = document.createElement("img");
                starImg.src = "/static/images/star.png";
                starImg.alt = "";
                starImg.style.width = "18px";
                starImg.style.height = "18px";
                boxRated.appendChild(starImg);
            }
            const starIcon = document.createElement("i");
            starIcon.className = "ti-star";
            starIcon.style.color = "yellow";
            starIcon.style.fontSize = "15px";
            boxRated.appendChild(starIcon);

            const quantitySold = document.createElement("span");
            quantitySold.className = "quantity-sold";
            quantitySold.textContent = "Đã bán " + formatQuantity(product.quantitySold);

            boxRatedSold.appendChild(boxRated);
            boxRatedSold.appendChild(quantitySold);

            const boxPrice = document.createElement("div");
            boxPrice.className = "box-price";
            const price = document.createElement("div");
            price.className = "price";
            price.textContent = product.price.toLocaleString('vi-VN');
            const sup = document.createElement("sup");
            sup.textContent = "đ";
            price.appendChild(sup);

            const priceDiscount = document.createElement("div");
            priceDiscount.className = "price-discount";
            priceDiscount.textContent = `-20%`;

            boxPrice.appendChild(price);
            boxPrice.appendChild(priceDiscount);

            contentBox.appendChild(boxLabel);
            contentBox.appendChild(boxName);
            contentBox.appendChild(boxRatedSold);
            contentBox.appendChild(boxPrice);

            productBox.appendChild(boxImg);
            productBox.appendChild(contentBox);

            productList.appendChild(productBox);
        });
    } catch (error) {
        console.error(error);
    }
}

async function getTotalpage(parentID, childID, key, page, page_size) {
    try {
        let url;
        if (parentID == null){
          url = `http://localhost:9000/productSearch?key=${key}&page=${page}&page_size=${page_size}`;
        }
        else{
            if (childID == null){
                url = `http://localhost:9000/productParentCate?parentID=${parentID}&page=${page}&page_size=${page_size}`;
            }
            else{
                url = `http://localhost:9000/productChildCate?childID=${childID}&page=${page}&page_size=${page_size}`;
            }
        }
        const response = await fetch(url, {
            method: 'GET',
            headers: header
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        
        const totalpage = data.total_page;
        return totalpage;
    }
    catch (error){
        console.error(error);
    }
}
async function setPage(parentID, childID, key, page) {
    const leftPagination = document.querySelector('.left__pagination');
    const rightPagination = document.querySelector('.right__pagination');
    const centerPagination = document.querySelector('.center__pagination');
    leftPagination.innerHTML = '';
    centerPagination.innerHTML = '';
    rightPagination.innerHTML = '';
    if (page - 1 > 0){
          page = page - 1;
      }
      else{
          page = 1;
      }
    centerPagination.textContent = page;
    // Tạo nút "Double Left"
    const doubleLeft = document.createElement('a');
    doubleLeft.setAttribute("id", "doublebackPage");
    // doubleLeft.id = ""

    const doubleLeftIcon = document.createElement('i');
    doubleLeftIcon.className = 'ti-angle-double-left';

    doubleLeft.appendChild(doubleLeftIcon);
    leftPagination.appendChild(doubleLeft);

    //Xử lý sự kiện doublebackPage
    doublebackPage.addEventListener("click", async function(event){
        page = 1;
        centerPagination.textContent = page;
        await updatePage(parentID, childID, key, page);
    });

    // Tạo nút "Left"
    const left = document.createElement('a');
    left.setAttribute("id", "backPage");

    const leftIcon = document.createElement('i');
    leftIcon.className = 'ti-angle-left';

    left.appendChild(leftIcon);
    leftPagination.appendChild(left);

    //Xử lý sự kiện backPage
    backPage.addEventListener("click", async function(event){
        if (page - 1 > 0){
            page = page - 1;
        }
        else{
            page = 1;
        }
        centerPagination.textContent = page;
        await updatePage(parentID, childID, key, page);
    });


    // Tạo nút "Right"
    const right = document.createElement('a');
    right.setAttribute('id', 'nextPage');
    
    const rightIcon = document.createElement('i');
    rightIcon.className = 'ti-angle-right';

    right.appendChild(rightIcon);
    rightPagination.appendChild(right);
    // Xử lý sự kiện nextPage
    const next = document.getElementById("nextPage");
    next.addEventListener('click', async function(event) {
       const totalpage = await getTotalpage(parentID, childID, key, page, 10);
        if (page + 1 > totalpage){
            page = totalpage;
        }
        else{
            page = page + 1;
        }
        centerPagination.textContent = page;

        await updatePage(parentID, childID, key, page);
    });
  

    // Tạo nút "Double Right"
    const doubleRight = document.createElement('a');
    doubleRight.setAttribute("id", "doublenextPage")
    const doubleRightIcon = document.createElement('i');
    doubleRightIcon.className = 'ti-angle-double-right';
    doubleRight.appendChild(doubleRightIcon);
    rightPagination.appendChild(doubleRight);
    // Xử lý sự kiện doublenextPage
    const doublenext = document.getElementById("doublenextPage");
    doublenext.addEventListener('click', async function(event) {
        // page = total_page;
      const totalpage = await getTotalpage(parentID, childID, key, page, 10);
      page = totalpage;
        centerPagination.textContent = page;
        // await updatePage(page);
        await updatePage(parentID, childID, key, page);
    });
}

async function updatePage(parentID, childID, key, page) {
    await setproductAll(parentID, childID, key, page, 10);
}

function eventSearch(page){
    document.addEventListener("DOMContentLoaded", function() {
        const searchForm = document.getElementById("search-form");
        
        searchForm.addEventListener("submit", function(event) {
            event.preventDefault(); // Ngăn chặn việc gửi form đi
        
            const formData = new FormData(searchForm);
            const searchTerm = formData.get("key");
        
            if (searchTerm.trim() !== "") {
                setPage(null, null, searchTerm, page);
                updatePage(null, null, searchTerm, page);
                setParentCate(searchTerm, page, 10);
                const title = `Trang chủ > Tìm kiếm "${searchTerm}"`;
                setTitleProduct(title);
            } else {
                alert("Vui lòng nhập từ khóa tìm kiếm.");
            }
        });
    });
}


// tìm kiếm sản phẩm
eventSearch(1);

updateIndexPage(null, null, '', 1, 10);
//set danh mục sản phẩm
setParentCate('', 1, 10);
// câp nhật lại danh sách sản phẩm
updatePage(null, null, '', 10);
  