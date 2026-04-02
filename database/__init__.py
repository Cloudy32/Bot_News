from database.queries import get_all_news, save_news
from database.session import init_db, make_session_factory

__all__ = ["init_db", "make_session_factory", "save_news", "get_all_news"]
