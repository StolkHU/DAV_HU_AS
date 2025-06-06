import numpy as np
import seaborn as sns
from loguru import logger
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import manhattan_distances


class TextClustering:
    def __init__(self):
        self.vectorizer = CountVectorizer(analyzer="char", ngram_range=(3, 3))

    def __call__(
        self, text: list[str], k: int, labels: list, batch: bool, method: str = "PCA"
    ) -> None:
        if batch:
            text = self.batch_seq(text, k)
        distance = self.fit(text)
        x = self.reduce_dims(distance, method)
        self.plot(x, labels)

    def batch_seq(self, text: list[str], k: int) -> list[str]:
        longseq = " ".join(text)
        n = int(len(longseq) / k)
        logger.info(f"Splitting text into {k} parts of {n} characters each")
        parts = [longseq[i : i + n] for i in range(0, len(longseq), n)]
        if len(parts) > k:
            logger.info(f"Removing {len(parts) - k} parts")
            parts = parts[:k]
        return parts

    def fit(self, parts: list[str]) -> np.ndarray:
        x = self.vectorizer.fit_transform(parts)
        logger.info(f"Vectorized text into shape {x.shape}")
        x = np.asarray(x.todense())
        distance = manhattan_distances(x, x)
        return distance

    def reduce_dims(self, distance: np.ndarray, method: str = "PCA") -> np.ndarray:
        if method == "PCA":
            logger.info("Using PCA")
            model = PCA(n_components=2)
        else:
            logger.info("Using t-SNE")
            model = TSNE(n_components=2)
        x = model.fit_transform(distance)
        return x

    def plot(self, x: np.ndarray, labels: list) -> None:
        sns.scatterplot(x=x[:, 0], y=x[:, 1], hue=labels)
