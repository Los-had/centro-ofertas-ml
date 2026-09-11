def format_deal(
    product,
    deal,
):

    return f"""
🔥 OFERTA ENCONTRADA

📦 {product.title}

💰 Por: R$ {product.current_price:.2f}

📊 Qualidade da oferta: {deal.score}/100

🏷️ Desconto histórico:
{deal.discount_percent:.1f}%

⭐ Avaliação:
{product.rating or "N/A"}

🛒 Comprar:
{product.url}

⚡ Pode acabar a qualquer momento.
""".strip()