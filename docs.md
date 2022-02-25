### 1. Tạo model Post bao gồm các trường sau:

-   Title: tít lè của bài Post, kiểu dữ liệu CharField ó VARCHAR trong SQL
-   Slug: sẽ được sử dụng để xây dựng những URL đẹp, tiện cho SEO
-   Author: ForeinKey khai báo một trường dạng quan hệ many-to-one, tham số on_delete=CASCADE sẽ chỉ định hành vi áp dụng khi đối tượng bị xóa cả ở Django và SQL, tỉ dụ khí xóa một User thì những bài đăng của User này cũng sẽ bị xóa
-   Body: Nội dung của bài post
-   Publish: thời điểm bài post được xuất bản, sử dụng timezone.now
-   Created: ngày giờ khi một bài post được tạo, cái này nó sẽ tạo khi một đối tượng mới được tạo
-   Updated: được tạo ngay khi lưu một đối tượng
-   Status: trạng thái của bài Post, có tham số choices để chọn
    <br>

### 2. Trong models, ta có manager mặc định là objects. Ngoài ra cũng có thể tự tạo một manager dành cho model. Ví dụ cụ thể ở bài toán lần này là tạo một custom manager cho models Post là PublishedManager để quản lý những bài đăng đã được xuất bản.

<br>
![](http://url/to/img.png)

<br>

### 3. Tạo list và detail view

-   View list này là function view, tham số là một request, nó sẽ lấy hết ra những post đã publised và trả về một nội dung Html, có template là list.html
-   Detail view thì nhận tham số là request, post, ngày, tháng, năm. Trước nhất kiểm tra xem post đã tồn tại, và được publish hay chưa. Sau đó cũng trả về hàm render()
    <br>

### 4. Tạo url cho các view vừa định nghĩa, và include vào cả url của project

-   Viết thêm một hàm get_absolute_url() tại model, điều này giúp trả về một url chính quy cho bài post. Đối với webblog, bài post có thể được hiển thị ở nhiều trang/url khác nhau. Tuy nhiên chỉ có một url là main.

### 5. Tạo template

Django template dựa trên:

-   Template tag (có thể custom): {% tag %}
-   Template variable: {{ variable }}
-   Template filter: {{ variable|filter }}

### 6. Phân trang

Ở Django có built-in class để phân trang là pagnigator, ta sẽ thêm vào ở view. Cách phân trang hoạt động như sau:

1. Đầu tiên khởi tạo một class Paginator() nhận hai tham số là object_list và per_page (tức là đưa ra số đối tượng ở một trang)
2. Tạo biến page lấy tham số 'page' từ request, đây là trang hiện tại
3. Giờ có thể gọi các đối tượng mong muốn bằng phương thức page() của class Paginator
4. Viết một cái ngoại lệ nếu trang không là số nguyên thì chuyển hướng về trang đầu và nếu trang không tồn tại thì trả về trang cuối cùng trong danh sách
5. Tiếp theo là viết template view cho cái phân trang này rồi include vào các template list và detail
