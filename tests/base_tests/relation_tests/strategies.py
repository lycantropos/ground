from hypothesis import strategies

from ground.enums import Relation

relations = strategies.sampled_from(Relation)
