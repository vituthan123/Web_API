
// document.addEventListener("DOMContentLoaded", function() {
//     const searchForm = document.getElementById("search-form");
    
//     searchForm.addEventListener("submit", function(event) {
//         event.preventDefault(); // Ngăn chặn việc gửi form đi
    
//         const formData = new FormData(searchForm);
//         const searchTerm = formData.get("key");
    
//         if (searchTerm.trim() !== "") {
//             // Chuyển hướng đến trang tìm kiếm với từ khóa nhập vào
//             window.location.href = `/search.html?key=${searchTerm}`;
//         } else {
//             alert("Vui lòng nhập từ khóa tìm kiếm.");
//         }
//     });
// });