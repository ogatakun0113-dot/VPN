import streamlit as st
import socket
import re

# --- 設定項目 ---
DDNS_HOSTNAME = "ogata-vezel.asuscomm.com"
PORT = "1194"

st.set_page_config(page_title="VPN Config Updater", page_icon="🌐")

st.title("🌐 VPN設定ファイル更新")
st.write(f"現在のルーター ({DDNS_HOSTNAME}) のIPを取得して、設定ファイルを更新します。")

# 1. 接続元の .ovpn ファイルをアップロードしてもらう
uploaded_file = st.file_uploader("元の .ovpn ファイルを選択してください", type=['ovpn'])

if uploaded_file is not None:
    try:
        # 2. DDNSから最新のIPアドレスを取得
        current_ip = socket.gethostbyname(DDNS_HOSTNAME)
        st.success(f"最新のWAN IPを確認しました: **{current_ip}**")

        # 3. ファイルの中身を読み込む
        content = uploaded_file.read().decode("utf-8")
        lines = content.splitlines()

        # 4. remote行を書き換える
        new_lines = []
        replaced = False
        pattern = re.compile(r'^remote\s+\S+\s+\d+')

        for line in lines:
            if pattern.match(line):
                new_lines.append(f"remote {current_ip} {PORT}")
                replaced = True
            else:
                new_lines.append(line)

        final_content = "\n".join(new_lines)

        if replaced:
            st.info("設定の書き換えが完了しました。")
            
            # 5. ダウンロードボタンを表示
            st.download_button(
                label="✅ 更新されたファイルをダウンロード",
                data=final_content,
                file_name="updated_client.ovpn",
                mime="application/x-openvpn-profile",
                use_container_width=True
            )
        else:
            st.error("ファイル内に 'remote' 設定行が見つかりませんでした。設定ファイルを確認してください。")

    except socket.gaierror:
        st.error("DDNSの解決に失敗しました。ルーターのドメイン名が正しいか確認してください。")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

st.markdown("---")
st.caption("スマホからでも、元のファイルをアップロードすれば最新版がダウンロードできます。")
