# RGB만 랜더링 (pyrealsense2 사용)
# 사진 연속 저장 시작/중지: s, 나가기: q
# 저장 경로: dataset/intel_images

import os
import cv2
import numpy as np
import pyrealsense2 as rs
import time  # ⏱️ 시간 체크를 위해 추가

# 1. 저장 폴더 설정
save_dir = 'dataset/intel_images'
os.makedirs(save_dir, exist_ok=True)

print("🔍 RealSense D435 RGB 파이프라인 초기화 중...")

# 2. RealSense 파이프라인 및 설정 객체 생성
pipeline = rs.pipeline()
config = rs.config()

# 3. 명시적으로 RGB(Color) 스트림만 활성화
# 해상도 640x480, 포맷 BGR8(OpenCV 기본 포맷), 30fps 설정
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 파이프라인 시작 및 카메라 프로파일 획득
try:
    profile = pipeline.start(config)
    print("✅ D435 RGB 스트림 연결 성공!")
    
    # 🌟 [추가됨] 번짐(Motion Blur) 방지를 위한 수동 노출(Exposure) 설정
    device = profile.get_device()
    color_sensor = None
    for sensor in device.query_sensors():
        if sensor.is_color_sensor():
            color_sensor = sensor
            break

    if color_sensor:
        # 자동 노출 끄기 (0: Off, 1: On)
        color_sensor.set_option(rs.option.enable_auto_exposure, 0)
        
        # 수동 노출값 설정 (환경에 맞게 50 ~ 200 사이로 조절하세요. 값이 작을수록 번짐이 덜함)
        exposure_value = 100 
        color_sensor.set_option(rs.option.exposure, exposure_value)
        print(f"⚙️ 수동 노출 설정 완료: {exposure_value} (자동 노출 OFF)")

except Exception as e:
    print(f"❌ 카메라 연결 실패: {e}")
    print("USB 3.0 포트에 연결되어 있는지 확인해 주세요.")
    exit()

# 🎯 [추가됨] 저장 속도 제어를 위한 변수 설정
target_fps = 5  # 초당 저장할 사진 장수 (필요에 따라 수정)
save_interval = 1.0 / target_fps  # 한 장 저장하는 데 걸리는 시간 간격
last_save_time = 0  # 마지막 저장 시간 기록

print("\n🚀 스트리밍 시작")
print(f"👉 's' 키: 연속 저장 시작 / 중지 (초당 {target_fps}장 저장)")
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
                print(f"\n🔴 연속 저장 시작! (초당 {target_fps}장 간격)")
                # 's'를 누르자마자 첫 장이 즉시 찍히도록 시간 초기화
                last_save_time = time.time() - save_interval 
            else:
                print("\n⏹️ 연속 저장 중지!")
                
        # is_saving이 True일 때 설정한 시간 간격마다 프레임 저장
        if is_saving:
            current_time = time.time()
            
            # ⏱️ [추가됨] 설정한 간격(save_interval)이 지났을 때만 저장
            if (current_time - last_save_time) >= save_interval:
                file_path = f'{save_dir}/{count:04d}_intel_d435.jpg'
                cv2.imwrite(file_path, frame)
                
                last_save_time = current_time # 마지막 저장 시간 갱신
                
                # 로그가 너무 많이 찍히지 않게 조절
                if count % target_fps == 0: 
                    print(f"📸 [저장 진행 중...] {file_path}")
                count += 1
            
        # 'q' 키: 프로그램 종료
        elif key == ord('q'):
            print("\n스트리밍을 종료합니다.")
            break

finally:
    # 5. 자원 안전하게 해제
    pipeline.stop()
    cv2.destroyAllWindows()