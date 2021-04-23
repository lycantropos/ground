import os
import platform

from hypothesis import (HealthCheck,
                        settings)

from .utils import IS_PYPY

on_azure_pipelines = bool(os.getenv('TF_BUILD', False))
settings.register_profile('default',
                          max_examples=(settings.default.max_examples
                                        // 5 * (1 + 4 * IS_PYPY)
                                        if on_azure_pipelines
                                        else settings.default.max_examples),
                          deadline=None,
                          suppress_health_check=[HealthCheck.filter_too_much,
                                                 HealthCheck.too_slow])
