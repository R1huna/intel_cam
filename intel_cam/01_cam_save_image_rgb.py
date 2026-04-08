# RGB만 랜더링
# 사진 저장 s, 나가기 q
# 저장 경로 dataset/images

import os
import cv2

# 1. 저장 폴더 설정
save_dir = 'dataset/images'
os.makedirs(save_dir, exist_ok=True)

print("🔍 RealSense D435 RGB 채널을 탐색 중...")

cap = None
# D435는 하드웨어 구성상 인덱스가 0, 1, 2... 외에 4, 6번 등에 잡히는 경우가 많습니다.
for i in range(11):
    temp_cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
    if temp_cap.isOpened():
        ret, frame = temp_cap.read()
        if ret:
            # RGB 센서인지 확인 (D435의 경우 보통 3채널 이미지 스트림)
            if len(frame.shape) == 3:
                print(f"✅ {i}번 인덱스에서 D435 RGB 스트림 연결 성공!")
                cap = temp_cap
                break
    temp_cap.release()

if cap is None:
    print("❌ 카메라를 찾을 수 없습니다. USB 3.0 연결을 확인해 주세요.")
    exit()

# 2. D435 하드웨어 사양에 맞춘 해상도 설정
# RGB 센서 최대 해상도인 FHD(1920x1080)로 설정합니다.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

print("\n🚀 스트리밍 시작 (No Inference / Raw BGR Mode)")
print("👉 's' 키: 원본 이미지 저장")
print("👉 'q' 키: 종료")

count = 0

while True:
    # 카메라에서 원본 데이터(BGR)를 읽어옵니다.
    ret, frame = cap.read()
    
    if not ret:
        print("프레임을 수신할 수 없습니다.")
        break

    # 3. 색상 변환 없이 원본(BGR) 그대로 화면 출력
    # (cv2.imshow는 기본적으로 BGR 형식을 기대하므로 변환이 없는 것이 가장 빠릅니다)
    cv2.imshow("D435 Raw RGB View", frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    # 's' 키: 현재 화면 저장 (원본 BGR 그대로 저장)
    if key == ord('s'):
        file_path = f'{save_dir}/d435_capture_{count:04d}.jpg'
        cv2.imwrite(file_path, frame)
        print(f"📸 [저장 완료] {file_path}")
        count += 1
        
    # 'q' 키: 프로그램 종료
    elif key == ord('q'):
        print("스트리밍을 종료합니다.")
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()