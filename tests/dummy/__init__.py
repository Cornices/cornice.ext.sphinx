# -*- coding: utf-8 -*-

from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.include('cornice')
    config.include('tests.dummy.views.includeme')
    return config.make_wsgi_app()


if __name__ == '__main__':
    main()
