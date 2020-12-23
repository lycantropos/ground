from hypothesis import strategies

from ground.geometrical import get_context

contexts = strategies.just(get_context())
