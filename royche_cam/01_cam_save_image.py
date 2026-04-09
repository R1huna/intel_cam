# R, G, B 차원 랜더링 모델
# 사진 자동 연속 저장 시작/중지: s, 나가기: q
# 저장 경로: dataset/royche_images

import cv2
import os
import time

def main():
    save_dir = 'dataset/royche_images'
    os.makedirs(save_dir, exist_ok=True)

    # 🌟 [핵심 수정 1] 우분투(Linux) 환경에서 카메라 제어 권한을 확실히 얻기 위해 CAP_V4L2 백엔드 사용
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    if not cap.isOpened():
        print("❌ 카메라를 찾을 수 없습니다. 포트 연결을 확인해 주세요.")
        return

    # 🌟 [핵심 수정 2] FHD 30FPS 유지를 위한 MJPG 포맷 설정
    # 일반 웹캠은 YUYV 포맷으로 FHD 30FPS 전송이 불가하여 강제로 프레임이 떨어지고 블러가 생깁니다.
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    cap.set(cv2.CAP_PROP_FOURCC, fourcc)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # 🌟 [핵심 수정 3] 확실한 수동 노출 제어
    # V4L2 기준 Auto Exposure: 1 (Manual Mode), 3 (Auto Mode)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) 
    
    # 노출값(Exposure)을 확 낮춰서 빛 번짐과 블러를 잡습니다.
    # 화면이 너무 어두워지면 이 숫자를 100, 150 등으로 올려주세요.
    exposure_value = 50 
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure_value)
    
    print(f"⚙️ 카메라 설정 완료: FHD, 30FPS, MJPG, 수동 노출({exposure_value})")
    
    # 사진 저장
    target_fps = 5  
    save_interval = 1.0 / target_fps
    last_save_time = 0

    print("\n🚀 실시간 스트리밍을 시작합니다.")
    print(f"👉 's' 키: 자동 연속 저장 시작 / 중지 (초당 {target_fps}장)")
    print("👉 'q' 키: 종료")

    count = 0
    is_saving = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 수신할 수 없습니다.")
            break

        cv2.imshow("Camera Stream", frame)

        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s'):
            is_saving = not is_saving
            if is_saving:
                print(f"\n🔴 자동 연속 저장 시작! (초당 {target_fps}장 간격)")
                last_save_time = time.time() - save_interval 
            else:
                print("\n⏹️ 자동 연속 저장 중지!")

        if is_saving:
            current_time = time.time()
            
            if (current_time - last_save_time) >= save_interval:
                file_path = os.path.join(save_dir, f'{count:04d}_royche.jpg')
                cv2.imwrite(file_path, frame)
                
                last_save_time = current_time
                
                if count % target_fps == 0:
                    print(f"📸 [저장 진행 중...] {file_path}")
                count += 1

        elif key == ord('q'):
            print("\n스트리밍을 종료합니다.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()