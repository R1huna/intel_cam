# R, G, B 차원 랜더링 모델
# 사진 저장 s, 나가기 q
# 저장 경로 dataset/images

import cv2
import os

def main():
    # 저장 폴더 설정 (필요 시 사용)
    save_dir = 'dataset/images'
    os.makedirs(save_dir, exist_ok=True)

    # 웹캠 연결 (D435 또는 일반 웹캠 인덱스 설정)
    # 이전 코드의 인덱스 1을 유지하거나, 연결된 포트에 맞게 수정하세요.
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("카메라를 찾을 수 없습니다.")
        return

    print("실시간 스트리밍을 시작합니다. (종료: 'q' 키 / 저장: 's' 키)")

    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 수신할 수 없습니다.")
            break

        # 화면 출력
        cv2.imshow("Camera Stream", frame)

        key = cv2.waitKey(1) & 0xFF
        
        # 's' 키: 현재 화면 저장
        if key == ord('s'):
            file_path = os.path.join(save_dir, f'capture_{count:04d}.jpg')
            cv2.imwrite(file_path, frame)
            print(f"[저장 완료] {file_path}")
            count += 1

        # 'q' 키: 종료
        elif key == ord('q'):
            print("스트리밍을 종료합니다.")
            break

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()