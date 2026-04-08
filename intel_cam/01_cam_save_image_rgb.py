# RGB만 랜더링 (pyrealsense2 사용)
# 사진 연속 저장 시작/중지: s, 나가기: q
# 저장 경로: dataset/images

import os
import cv2
import numpy as np
import pyrealsense2 as rs

# 1. 저장 폴더 설정
save_dir = 'dataset/images'
os.makedirs(save_dir, exist_ok=True)

print("🔍 RealSense D435 RGB 파이프라인 초기화 중...")

# 2. RealSense 파이프라인 및 설정 객체 생성
pipeline = rs.pipeline()
config = rs.config()

# 3. 명시적으로 RGB(Color) 스트림만 활성화
# 해상도 1920x1080, 포맷 BGR8(OpenCV 기본 포맷), 30fps 설정
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

# 파이프라인 시작
try:
    pipeline.start(config)
    print("✅ D435 RGB 스트림 연결 성공!")
except Exception as e:
    print(f"❌ 카메라 연결 실패: {e}")
    print("USB 3.0 포트에 연결되어 있는지 확인해 주세요.")
    exit()

print("\n🚀 스트리밍 시작")
print("👉 's' 키: 연속 저장 시작 / 중지 (토글)")
print("👉 'q' 키: 종료")

count = 0
is_saving = False

try:
    while True:
        # 4. 카메라에서 프레임 세트를 기다림
        frames = pipeline.wait_for_frames()
        
        # RGB 프레임만 추출
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # RealSense 프레임 데이터를 numpy 배열(OpenCV 호환)로 변환
        frame = np.asanyarray(color_frame.get_data())

        # 화면 출력
        cv2.imshow("D435 Real RGB View", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # 's' 키: 연속 저장 상태 전환
        if key == ord('s'):
            is_saving = not is_saving
            if is_saving:
                print("\n🔴 연속 저장 시작! (중지하려면 's'를 다시 누르세요)")
            else:
                print("\n⏹️ 연속 저장 중지!")
                
        # is_saving이 True일 때 프레임마다 사진 저장
        if is_saving:
            file_path = f'{save_dir}/d435_capture_{count:04d}.jpg'
            cv2.imwrite(file_path, frame)
            
            if count % 30 == 0: 
                print(f"📸 [저장 진행 중...] {file_path}")
            count += 1
            
        # 'q' 키: 프로그램 종료
        elif key == ord('q'):
            print("스트리밍을 종료합니다.")
            break

finally:
    # 5. 자원 안전하게 해제
    pipeline.stop()
    cv2.destroyAllWindows()