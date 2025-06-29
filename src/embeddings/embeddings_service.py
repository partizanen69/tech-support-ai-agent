from sentence_transformers import SentenceTransformer
from torch import Tensor


class EmbeddingsService:
    model: SentenceTransformer

    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def get_embedding(self, text: str) -> list[float]:
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding


embeddings_service = EmbeddingsService()
