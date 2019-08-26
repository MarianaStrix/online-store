import environ

__all__ = (
    'env',
)

env = environ.Env(DEBUG=(bool, False),)

env.read_env(
    env.path(
        'ENV_FILE_PATH',
        default=(environ.Path(__file__) - 1).path('.env')()
    )())
