import sys
import time
import math
import platform

# ==========================================
# 設定エリア: ここを書き換えてモードを切り替えます
# True: ダミーモード (実機なしでテスト)
# False: 実機モード (USB接続)
# ==========================================
IS_SIMULATION = True
# ==========================================

# 1. ダミー用クラスの定義 (シミュレーション用)
class DummyUtils:
    def rpm2rad_per_sec(self, rpm): return rpm * (2 * math.pi) / 60
    def rad_per_sec2rpm(self, rad): return rad * 60 / (2 * math.pi)
    def rad2deg(self, rad): return rad * 180 / math.pi

class DummyUARTController:
    def __init__(self, port):
        self.port = port
        print(f"[System] ポート {port} へ接続しました（シミュレーション）")
    def set_acc(self, id, val): print(f"  [設定] Motor {id}: 加速度 {val}")
    def set_dec(self, id, val): print(f"  [設定] Motor {id}: 減速度 {val}")
    def set_max_torque(self, id, val): print(f"  [設定] Motor {id}: 最大トルク {val}")
    def enable_action(self, id): print(f"  [状態] Motor {id}: ON (有効化)")
    def disable_action(self, id): print(f"  [状態] Motor {id}: OFF (無効化)")
    def run_at_velocity(self, id, rps):
        rpm = rps * 60 / (2 * math.pi)
        print(f"  [動作] Motor {id}: {'正転' if rpm >= 0 else '逆転'}速度 {abs(rpm):.1f} RPM")

# 2. モジュールの準備
if IS_SIMULATION:
    class DummyModule: pass
    pykeigan = DummyModule()
    pykeigan.uartcontroller = DummyModule()
    pykeigan.uartcontroller.UARTController = DummyUARTController
    pykeigan.utils = DummyUtils()
    sys.modules['pykeigan'] = pykeigan
    sys.modules['pykeigan.uartcontroller'] = pykeigan.uartcontroller
    sys.modules['pykeigan.utils'] = pykeigan.utils
else:
    from pykeigan import uartcontroller

# 3. ロボットクラスの読み込み
# (環境に合わせてインポートパスを適宜調整してください)
try:
    from motor_test.robot_2wd_new import Robot2WD
except ImportError:
    from robot_2wd_new import Robot2WD

def main():
    # ポート設定
    if IS_SIMULATION:
        L_PORT = "/dev/serial/by-id/dummy_left"
        R_PORT = "/dev/serial/by-id/dummy_right"
    else:
        # Windowsの場合は "COM3" 等に書き換えてください
        L_PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_B0001KJH-if00-port0"
        R_PORT = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_B003725S-if00-port0"

    print(f"--- モーター動作テスト開始 (モード: {'シミュレーション' if IS_SIMULATION else '実機'}) ---")
    
    try:
        robot = Robot2WD(L_PORT, R_PORT)
        robot.enable()
        
        test_rpm = 100
        print(f"走行開始: {test_rpm} RPM")
        robot.run(test_rpm, test_rpm)
        
        time.sleep(3.0)
        
        print("停止命令")
        robot.run_stop()
        robot.disable()
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    
    print("--- テスト終了 ---")

if __name__ == "__main__":
    main()