from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category, PriceHistory, Product

from app.services.mercadolivre import MercadoLivreClient


def import_item(
    db: Session,
    item_id: str,
):
    client = MercadoLivreClient()

    try:
        item = client.get_item(item_id)
    finally:
        client.close()

    title = item.get("title", "Produto")

    price = item.get("price")

    if price is None:
        raise ValueError(
            "Produto sem preço."
        )

    category_ml_id = item.get(
        "category_id",
        "unknown",
    )

    category_slug = (
        f"ml-{category_ml_id}".lower()
    )

    category = db.scalar(
        select(Category).where(
            Category.slug == category_slug
        )
    )

    if not category:

        category = Category(
            name=f"Mercado Livre {category_ml_id}",
            slug=category_slug,
        )

        db.add(category)
        db.commit()
        db.refresh(category)

    product = db.scalar(
        select(Product).where(
            Product.ml_item_id == item_id
        )
    )

    if product:

        product.current_price = price

        product.original_price = item.get(
            "original_price"
        )

        product.stock_quantity = item.get(
            "available_quantity"
        )

        product.sold_quantity = (
            item.get("sold_quantity", 0)
            or 0
        )

        product.url = item.get(
            "permalink"
        )

    else:

        pictures = item.get(
            "pictures",
            [],
        )

        image_url = None

        if pictures:
            image_url = pictures[0].get(
                "url"
            )

        product = Product(
            ml_item_id=item_id,
            title=title,
            url=item.get("permalink"),
            image_url=image_url,
            current_price=price,
            original_price=item.get(
                "original_price"
            ),
            rating=None,
            review_count=0,
            sold_quantity=(
                item.get("sold_quantity", 0)
                or 0
            ),
            stock_quantity=item.get(
                "available_quantity"
            ),
            category_id=category.id,
        )

        db.add(product)
        db.commit()
        db.refresh(product)

    history = PriceHistory(
        product_id=product.id,
        price=price,
    )

    db.add(history)

    db.commit()

    return product