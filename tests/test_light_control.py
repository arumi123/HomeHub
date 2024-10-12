import pytest
import subprocess
import raspi.src.light_control

def test_get_command(capsys):
    # Get コマンドのテスト
    get_command('arg1', 'arg2')
    captured = capsys.readouterr()
    assert "Get command executed with args: arg1 arg2" in captured.out

def test_set_light_on(mocker):
    # subprocess.run をモック化
    mock_subprocess = mocker.patch('subprocess.run')
    
    # ライトをオンにする場合のテスト
    set_light_state(1)
    mock_subprocess.assert_called_once_with(['python3', '/var/lib/homebridge/irrp.py', '-p', '-g17', '-f', 'codes', 'light:on'], check=True)

def test_set_light_off(mocker):
    # subprocess.run をモック化
    mock_subprocess = mocker.patch('subprocess.run')
    
    # ライトをオフにする場合のテスト
    set_light_state(0)
    mock_subprocess.assert_called_once_with(['python3', '/var/lib/homebridge/irrp.py', '-p', '-g17', '-f', 'codes', 'light:off'], check=True)

def test_invalid_light_state():
    # 無効なライトの状態の場合のテスト
    with pytest.raises(ValueError, match="Invalid light state. Use 0 to turn off or 1 to turn on."):
        set_light_state(2)
