from django.db.models import Prefetch, QuerySet

from tabom.models import Article, Like


def create_an_article(title: str) -> Article:
    return Article.objects.create(title=title)


def get_an_article(user_id: int, article_id: int) -> Article:
    return Article.objects.prefetch_related(
        Prefetch("like_set", queryset=Like.objects.filter(user_id=user_id), to_attr="my_likes")
    ).get(id=article_id)


def get_article_list(user_id: int, offset: int, limit: int) -> QuerySet[Article]:
    return (
        Article.objects.order_by("-id")
        .prefetch_related(Prefetch("like_set", queryset=Like.objects.filter(user_id=user_id), to_attr="my_likes"))[
            offset : offset + limit
        ]
    )


def delete_an_article(article_id: int) -> None:
    Article.objects.filter(id=article_id).delete()
