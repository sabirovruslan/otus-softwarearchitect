import os

from flask import json, Flask


def init_config(app: Flask, env=None, db_engines=None):
    """
    :param app: Flask
    :param env: DEFAULT|TEST|LOCAL
    :param db_engines: ['postgresql', 'sql_alchemy']
    :return:
    """

    config_db_initializers = {'postgresql': __psql}

    env_config: dict = {k: v for k, v in os.environ.items()}
    file_config = __read_config_from_file(app, env)
    config = {**file_config, **env_config}

    for engine in db_engines or []:
        callback = config_db_initializers.get(engine)

        config = callback(config)

    formatting_env = {}
    if config.get('ENV_FORMATING'):
        formatting_env = json.loads(config.get('ENV_FORMATING'))

    for key, envs in formatting_env.items():
        if key in config and isinstance(config[key], str):
            config[key] = config[key].format(**{e: os.environ.get(e, '') for e in envs})

    app.config.from_mapping(config)


def __read_config_from_file(app: Flask, env: str) -> dict:
    import configparser

    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read(os.path.join(app.config.root_path, 'config.ini'))
    env = str(env or os.environ.get('ENV', '')).upper()
    config = dict(parser.items('DEFAULT'))
    if parser.has_section(env):
        config.update(dict(parser.items(env)))

    return config


def __psql(config: dict):
    return __sql_alchemy(config, query='?client_encoding=utf8')


def __sql_alchemy(config: dict, query='?charset=utf8'):
    from sqlalchemy.engine.url import URL

    config['SQLALCHEMY_DATABASE_URI'] = (
            str(
                URL(
                    drivername=config.get('DB_DRIVERNAME'),
                    database=config.get('DB_DATABASE'),
                    host=config.get('DB_HOST'),
                    username=config.get('DB_USERNAME'),
                    password=config.get('DB_PASSWORD'),
                    port=config.get('DB_PORT'),
                )
            )
            + query  # noqa W503
    )

    return config
