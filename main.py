from fastapi import FastAPI
from typing import List
from model import Article, ArticleUpdateRequest
from uuid import UUID, uuid4
from http.client import HTTPException


app = FastAPI()

db: List[Article] = [
    Article(id=uuid4(), designation="Article-01",
            numero="AZE-4589", qc=10, qpc=20)
]


@app.get("/")
def root():
    return {"wording": "Hello world"}


@app.get("/api/v1/articles")
async def get_articles():
    return db


@app.post("/api/v1/articles")
async def create_article(article: Article):
    db.append(article)
    return article


@app.delete("/api/v1/articles/{article_id}")
async def delete_article(article_id: UUID):
    for article in db:
        if article.id == article_id:
            db.remove(article)
            return
    raise HTTPException(
        status_code=404,
        detail=f"Article with id {article_id} not found"
    )


@app.put("/api/v1/articles/{article_id}")
async def update_article(art: ArticleUpdateRequest, article_id: UUID):
    for a in db:
        if a.id == article_id:
            if art.numero is not None:
                a.numero = art.numero
            if art.designation is not None:
                a.designation = art.designation
            if art.qc is not None:
                a.qc = art.qc
            if art.qpc is not None:
                a.qpc = art.apc
            return a
        raise HTTPException(
            status_code=404,
            detail=f"Article with id {article_id} not found"
        )
