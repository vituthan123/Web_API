

# Sử dụng một base image chứa nginx
FROM nginx:alpine

# Xác định thư mục làm việc mặc định trong container
WORKDIR /var/www/html

# Xoá các tệp mặc định của nginx
RUN rm -rf ./*

# Sao chép các tệp và thư mục cần thiết từ thư mục cục bộ vào container
COPY . /var/www/html
# COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./static /var/www/html/static
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
# Expose cổng mà nginx sẽ chạy trên
EXPOSE 80

# Khởi động nginx khi container được khởi chạy
CMD ["nginx", "-g", "daemon off;"]
