from hypothesis import strategies

from ground.base import Relation

relations = strategies.sampled_from(Relation)
