import pytest

import laxative_engine

engine = laxative_engine.LaxativeEngine()

def test_distance():
   assert engine.get_distance_metric("POOP", "POOP") == 0
   assert engine.get_distance_metric("POOP", "POOL") == 1
   assert engine.get_distance_metric("POOP", "PODS") == 2
   assert engine.get_distance_metric("POOP", "PANT") == 3
   assert engine.get_distance_metric("POOP", "RANT") == 4

def test_end_to_end():
   print(engine.get_reply_message("task"))

test_end_to_end()