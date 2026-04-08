# 캠 모델 확인 및 USB 타입 파악

import pyrealsense2 as rs

print("🔍 RealSense 장치 스캔 중...")
ctx = rs.context()
devices = ctx.query_devices()

if len(devices) == 0:
    print("❌ 연결된 RealSense 카메라를 찾을 수 없습니다. 케이블을 다시 꽂아주세요.")
else:
    for dev in devices:
        name = dev.get_info(rs.camera_info.name)
        usb_type = dev.get_info(rs.camera_info.usb_type_descriptor)
        
        print(f"\n✅ 장치 이름: {name}")
        print(f"🔌 USB 연결 상태: USB {usb_type}")
        
        if "2." in usb_type:
            print("⚠️ [경고] USB 2.1 하위 버전으로 연결되어 있습니다.")
            print("   -> 대역폭이 부족해 FHD 해상도 스트리밍 시 I/O 에러가 발생합니다.")
            print("   -> 본체 뒷면 메인보드의 파란색 USB 3.0 포트에 직접 꽂거나 케이블을 교체해 보세요.")
        elif "3." in usb_type:
            print("🚀 [성공] USB 3.0 이상으로 완벽하게 연결되었습니다! 고해상도 사용이 가능합니다.")