# Shop Management web app

## Mô tả
- Đây là một web chuyên về bán giày
- Được thiết kế đơn giản gọn nhẹ nhưng đầy đủ chức năng để mang sự tiện lợi cho cả người bán lẫn người mua.
- Giao dịch với khách hàng, tạo ra hoá đơn thanh toán cho cả khách hàng lẫn người bán, không hỗ trợ giao dịch trực truyến
 
### Admin user cho thầy đăng nhập:
- Tên: admin
- Pass: admin
- Thầy có thể truy cập đường link này để vào trang admin, điều chỉnh dữ liệu trong CSDL:
https://shoesvendor.herokuapp.com/admin

## Chức năng
- Đăng ký/Đăng nhập với tư cách là khách hàng hoặc người bán hàng(thông qua page ẩn admin). Có hệ thống session lưu người dùng kể cả khi đã tắt browser(có các bảng của Django trong CSDL)
- Có page product đưa ra danh sách hàng, mỗi hàng sẽ có nút View Details để hiện thêm thông tin
- Có thể tìm kiếm món hàng bằng cách nhập tên. Có thể lọc và sắp xếp hàng theo tên hoặc giá
- Trong thông tin sản phẩm, người mua có thể thêm hàng vào rỏ hàng với số lượng tuỳ thích. Sẽ thông báo "Đã cho vào rỏ hàng" nếu thêm vào thành công. Số lượng tồn kho sẽ giảm nếu hàng được thanh toán
- Ở đây có bảng Cart để lưu thông tin các món hàng. Các món hàng được phân biệt với nhau qua mã hàng và người mua, kèm theo số lượng và giá mỗi hàng.
- Có các hàm xử lý sao cho nhiều người dùng cùng thêm hàng cùng một lúc. Khi hết hàng mà người khác vốn đã thêm từ trước, thì món hàng đó sẽ bị mất, kèm theo một thông báo cho người dùng.
- Có page Cart - giỏ hàng để người dùng xem chi tiết rỏ hàng của mình. Ở đây dùng Group By để gộp lại bất kì hàng nào được thêm nhiều lần. Khách hàng có thể checkout, lưu lại hoá đơn giao dịch để thực hiện sau này.
- Trong page Cart, người dùng có thể Delete bất kì món hàng nào mình không muốn.
- Có page Order - hoá đơn để người dùng xem, hiện ra thông tin về hàng và người mua, tổng tiền và trạng thái gửi.

## Các câu lệnh SQL chính
- Lấy sản phẩm theo id riêng:
    ```
    SELECT * FROM `products` WHERE `product_id` = pid
    ```
- Lấy danh sách sản phẩm trong cart sau khi được Group By theo id sản phẩm:
    ```
    SELECT *, SUM(`cart`.`quantity`) AS `quantity` FROM `cart` WHERE `user` = username 
    GROUP BY `cart`.`productID`, `cart`.`productName`, `cart`.`productImage`, `cart`.`sellPrice`, `cart`.`user`
    ```
- Lấy thông tin hàng được chọn bởi người dùng và cho vào giỏ hàng:
    ```
    INSERT INTO cart(`product_id`, `product_name`, `product_image`, `quantity`, `user`)
    VALUES (product_id, product_name, product_image, quantity, user)
    ``` 
- Xoá hàng khỏi giỏ nếu người dùng muốn hoặc do hết hàng:
    ```
    DELETE FROM cart
    WHERE `user` = request.user.username AND `product_id` = pid
    ```
- Cập nhật số lượng trong giỏ nếu hàng tồn kho không đủ:
    ```
    UPDATE cart
    SET quantity = in_stock
    WHERE `user` = request.user.username AND `product_id` = pid
    ```
- Cập nhật số hàng tồn kho sau khi đã thanh toán:
    ```
    UPDATE products
    SET quantity = quantity_in_stock
    WHERE `product_id` = pid
    ```
- Hiện hoá đơn cho người dùng:
    ```
    SELECT * FROM `orderDJ` WHERE `user` = request.user.username
    ```
- Thêm chi tiết vào bảng orderDJ:
    ```
    INSERT INTO orderDJ(`user`, `customer_name`, `address`, `phone`, `total_price`)
    VALUES (user, customer_name, address, phone, total_price)
    ```
- Tìm kiếm món hàng theo định dạng tên hàng:
    ```
    SELECT * FROM `products` 
    WHERE UPPER(`products`.`productName`::text) LIKE UPPER(%adidas%)
    ```
- Lọc hàng mà không Out Of Stock:
    ```
    SELECT * FROM `products` WHERE NOT (`products`.`quantityInStock` = 0)
    ```
- Sắp xếp vị trí món hàng theo bảng chữ cái:
    ```
    SELECT * FROM `products` ORDER BY `products`.`productName` ASC
    ```

## Quá trình phát triển
- Định hình mục tiêu là làm web bán giày và nền tảng cho nó là Django
- Thiết kế cấu trúc trang web
- Xây dựng các thành phần back-end của Django, bắt đầu xây dựng chức năng
- Xây dựng front-end cho web với HTML, CSS, JS và Bootstrap. Đồng thời cũng dùng Jinja cho dynamic data
- Kiểm thử các chức năng như nhiều người cùng thêm và thanh toán hàng, hết hàng
- **FIX BUG**
- Hoàn thiện trang web

## Ảnh demo web
- Homepage - landing page
<img src="README_image/homepage.png">
- Register 
<img src="README_image/Register.png">
- Login
<img src="README_image/Login.png">
- Trang sản phẩm
<img src="README_image/Products.png" >
- Chi tiết sản phẩm
<img src="README_image/Details.png">
- Giỏ hàng
<img src="README_image/Cart.png">
- Chi tiết sản phẩm sau khi thêm vào giỏ
<img src="README_image/Details_cart.png">
- Điền thông tin giao hàng
<img src="README_image/OrderDetails.png">
- Page đơn hàng
<img src="README_image/Orders.png">
