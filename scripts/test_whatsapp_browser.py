from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parents[1]
SESSION_DIR = BASE_DIR / "whatsapp_session"


with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=str(SESSION_DIR),
        headless=False,
    )

    page = context.pages[0] if context.pages else context.new_page()

    page.goto("https://web.whatsapp.com")

    print("WhatsApp Web aberto.")
    print("Faça o login/QR Code se necessário.")
    print("Pressione Ctrl+C no terminal para encerrar.")

    try:
        while True:
            page.wait_for_timeout(100)
    except KeyboardInterrupt:
        context.close()