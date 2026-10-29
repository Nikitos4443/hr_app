from config import DB_PROVIDER

from .IDatabaseProvider import IDatabaseProvider
from .sql.SQLDatabaseProvider import get_sql_provider

_PROVIDERS = {
    "sql": get_sql_provider,
}

try:
    get_provider = _PROVIDERS[DB_PROVIDER]
except KeyError as e:
    raise RuntimeError(f"Unknown DB_PROVIDER: {DB_PROVIDER!r}") from e

__all__ = ["IDatabaseProvider", "get_provider"]
