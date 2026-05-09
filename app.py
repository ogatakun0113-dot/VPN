import socket
import re
import os

# --- 設定項目 ---
# ルーターのDDNSアドレス
DDNS_HOSTNAME = "ogata-vezel.asuscomm.com"
# 書き換え対象のファイル名（同じフォルダに置いてください）
OVPN_FILE = "client (3) (1).ovpn"
# ポート番号（固定）
PORT = "1194"

def update_ovpn_remote():
    try:
        # 1. DDNSから最新のIPアドレスを逆引き
        print(f"Checking IP for {DDNS_HOSTNAME}...")
        current_ip = socket.gethostbyname(DDNS_HOSTNAME)
        print(f"Current WAN IP: {current_ip}")

        if not os.path.exists(OVPN_FILE):
            print(f"エラー: {OVPN_FILE} が見つかりません。")
            return

        # 2. ファイルを読み込む
        with open(OVPN_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 3. remote行を書き換える
        new_lines = []
        replaced = False
        # 正規表現で "remote [IP/Host] [Port]" の行を探す
        pattern = re.compile(r'^remote\s+\S+\s+\d+')

        for line in lines:
            if pattern.match(line):
                new_lines.append(f"remote {current_ip} {PORT}\n")
                replaced = True
            else:
                new_lines.append(line)

        # 4. ファイルを上書き保存
        if replaced:
            with open(OVPN_FILE, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"成功: {OVPN_FILE} の接続先を {current_ip} に更新しました！")
        else:
            print("警告: ファイル内に 'remote' 設定行が見つかりませんでした。")

    except socket.gaierror:
        print("エラー: DDNSの解決に失敗しました。ネット接続やアドレスを確認してください。")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    update_ovpn_remote()
