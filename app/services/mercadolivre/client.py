import random
import time

import httpx

from app.core.config import (
    ML_ACCESS_TOKEN,
    ML_SITE_ID,
)


class MercadoLivreError(Exception):
    pass


class MercadoLivreRateLimitError(MercadoLivreError):
    pass


class MercadoLivreClient:

    BASE_URL = "https://api.mercadolibre.com"

    def __init__(
        self,
        access_token: str | None = None,
    ):
        self.access_token = (
            access_token
            or ML_ACCESS_TOKEN
        )

        self.client = httpx.Client(
            timeout=20,
            headers=self._headers(),
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

    def _request(
        self,
        method: str,
        path: str,
        **kwargs,
    ):
        max_retries = 3

        for attempt in range(max_retries):

            response = self.client.request(
                method,
                f"{self.BASE_URL}{path}",
                **kwargs,
            )

            if response.status_code == 429:

                if attempt == max_retries - 1:
                    raise MercadoLivreRateLimitError(
                        "Mercado Livre retornou 429."
                    )

                delay = (
                    2 ** attempt
                    + random.uniform(0, 1)
                )

                time.sleep(delay)

                continue

            if response.status_code >= 400:
                raise MercadoLivreError(
                    f"Mercado Livre HTTP "
                    f"{response.status_code}: "
                    f"{response.text}"
                )

            return response.json()

        raise MercadoLivreError(
            "Falha inesperada na requisição."
        )

    def search_items(
        self,
        query: str,
        limit: int = 20,
    ):
        limit = min(limit, 50)

        return self._request(
            "GET",
            f"/sites/{ML_SITE_ID}/search",
            params={
                "q": query,
                "limit": limit,
            },
        )

    def get_item(
        self,
        item_id: str,
    ):
        return self._request(
            "GET",
            f"/items/{item_id}",
        )

    def close(self):
        self.client.close()