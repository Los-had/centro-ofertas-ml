import httpx

from app.core.config import (
    ML_ACCESS_TOKEN,
    ML_SITE_ID,
)


class MercadoLivreClient:

    BASE_URL = "https://api.mercadolibre.com"

    def __init__(self, access_token: str | None = None):
        self.access_token = (
            access_token
            or ML_ACCESS_TOKEN
        )

    def _headers(self):
        headers = {
            "Accept": "application/json",
        }

        if self.access_token:
            headers["Authorization"] = (
                f"Bearer {self.access_token}"
            )

        return headers

    def get_item(self, item_id: str):
        response = httpx.get(
            f"{self.BASE_URL}/items/{item_id}",
            headers=self._headers(),
            timeout=20,
        )

        response.raise_for_status()

        return response.json()

    def search_items(
        self,
        query: str,
        limit: int = 20,
    ):
        response = httpx.get(
            f"{self.BASE_URL}/sites/{ML_SITE_ID}/search",
            params={
                "q": query,
                "limit": min(limit, 50),
            },
            headers=self._headers(),
            timeout=20,
        )

        response.raise_for_status()

        return response.json()

    def get_category(self, category_id: str):
        response = httpx.get(
            f"{self.BASE_URL}/categories/{category_id}",
            headers=self._headers(),
            timeout=20,
        )

        response.raise_for_status()

        return response.json()