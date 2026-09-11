from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import PriceHistory, Product


def calculate_deal_score(
    db: Session,
    product: Product,
) -> dict:

    history = db.scalars(
        select(PriceHistory)
        .where(PriceHistory.product_id == product.id)
        .order_by(PriceHistory.recorded_at.desc())
    ).all()

    if not history:
        return {
            "score": 0,
            "discount_percent": 0,
            "status": "insufficient_data",
            "reason": "Ainda não existe histórico de preços.",
        }

    prices = [item.price for item in history]

    highest_price = max(prices)
    lowest_price = min(prices)

    now = datetime.utcnow()
    recent_cutoff = now - timedelta(days=30)

    recent_prices = [
        item.price
        for item in history
        if item.recorded_at >= recent_cutoff
    ]

    recent_low = (
        min(recent_prices)
        if recent_prices
        else lowest_price
    )

    # --------------------------------------------------------
    # Desconto histórico
    # --------------------------------------------------------

    if highest_price > 0:
        historical_discount = (
            (highest_price - product.current_price)
            / highest_price
        ) * 100
    else:
        historical_discount = 0

    historical_discount = max(
        0,
        historical_discount,
    )

    score = 0
    reasons = []

    # Até 35 pontos
    score += min(
        historical_discount * 0.7,
        35,
    )

    if historical_discount >= 20:
        reasons.append(
            f"Preço {historical_discount:.1f}% abaixo "
            "do maior preço registrado."
        )

    # Até 30 pontos
    if product.current_price <= recent_low:
        score += 30

        reasons.append(
            "Preço está no menor nível registrado "
            "nos últimos 30 dias."
        )

    # --------------------------------------------------------
    # Avaliação
    # --------------------------------------------------------

    if product.rating is not None:

        if product.rating >= 4.8:
            score += 15
            reasons.append("Avaliação excelente.")

        elif product.rating >= 4.5:
            score += 10
            reasons.append("Boa avaliação.")

        elif product.rating >= 4.0:
            score += 5

    # --------------------------------------------------------
    # Número de avaliações
    # --------------------------------------------------------

    if product.review_count >= 1000:
        score += 10
        reasons.append(
            "Grande quantidade de avaliações."
        )

    elif product.review_count >= 100:
        score += 7

    elif product.review_count >= 20:
        score += 3

    # --------------------------------------------------------
    # Vendas
    # --------------------------------------------------------

    if product.sold_quantity >= 1000:
        score += 10
        reasons.append(
            "Produto possui alto volume de vendas."
        )

    elif product.sold_quantity >= 100:
        score += 6

    elif product.sold_quantity >= 20:
        score += 3

    score = min(
        round(score, 2),
        100,
    )

    if score >= 90:
        status = "publish"

    elif score >= 70:
        status = "review"

    elif score >= 50:
        status = "ignore"

    else:
        status = "weak"

    if not reasons:
        reasons.append(
            "Poucos sinais de oportunidade encontrados."
        )

    return {
        "score": score,
        "discount_percent": round(
            historical_discount,
            2,
        ),
        "status": status,
        "reason": " ".join(reasons),
    }