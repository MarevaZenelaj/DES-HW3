from random import randint
from random import expovariate
exponential_lambda = 0.3347536271959042

def randomNumber(lowerLimit, upperLimit,k):
    seed = 0
    m = 100
    a = 21
    c = 49
    y = seed
    list_numbers = {y}
    for i in range(k):
        y = (y*a+c) % m
        list_numbers.add(y)    
    return list_numbers

def customRandomNumber(lowerLimit, upperLimit):
    sequence = list(randomNumber(lowerLimit, upperLimit,100000))
    index = int(randint(0, len(sequence)-1))
    return sequence[index]*(upperLimit-lowerLimit)/100+ lowerLimit


class Entity:

    def __init__(self):
        self.target = None
        self.type = 'Entity'
        self.target = None


class DisplaceEntity(Entity):

    def __init__(self, from_place, to):
        super().__init__()
        self.from_place = from_place  # cabbages_on_shelf
        self.to = to  # cabbage_reorder_proc
        self.firstchoice = None
        self.secondchoice = None
        self.type = 'Displacement'

    def set_target(self, target):
        self.target = target

    def add_transition(self, firstchoicehappy, alternative):
        self.firstchoice = firstchoicehappy
        self.secondchoice = alternative


class GenerateAtStart(Entity):

    def __init__(self, num):
        super().__init__()
        self.type = 'cabbageGeneration'
        self.num = num

    def set_target(self, target):
        self.target = target


class AdvanceTimeUniformDistributionRotten(Entity):

    def __init__(self, low, high):
        super().__init__()
        self.count = 0
        self.type = 'cabbageRotten'
        self.low = low
        self.high = high

    def set_target(self, target):
        self.target = target

    def return_random(self):
        return customRandomNumber(self.low, self.high)


class AdvanceTimeUniformDistributionReordered(Entity):

    def __init__(self, low, high):
        super().__init__()
        self.count = 0
        self.type = 'cabbageArrived'
        self.low = low
        self.high = high

    def set_target(self, target):
        self.target = target

    def return_random(self):
        return customRandomNumber(self.low, self.high)


class GenerateEntityUniformDistribution(Entity):

    def __init__(self):
        super().__init__()
        self.type = 'CustEntry'

    def set_target(self, target):
        self.target = target

    def returnrand(self):
        return expovariate(exponential_lambda)


class EntityCounter(Entity):

    def __init__(self):
        super().__init__()
        self.total_count = 0
        self.type = 'Counter'

    def set_target(self, target):
        self.target = target

    def increase_counter(self):
        self.total_count += 1

    def count(self):
        return self.total_count


class TerminateEntity(Entity):

    def __init__(self):
        super().__init__()
        self.customersLeft = 0
        self.type = 'Termination'

    def increase_number(self):
        self.customersLeft += 1

    def set_target(self, target):
        self.target = target

    def count(self):
        return self.customersLeft


class Simulation:

    def __init__(self, firstcustomer, firstcabbage):
        self.firstcustomer = firstcustomer
        self.firstcabbage = firstcabbage
        self.clock = 0
        self.stock = firstcabbage.num
        self.future_event_list = []
        self.future_event_list.append((self.firstcustomer, self.clock + self.firstcustomer.returnrand()))
        self.future_event_list.append((self.firstcabbage.target, self.clock + self.firstcabbage.target.return_random()))

    def process_cabbage_rotten(self, next_event):
        self.stock -= 1
        next_event[0].target.total_count += 1
        newitem = AdvanceTimeUniformDistributionReordered(next_event[0].target.target.low, next_event[0].target.target.high)
        newitem.set_target(next_event[0].target.target.target)
        self.future_event_list.append((newitem, self.clock + newitem.return_random()))

    def process_cabbage_arrived(self, next_event):
        self.stock += 1
        rotten_cabbage = AdvanceTimeUniformDistributionRotten(next_event[0].target.low,
                                                              next_event[0].target.low)
        rotten_cabbage.set_target(next_event[0].target.target)
        self.future_event_list.append((rotten_cabbage, self.clock + rotten_cabbage.return_random()))

    def process_entry_event(self, next_event):
        self.future_event_list.append((next_event[0].target, self.clock))

    def get_cabbages_displacement(self, next_event):
        if self.stock == 0:
            next_event[0].secondchoice.total_count += 1
            self.future_event_list.append((next_event[0].secondchoice, self.clock))
        else:
            next_event[0].firstchoice.total_count += 1
            self.future_event_list.append((next_event[0].firstchoice, self.clock))
            self.stock -= 1

        new_entity = AdvanceTimeUniformDistributionReordered(next_event[0].to.low, next_event[0].to.high)
        new_entity.set_target(next_event[0].to.target)
        self.future_event_list.append((new_entity, self.clock + new_entity.return_random()))

        new_customer = GenerateEntityUniformDistribution()
        new_customer.set_target(self.firstcustomer.target)
        self.future_event_list.append((new_customer, self.clock + new_customer.returnrand()))

    def process_counter_event(self, next_event):
        next_event[0].total_count += 1
        self.future_event_list.append((next_event[0].target, self.clock))

    def process_entry_cabbage(self, next_event):
        self.stock = next_event[0].num
        self.future_event_list.append((next_event[0].target, self.clock))

    def process_termination_event(self, next_event):
        next_event[0].customersLeft += 1
        self.future_event_list.append((next_event[0].target, self.clock))

    def run(self, stop_after):
        counterr = 0
        tobeconditioned = stop_after[0].count()
        limit = stop_after[1]
        while len(self.future_event_list) != 0 and tobeconditioned < limit:
            self.future_event_list.sort(key=lambda x: x[1])
            next_event = self.future_event_list[0]
            if next_event[0] is None:
                del self.future_event_list[0]
                continue
            del self.future_event_list[0]
            self.clock = next_event[1]

            if next_event[0].type == 'CustEntry':
                self.process_entry_event(next_event)

            elif next_event[0].type == 'Counter':
                self.process_counter_event(next_event)

            elif next_event[0].type == 'Termination':
                self.process_termination_event(next_event)

            elif next_event[0].type == 'cabbageGeneration':
                self.process_entry_cabbage(next_event)

            elif next_event[0].type == 'cabbageRotten':
                self.process_cabbage_rotten(next_event)

            elif next_event[0].type == 'cabbageArrived':
                self.process_cabbage_arrived(next_event)

            elif next_event[0].type == 'Displacement':
                self.get_cabbages_displacement(next_event)

            tobeconditioned = stop_after[0].count()
            counterr += 1