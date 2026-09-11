from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Deal, Product

from app.services.deals.scoring import (
    calculate_deal_score,
)


def evaluate_product(
    db: Session,
    product: Product,
):

    result = calculate_deal_score(
        db,
        product,
    )

    deal = Deal(
        product_id=product.id,
        score=result["score"],
        discount_percent=result[
            "discount_percent"
        ],
        status=result["status"],
        reason=result["reason"],
    )

    db.add(deal)
    db.commit()
    db.refresh(deal)

    return deal


def evaluate_all_products(
    db: Session,
):

    products = db.scalars(
        select(Product).where(
            Product.active == True
        )
    ).all()

    results = []

    for product in products:

        deal = evaluate_product(
            db,
            product,
        )

        results.append(deal)

    return results