### [1. Tạo model Post bao gồm các trường sau:](https://github.com/tangoc2712/blogApp/blob/main/blog/models.py#L13-L43)

-   Title: tít lè của bài Post, kiểu dữ liệu CharField ó VARCHAR trong SQL
-   Slug: sẽ được sử dụng để xây dựng những URL đẹp, tiện cho SEO
-   Author: ForeinKey khai báo một trường dạng quan hệ many-to-one, tham số on_delete=CASCADE sẽ chỉ định hành vi áp dụng khi đối tượng bị xóa cả ở Django và SQL, tỉ dụ khí xóa một User thì những bài đăng của User này cũng sẽ bị xóa
-   Body: Nội dung của bài post
-   Publish: thời điểm bài post được xuất bản, sử dụng timezone.now
-   Created: ngày giờ khi một bài post được tạo, cái này nó sẽ tạo khi một đối tượng mới được tạo
-   Updated: được tạo ngay khi lưu một đối tượng
-   Status: trạng thái của bài Post, có tham số choices để chọn
    <br>

### [2. Trong models, ta có manager mặc định là objects. Ngoài ra cũng có thể tự tạo một manager dành cho model. Ví dụ cụ thể ở bài toán lần này là tạo một custom manager cho models Post là PublishedManager để quản lý những bài đăng đã được xuất bản](https://github.com/tangoc2712/blogApp/blob/main/blog/models.py#L8-L10)

<br>
	
![alt text](https://github.com/tangoc2712/blogApp/blob/main/image/Screenshot%202022-02-25%20183916.png?raw=true)

<br>

### [3. Tạo list và detail view](https://github.com/tangoc2712/blogApp/blob/main/blog/views.py#L7-L500)

-   View list này là function view, tham số là một request, nó sẽ lấy hết ra những post đã publised và trả về một nội dung Html, có template là list.html
-   Detail view thì nhận tham số là request, post, ngày, tháng, năm. Trước nhất kiểm tra xem post đã tồn tại, và được publish hay chưa. Sau đó cũng trả về hàm render()
    <br>

### [4. Tạo url cho các view vừa định nghĩa](https://github.com/tangoc2712/blogApp/blob/main/blog/urls.py#L4-L20), và [include vào cả url của project](https://github.com/tangoc2712/blogApp/blob/main/mysite/urls.py#L20)

-   Viết thêm một hàm [get_absolute_url](https://github.com/tangoc2712/blogApp/blob/19dd345152578859abdfbe2bd248322413048e6d/blog/models.py#L39-L43) tại model, điều này giúp trả về một url chính quy cho bài post. Đối với webblog, bài post có thể được hiển thị ở nhiều trang/url khác nhau. Tuy nhiên chỉ có một url là main.

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

### [7. Class-based view](https://github.com/tangoc2712/blogApp/blob/main/blog/views.py#L13-L17)

Thay đổi view từ fucntion-based sang class-based view có một số lợi ích như:

-   Dễ dàng tổ chức code liên quan đến các phương thức HTTP
-   Sử dụng tính kế thừa để tái sử dụng các view (mixins)

### 8. Chia sẻ bài đăng bằng email (Form Handle)

Để gửi email bằng host của gmail, ta cần cài đặt trong [settings.py](https://github.com/tangoc2712/blogApp/blob/main/mysite/settings.py#L85-L90), sau đó cài đặt cho quyền truy cập không an toàn ở tài khoản gmail(_không khuyến khích làm theo_)

-   [Tạo form để người dùng điền thông tin](https://github.com/tangoc2712/blogApp/blob/main/blog/forms.py)
-   [Tạo url, template hiển thị form](https://github.com/tangoc2712/blogApp/blob/main/blog/templates/blog/post/share.html)
-   [Tạo view logic ở views.py để lấy dữ liệu bài đăng và gửi đi bằng email](https://github.com/tangoc2712/blogApp/blob/main/blog/views.py#L60-L90)

### 9. Tạo hệ thống comment

Danh sách các công việc cần làm là:

-   [Tạo model chứa các thông tin comment từ guess](https://github.com/tangoc2712/blogApp/blob/main/blog/models.py#L46-L59): : Gồm các trường như là post (khóa ngoại nối nhiều một với Post model), tên, email, nội dung, ngày tạo, ngày cập nhật, trạng thái active hay chưa ====> Nhớ makemigrations, migrate, đăng kí vào admin site
-   [Tạo form và validate dữ liệu đầu vào](https://github.com/tangoc2712/blogApp/blob/main/blog/forms.py#L12-L15): Khác với class Form như ở trên gửi email, lần này ta cần lưu dữ liệu comment, nên là cần sử dụng ModelForm class
-   [Sửa tại view](https://github.com/tangoc2712/blogApp/blob/main/blog/views.py#L65-L81):
-   [Chỉnh sửa template của post_detail để thêm comment vào](https://github.com/tangoc2712/blogApp/blob/main/blog/templates/blog/post/detail.html#L27-L38)

### 10. Cài đặt PostgreSQL

-   Nếu ở Window thì cần tạo csdl và acc ở PgAdmin, sau đó ghi thông tin của csdl vào settings.py

### 11. Cài đặt Search View

Để search thì sẽ gửi GET request (chứa từ search), sau đó sẽ kiểm tra form cuối cùng cho về biến results là các đối tượng Post được filter

-   Tạo search form, chứa field là query
-   Xử lý logic ở view
-   Template
