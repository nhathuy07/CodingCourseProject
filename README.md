# Dự án trò chơi: Space Miner

## Người tham gia
****
Nguyễn Đình Nhật Huy [huyndn2007@gmail.com](mailto:huyndn2007@gmail.com)

## Cách cài đặt thư viện và chạy chương trình
****
1. Tạo Virtual Environment: `python -m venv .venv`
2. Khởi động Virtual Environment: `.venv/Scripts/activate` (đối với Windows) hoặc `.venv/bin/activate` (đối với macOS)
3. Cài đặt các thư viện: `python -m pip install -r requirements.txt`

## Mô tả trò chơi
****
### Nhân vật
1. **Mark**: Đây là một người máy phi hành gia, có nhiệm vụ thực hiện các chuyến thám hiểm ở xa Trái Đất nhưng không may bị gặp nạn và phải sửa tàu. Xuyên suốt trò chơi, người chơi sẽ điều khiển nhân vật này di chuyển qua địa hình bằng `Phím mũi tên Trái / Phải`, nhảy qua chướng ngại vật bằng phím `Spacebar`, bắn hạ quái vật bằng phím `F` và đi xuyên qua các vật phẩm (quặng, tăng sức mạnh) để nhận chúng.<br>
⚠️**GIỚI HẠN CỦA NHÂN VẬT**:<br>
    * Sau khi bắn một viên đạn, người chơi phải chờ khoảng **0.2 giây** để bắn viên tiếp theo
    * Nhân vật được cung cấp 100 HP, và **không thể** hồi lại HP trong suốt màn chơi.
    * Nếu bị rơi xuống vũng chất lỏng ăn mòn, lượng HP của nhân vật sẽ tụt xuống 0 **gần như lập tức**.
    * Nhân vật có tốc độ giới hạn, và cần mất một khoảng thời gian ngắn (dưới **1s** từ khi bắt đầu di chuyển) để đạt **tốc độ tối đa.**, và phải mất một khoảng thời gian kể từ khi nhả phím `Trái / Phải` để **dừng di chuyển hoàn toàn**.

2. **Roger**: Nhân vật này sở hữu dịch vụ sửa chữa phương tiện giao thông, là người đã đề nghị sửa chữa tàu cho nhân vật chính, đổi lại, nhân vật chính đi khai thác quặng cho anh ta. Nhân vật này chỉ xuất hiện ở đoạn hội thoại mở đầu của trò chơi, và đoạn hội thoại cuối khi con tàu của nhân vật chính đã được sửa chữa xong.
3. **Monster**: Những sinh vật ngoài hành tinh, trú ngụ trong hang động và luôn nhăm nhe tấn công nhân vật chính. Chúng có ba chủng màu khác nhau: đỏ, nâu và đen, mỗi chủng đều có tốc độ di chuyển, sức mạnh và lượng HP khác nhau. Trong số các loài trên, loài màu đen là đặc biệt hơn cả, vì khi bị tiêu diệt, chúng sẽ thải ra một loại **thanh năng lượng**.
4. **Floating Beast**: Trùm cuối của trò chơi, có tính cách hung hãn, và xuất hiện khi nhân vật chính chuẩn bị rời khỏi hành tinh. Khi phát hiện ra nhân vật chính đã thâm nhập vào hang động và tiêu diệt thuộc hạ, tên trùm cuối đã nổi giận và quyết hạ gục người chơi trong một trận đấu **ngoài không gian**. Trong suốt trận đấu, Floating Beast liên tục tấn công người chơi bằng những luồng đạn, những cơn mưa thiên thạch và những tiếng gào thét to đến mức có thể đẩy bật người chơi xuống vực.
### Bối cảnh
1. Bối cảnh của trò chơi được đặt trên một hành tinh lạ, vào năm 2070. Khi đó, công nghệ đã phát triển vượt bậc, người máy dần được ưa dùng cho những chuyến thám hiểm không gian nhờ vào khả năng tự sạc lại pin và tiếp xúc với những môi trường nguy hiểm.<br>

2. Ở mỗi ván chơi, thời gian là không giới hạn. Màn chơi sẽ kết thúc khi người chơi thu thập đủ số quặng được yêu cầu, hoặc khi nhân vật bị hư hại hoàn toàn (lượng HP tụt về 0)

### Cốt truyện
Mark - một người máy phi hành gia -  đang thực hiện chuyến thám hiểm vũ trụ. Chuyến đi diễn ra rất suôn sẻ, nhưng một tảng thiên thạch lớn đã va mạnh vào phần sau của con tàu, khiến con tàu bị hư hại nặng và phải hạ cánh khẩn cấp xuống một hành tinh lạ có bề mặt màu xanh dương. Sau khi hạ cánh, người máy đã tìm được tiệm sửa chữa phương tiện giao thông của Roger. Khi biết tàu của Mark phải thay nhiều bộ phận quan trọng nhưng cậu không có một xu dính túi, Roger đã gợi ý cậu đi khai thác quặng dưới hang để thanh toán chi phí sửa chữa và không quên dặn cậu rằng dưới hang có rất nhiều mối nguy.<br>

Vậy là, Mark lên đường, vượt qua bốn cái hang khác nhau, vừa thu thập đủ quặng, vừa phải coi chừng bị tấn công, vừa phải tránh những vũng nước có khả năng ăn mòn cực cao. Và, mỗi lần đi khai thác thành công, một bộ phận trên chiếc tàu sẽ được thay mới.<br>

Sau khi sửa xong con tàu, Mark lại tiếp tục cuộc hành trình, nhưng mọi chuyện vẫn chưa kết thúc ở đó. Floating Beast - trùm cuối của trò chơi - đã phát hiện ra rằng những thuộc hạ của hắn bị tiêu diệt nên rất tức giận và quyết đấu với Mark một trận ngoài không gian. Trong suốt trận đấu, Mark bị tấn công dồn dập bởi những luồng đạn, những cơn mưa thiên thạch và những luồng sóng âm mạnh đến mức có thể đẩy văng cậu ta đi xa.
Cuối trò chơi, sau khi tiêu diệt Floating Beast, Mark đã có thể tiếp tục chuyến khám phá của mình.

### Điểm nổi bật trong trò chơi
1. Các nút chọn màn chơi trong giao diện được biểu thị bằng **hình ảnh đại diện** thay vì chỉ bằng văn bản.
2. Trò chơi cho phép người dùng chơi các màn chơi theo **bất cứ thứ tự nào**, không nhất thiết phải chơi lần lượt từ **màn 1, màn 2, màn 3, v.v.**
3. Hệ thống Cutscenes trong trò chơi có lồng **hiệu ứng âm thanh** (tiếng động cơ phản lực, giọng của người máy, v.v) để tăng độ sinh động.
4. Trong suốt màn chơi, người chơi sẽ được thấy nhiều **hiệu ứng hình ảnh** khác nhau (lửa phun từ động cơ của người máy, đạn phát nổ, đất lở ra và rơi cùng thạch nhũ,...)
5. Tiến trình chơi được **tự động lưu lại** sau mỗi màn chơi để người chơi có thể chơi tiếp vào những lần sau.
6. Thời gian Boss ra đòn tấn công là **ngẫu nhiên**, khiến người chơi phải luôn cảnh giác.

## Sản phẩm này có sử dụng mã nguồn / hình ảnh / âm thanh từ các nguồn sau
****
* <a href="https://www.flaticon.com/free-icons/asteroid" title="Asteroid icons">Asteroid icons created by monkik - Flaticon</a><br>
* Galaxy background vector created by pikisuperstar - www.freepik.com<br>
* Watercolor planet collection with gas rings created by pikisuperstar - Freepik<br>
* [freesound.org](https://freesound.org)
* [mixkit.co](https://mixkit.co)
* [pixabay.com](https://pixabay.com)
* [https://stackoverflow.com/questions/44721221/natural-sort-of-list-containing-paths-in-python](https://stackoverflow.com/questions/44721221/natural-sort-of-list-containing-paths-in-python)
* [https://github.com/STEAMforVietnam/cs102](https://github.com/STEAMforVietnam/cs102)
* [https://www.pygame.org/wiki/](https://www.pygame.org/wiki/)