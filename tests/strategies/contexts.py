from fractions import Fraction
from numbers import Rational

from hypothesis import strategies as st
from symba.base import sqrt

from ground.base import Context

from .coordinates import rational_coordinates_strategies

rational_contexts = st.builds(
    Context,
    coordinate_checker=st.just(Rational.__instancecheck__),
    coordinate_factory=st.just(Fraction),
    sqrt=st.just(sqrt),
)
rational_contexts_with_coordinates_strategies = st.tuples(
    rational_contexts, rational_coordinates_strategies
)
contexts_with_coordinates_strategies = (
    rational_contexts_with_coordinates_strategies
)
