from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Category, Deal, PriceHistory, Product
from app.schemas import (
    CategoryCreate,
    CategoryResponse,
    DealResponse,
    PriceHistoryCreate,
    PriceHistoryResponse,
    ProductCreate,
    ProductResponse,
)

router = APIRouter()


@router.get("/test")
def test():
    return {
        "status": "ok",
        "message": "API funcionando",
    }


# ============================================================
# CATEGORIES
# ============================================================

@router.post("/categories", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):
    existing = db.scalar(
        select(Category).where(Category.slug == category.slug)
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Categoria já existe.",
        )

    new_category = Category(
        name=category.name,
        slug=category.slug,
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.scalars(
        select(Category).order_by(Category.name)
    ).all()


# ============================================================
# PRODUCTS
# ============================================================

@router.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    category = db.get(Category, product.category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada.",
        )

    if product.ml_item_id:
        existing = db.scalar(
            select(Product).where(
                Product.ml_item_id == product.ml_item_id
            )
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Produto do Mercado Livre já cadastrado.",
            )

    new_product = Product(**product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/products", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.scalars(
        select(Product).order_by(Product.id.desc())
    ).all()


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado.",
        )

    return product


# ============================================================
# PRICE HISTORY
# ============================================================

@router.post(
    "/products/{product_id}/prices",
    response_model=PriceHistoryResponse,
)
def add_price(
    product_id: int,
    price_data: PriceHistoryCreate,
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado.",
        )

    product.current_price = price_data.price

    history = PriceHistory(
        product_id=product_id,
        price=price_data.price,
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return history


@router.get(
    "/products/{product_id}/prices",
    response_model=list[PriceHistoryResponse],
)
def get_price_history(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado.",
        )

    return db.scalars(
        select(PriceHistory)
        .where(PriceHistory.product_id == product_id)
        .order_by(PriceHistory.recorded_at.desc())
    ).all()


# ============================================================
# DEALS
# ============================================================

@router.get("/deals", response_model=list[DealResponse])
def list_deals(db: Session = Depends(get_db)):
    return db.scalars(
        select(Deal).order_by(Deal.score.desc())
    ).all()

@router.post(
    "/products/{product_id}/evaluate",
    response_model=DealResponse,
)
def evaluate_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    from app.services.deals.scoring import calculate_deal_score

    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado.",
        )

    result = calculate_deal_score(
        db,
        product,
    )

    deal = Deal(
        product_id=product.id,
        score=result["score"],
        discount_percent=result["discount_percent"],
        status=result["status"],
        reason=result["reason"],
    )

    db.add(deal)
    db.commit()
    db.refresh(deal)

    return deal



@router.get("/mercadolivre/search")
def search_mercadolivre(
    q: str,
    limit: int = 20,
):
    from app.services.mercadolivre import MercadoLivreClient

    client = MercadoLivreClient()

    try:
        return client.search_items(
            query=q,
            limit=limit,
        )
    finally:
        client.close()

@router.post("/mercadolivre/import/{item_id}")
def import_mercadolivre_item(
    item_id: str,
    db: Session = Depends(get_db),
):
    from app.services.mercadolivre.collector import (
        import_item,
    )

    product = import_item(
        db,
        item_id,
    )

    return {
        "status": "imported",
        "product_id": product.id,
        "title": product.title,
        "price": product.current_price,
        "ml_item_id": product.ml_item_id,
    }