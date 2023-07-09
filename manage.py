from src.core.settings import settings
from src.utils.app_types import ModeToFunction


def main():
    args = settings.parser.parse_args()
    parser_mode = args.usage
    getattr(ModeToFunction, parser_mode)()


if __name__ == '__main__':
    main()
