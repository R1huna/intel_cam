# 캠 번호 확인

import cv2

for i in range(6):
    cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✅ 빙고! 현재 작동하는 진짜 카메라 번호는 {i}번 입니다!")
            cap.release()
            break
    cap.release()