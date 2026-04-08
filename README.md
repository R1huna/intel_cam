# 📸 Camera Image Save Models (Intel & Royche)

이 프로젝트는 Intel RealSense 카메라와 Royche(일반 웹캠) 카메라를 사용하여 영상 스트림을 받아오고, 이미지를 저장하는 파이썬(Python) 스크립트 모음입니다.

## 📂 폴더 구조 및 설명

이 저장소는 크게 인텔 카메라용 폴더와 로이체 카메라용 폴더로 나뉘어 있습니다.

### 1. `intel_cam/` (Intel RealSense 전용)
* `00_cam_num.py`: 현재 PC에 연결된 인텔 카메라의 장치 번호(Index)를 확인하는 스크립트입니다.
* `01_cam_save_image_rgb.py`: 인텔 카메라의 일반 컬러(RGB) 화면을 띄우고 이미지를 저장합니다.
* `02_cam_save_image_depth.py`: 인텔 카메라의 깊이(Depth) 센서를 활용하여 거리 정보가 포함된 화면을 띄우고 이미지를 저장합니다.
* `requirements.txt`: 인텔 카메라 구동에 필요한 파이썬 패키지 목록입니다. (예: `pyrealsense2`, `opencv-python`)

### 2. `royche_cam/` (Royche 및 일반 웹캠 전용)
* `00_cam_num.py`: 연결된 웹캠의 장치 번호를 확인하는 스크립트입니다.
* `01_cam_save_image.py`: 웹캠 화면을 띄우고 RGB 이미지를 저장합니다.
* `requirements.txt`: 웹캠 구동에 필요한 파이썬 패키지 목록입니다. (예: `opencv-python`)

---

## 🚀 사용 방법 (이렇게 하면 됩니다!)

본 프로젝트는 **Ubuntu 환경**을 기준으로 작성되었습니다.

### Step 1. 패키지 설치
각 카메라 폴더에 있는 `requirements.txt`를 이용해 필요한 라이브러리를 먼저 설치해 주세요.
```bash
# 인텔 카메라를 사용할 경우
cd intel_cam
python3 -m venv [이름]
pip install -r requirements.txt

# 로이체 카메라를 사용할 경우
cd royche_cam
python3 -m venv [이름]
pip install -r requirements.txt
```

### Step 2. 실행
```bash
# 인텔 카메라 intel_cam/

# 인텔 카메라 상태 확인
00_cam_num.py 

# 사진 데이터셋 확보
01_cam_save_image_rgb.py
02_cam_save_image_depth.py
```
```bash
# 로이제 카메라 royche_cam/

# 로이제 카메라 상태 확인
00_cam_num.py 

# 사진 데이터셋 확보
01_cam_save_image.py
```

### 주의점

인텔 카메라 수정시 pyrealsense2 있는지 확인하기
없으면 IR 채널만 불러와서 출력될 가능성이 있음
```bash
pip install pyrealsense2
```

사진 데이터셋 dataset/images 에 저장됨


s를 누르면 연속 저장, 다시 s 를 누르면 연속 저장 중지 q를 누르면 종료

### github 주의!!!
Fork 하지 않고 git clone 하여 git push하지 않기

### github로 push 하는 법
VSCode에서 수정한 코드를 github에 push하는 법
1. git status 로 commit할 파일 이름 및 올리면 안될 파일이 있는지 확인

2. VSCode 에서 수정한 코드를 commit을 한다 (단 터미널에서 하든 VSCode에서 하든 한곳에서 작업 실행)
```bash
git add [파일 선택]
```
```bash
git commit -m "수정 사항 내용"
```

3. git status 로 마지만 확인

4. git push 하여 github에 등록

### github 협업(pull requests)
수정된 코드를 적용 시키는 법
1. github에서 왼쪽 상단에 있는 pull requests를 클릭

2. 왼쪽에 있는 New pull request 클릭

3. 자신이 올린 Commit을 선택

4. Merge 요청 보내기

### github pull (불러오기)
main branch를 불러와서 버전 맞추기
1. 메인 브랜치로 이돌
```bash
git checkout main
```

2. github에서 main branch 불러오기
```bash
git pull origin main
```

====================  
오류 발생 시  
수정 중인 파일이 있어서 pull을 할 수 없다

1. 
```bash
git stash               # 현재 수정 사항을 임시 보관함에 넣기
git pull origin main    # 최신 코드 가져오기
git stash pop           # 임시 보관했던 내 작업 다시 꺼내기
```

2. 이 방법으로 하면 충돌이 발생할 가능서 있음. 충돌 해결 후 commit 하기
```bash
git add .
git commit -m "작업 중인 내용 저장"
git pull origin main
```