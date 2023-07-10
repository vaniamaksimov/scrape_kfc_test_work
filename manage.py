from src.core.settings import settings
from src.utils.app_types import ModeToFunction


def main():
    args = settings.parser.parse_args()
    parser_mode = args.usage
    func = getattr(ModeToFunction, parser_mode)()
    func()


if __name__ == '__main__':
    main()
