import socket
import re
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# --- 設定項目 ---
DDNS_HOSTNAME = "ogata-vezel.asuscomm.com"
OVPN_FILE = "client (3) (1).ovpn"
PORT = "1194"

def update_ovpn_remote():
    try:
        # 1. DDNSから最新のIPアドレスを取得
        print(f"Checking IP for {DDNS_HOSTNAME}...")
        current_ip = socket.gethostbyname(DDNS_HOSTNAME)
        print(f"Current WAN IP: {current_ip}")

        # 元のファイルがあるか確認
        if not os.path.exists(OVPN_FILE):
            print(f"エラー: {OVPN_FILE} が見つかりません。")
            return

        # 2. ファイルを読み込む
        with open(OVPN_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 3. 保存先をユーザーに尋ねる
        # tkinterのメインウィンドウを隠す
        root = tk.Tk()
        root.withdraw()
        
        # 保存ダイアログを表示
        save_path = filedialog.asksaveasfilename(
            title="更新後のファイルを保存する場所を選んでください",
            initialfile="updated_client.ovpn",
            defaultextension=".ovpn",
            filetypes=[("OpenVPN files", "*.ovpn"), ("All files", "*.*")]
        )

        if not save_path:
            print("保存がキャンセルされました。")
            return

        # 4. remote行を書き換える
        new_lines = []
        replaced = False
        pattern = re.compile(r'^remote\s+\S+\s+\d+')

        for line in lines:
            if pattern.match(line):
                new_lines.append(f"remote {current_ip} {PORT}\n")
                replaced = True
            else:
                new_lines.append(line)

        # 5. 指定された場所に別名で保存
        if replaced:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"成功: {save_path} に保存しました！")
            messagebox.showinfo("完了", f"接続先を {current_ip} に更新して保存しました。")
        else:
            print("警告: ファイル内に 'remote' 設定行が見つかりませんでした。")

    except socket.gaierror:
        messagebox.showerror("エラー", "DDNSの解決に失敗しました。")
    except Exception as e:
        messagebox.showerror("エラー", f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    update_ovpn_remote()
