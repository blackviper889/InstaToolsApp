import flet as ft
import pyotp
import instaloader
import threading
import time

def main(page: ft.Page):
    page.title = "Insta Turbo Tools"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "auto"

    user_input = ft.TextField(label="Usernames (Bulk)", multiline=True, min_lines=3, border_color="blue")
    pass_input = ft.TextField(label="Common Password", password=True, can_reveal_password=True, border_color="blue")
    key_input = ft.TextField(label="2FA Keys (Bulk)", multiline=True, min_lines=3, border_color="blue")
    
    status_text = ft.Text("Status: Ready", size=18, weight="bold", color="white")
    stats_label = ft.Text("✅ Success: 0 | ❌ Failed: 0", size=16, color="amber")

    success_area = ft.TextField(label="Success Box (Cookies)", multiline=True, min_lines=8, read_only=True, border_color="green")
    failed_area = ft.TextField(label="Failed List", multiline=True, min_lines=4, read_only=True, border_color="red")

    def start_process(e):
        usernames = [u.strip() for u in user_input.value.split('\n') if u.strip()]
        password = pass_input.value.strip()
        keys = [k.strip().replace(" ", "").upper() for k in key_input.value.split('\n') if k.strip()]

        if not usernames or not password or len(usernames) != len(keys):
            status_text.value = "⚠️ Error: Input Mismatch!"
            status_text.color = "red"
            page.update()
            return

        status_text.value = "⚡ Extracting..."
        status_text.color = "blue"
        success_area.value = ""
        failed_area.value = ""
        page.update()

        s_count = 0
        f_count = 0
        
        for i in range(len(usernames)):
            user = usernames[i]
            key = keys[i]
            try:
                L = instaloader.Instaloader()
                totp = pyotp.TOTP(key).now()
                L.login(user, password)
                cookies = L.context._session.cookies.get_dict()
                cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
                
                success_area.value += f"{user}|{password}|{cookie_str}\n"
                s_count += 1
            except:
                failed_area.value += f"{user} - Failed\n"
                f_count += 1
            
            stats_label.value = f"✅ Success: {s_count} | ❌ Failed: {f_count}"
            page.update()

        status_text.value = "✅ Done!"
        status_text.color = "green"
        page.update()

    page.add(
        ft.Text("🚀 INSTA COOKIE EXTRACTOR", size=22, weight="bold", color="blue"),
        user_input, pass_input, key_input,
        ft.ElevatedButton("START EXTRACTING", on_click=start_process, width=400, height=50, bgcolor="blue", color="white"),
        ft.Divider(),
        status_text, stats_label,
        ft.Text("Success Results:"),
        success_area,
        ft.ElevatedButton("Copy Success", icon=ft.icons.COPY, on_click=lambda _: page.set_clipboard(success_area.value)),
        ft.Text("Failed IDs:"),
        failed_area,
        ft.ElevatedButton("Copy Failed", icon=ft.icons.COPY, on_click=lambda _: page.set_clipboard(failed_area.value)),
    )

ft.app(target=main)
