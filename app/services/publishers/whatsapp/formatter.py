def format_deal(product, deal):
    return (
        "🔥 OFERTA ENCONTRADA\n\n"
        f"📦 {product.title}\n\n"
        f"💰 Por: R$ {product.current_price:.2f}\n\n"
        f"📊 Qualidade da oferta: {deal.score}/100\n"
        f"🏷️ Desconto histórico: {deal.discount_percent:.1f}%\n"
        f"⭐ Avaliação: {product.rating or 'N/A'}\n\n"
        f"🛒 Comprar:\n{product.url}\n\n"
        "⚡ Pode acabar a qualquer momento."
    )