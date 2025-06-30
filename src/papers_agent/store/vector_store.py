from __future__ import annotations
from functools import lru_cache
import pathlib, faiss
from langchain_community.vectorstores.faiss import FAISS, InMemoryDocstore
from langchain_openai import OpenAIEmbeddings

VEC_DIR = pathlib.Path("data/app/faiss")
VEC_DIR.mkdir(parents=True, exist_ok=True)

@lru_cache(maxsize=1)
def _embedder():
    return OpenAIEmbeddings(model="text-embedding-3-small")

def _new_empty_vs() -> FAISS:
    dim = len(_embedder().embed_query("placeholder"))
    index = faiss.IndexFlatL2(dim)
    docstore = InMemoryDocstore({})
    index_to_docstore_id: dict[int, str] = {}
    return FAISS(_embedder(), index, docstore, index_to_docstore_id)

def get_vs() -> FAISS:
    if (VEC_DIR / "index.faiss").exists():
        return FAISS.load_local(
            VEC_DIR, _embedder(), allow_dangerous_deserialization=True
        )
    vs = _new_empty_vs()
    vs.save_local(VEC_DIR)
    return vs

def add_paper(pmid: str, abstract: str):
    vs = get_vs()
    vs.add_texts([abstract], metadatas=[{"pmid": pmid}])
    vs.save_local(VEC_DIR)
