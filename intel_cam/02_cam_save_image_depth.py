# R, G, B, Depth 차원 랜더링 모델
# 사진 저장 s, 나가기 q
# 저장 경로 dataset/images

import os
import cv2
import numpy as np
import pyrealsense2 as rs

# 1. 이미지를 저장할 폴더 설정 및 생성
save_dir = 'dataset/images'
os.makedirs(save_dir, exist_ok=True)

pipeline = rs.pipeline()
config = rs.config()

# 2. 리눅스 환경에 맞춰 안정적인 해상도(1280x720)로 설정
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

print("🚀 RealSense 카메라 스트리밍 시작...")
print(f"👉 's' 키: RGB 원본 사진 저장 (경로: {save_dir}/)")
print("👉 'q' 키: 프로그램 종료")

# 저장 파일명에 붙일 번호 카운터
count = 0

try:
    pipeline.start(config)
    print("✅ 파이프라인 시작 성공! 화면을 띄웁니다.")
    
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # 배열 변환 (우리가 아는 넘파이 배열 형태로 변환)
        depth_image = np.asanyarray(depth_frame.get_data())
        
        # 💡 color_image: 이 변수가 뎁스가 섞이지 않은 순수 RGB 프레임입니다.
        color_image = np.asanyarray(color_frame.get_data())

        # 화면 출력을 위한 Depth 컬러맵 생성
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET
        )

        # 화면에 띄울 때만 두 이미지를 가로로 이어붙임 (저장본과는 무관함)
        images = np.hstack((color_image, depth_colormap))
        cv2.imshow('RealSense Stream - Press "s" to save RGB', images)

        key = cv2.waitKey(1) & 0xFF

        # 3. 's' 키를 누르면 RGB만 저장
        if key == ord('s'):
            # 파일 경로 지정 (예: dataset/images/capture_0000.jpg)
            file_path = f"{save_dir}/capture_{count:04d}.jpg"
            
            # 💡 hstack으로 합쳐진 'images'가 아니라, 순수 RGB인 'color_image'를 저장합니다.
            cv2.imwrite(file_path, color_image)
            
            print(f"📸 [{count}번째] RGB 사진 저장 완료: {file_path}")
            count += 1
            
        # 4. 'q' 키를 누르면 종료
        elif key == ord('q'):
            print("프로그램을 안전하게 종료합니다.")
            break

finally:
    # 자원 해제
    pipeline.stop()
    cv2.destroyAllWindows()