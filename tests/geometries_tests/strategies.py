from hypothesis import strategies

from ground.geometries import get_context

contexts = strategies.just(get_context())
