from pydantic.v1.networks import MultiHostDsn


class SqliteDsn(MultiHostDsn):
    allowed_schemes = {
        'sqlite+aiosqlite',
        'sqlite+pysqlite',
    }
    host_required = False

    @classmethod
    def build(cls, *, scheme: str, path: str) -> str:
        url = scheme + ':///' + path
        return url
