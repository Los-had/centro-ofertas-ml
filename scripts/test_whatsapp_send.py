from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parents[1]
SESSION_DIR = BASE_DIR / "whatsapp_session"

TARGET = "Ofertas Pesca"

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=str(SESSION_DIR),
        headless=False,
    )

    page = context.pages[0] if context.pages else context.new_page()

    page.goto("https://web.whatsapp.com")

    print("WhatsApp Web aberto.")
    print("Aguardando carregamento...")
    page.wait_for_timeout(8000)

    matches = page.get_by_text(TARGET, exact=False)

    print("Correspondências:", matches.count())

    if matches.count() == 0:
        print("Grupo não encontrado.")
        input("ENTER para encerrar...")
        context.close()
        raise SystemExit

    for i in range(matches.count()):
        try:
            print(
                f"[{i}] texto = {matches.nth(i).inner_text()!r} | "
                f"visível = {matches.nth(i).is_visible()}"
            )
        except Exception as e:
            print(f"[{i}] erro: {e}")

    target = matches.filter(visible=True).first

    print("\nClicando no grupo...")
    target.click()

    page.wait_for_timeout(2000)

    print("Grupo aberto!")
    print("URL:", page.url)

    input("\nENTER para fechar sem enviar mensagem...")

    context.close()