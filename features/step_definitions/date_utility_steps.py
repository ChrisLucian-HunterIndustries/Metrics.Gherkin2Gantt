from aloe import before, step, world
from datetime import date

from Utilities.DateUtilities import month_delta


@before.each_example
def clear(*args):
    world.date = None
    world.delta = None
    world.result = None

@step(r'Given date "(\d+)/(\d+)/(\d+)" and delta "(\d+)"')
def enter_number(self, month, day, year, delta):
    the_date = date(int(year), int(month), int(day))
    world.date = the_date
    world.delta = int(delta)


@step(r'When I get the date delta')
def press_add(self):
    world.result = month_delta(world.date, world.delta)


@step(r'Then the result should be "(\d+)/(\d+)/(\d+)"')
def assert_result(self, month, day, year):
    assert world.result == date(int(year), int(month), int(day))
