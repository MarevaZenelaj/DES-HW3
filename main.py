from random import randint


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
        return randint(self.low, self.high)


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
        return randint(self.low, self.high)


class GenerateEntityUniformDistribution(Entity):

    def __init__(self, low, high):
        super().__init__()
        self.low = low
        self.high = high
        self.type = 'CustEntry'

    def set_target(self, target):
        self.target = target

    def returnrand(self):
        return randint(self.low, self.high)


class EntityCounter(Entity):

    def __init__(self):
        super().__init__()
        self.total_count = 0
        self.type = 'Counter'

    def set_target(self, target):
        self.target = target

    def increase_counter(self):
        self.total_count += 1


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

    def process_cabbage_rotten(self, next_event):
        print("entered")
        self.stock -= 1
        next_event[0].target.count += 1
        print(next_event[0].target.type)

    def process_cabbage_arrived(self, next_event):
        self.stock += 1

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
        self.future_event_list.append((cabbage_reorder_proc, self.clock + cabbage_reorder_proc.return_random()))
        self.future_event_list.append((cust_entry, self.clock + cust_entry.returnrand()))

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
            #print(f'processing event {next_event[0].type} at time {self.clock}')

            if next_event[0].type == 'CustEntry':
                self.process_entry_event(next_event)

            elif next_event[0].type == 'Counter':
                self.process_counter_event(next_event)

            elif next_event[0].type == 'Termination':
                self.process_termination_event(next_event)

            elif next_event[0].type == 'cabbageGeneration':
                self.process_entry_cabbage(next_event)

            elif next_event[0].type == 'cabbageRotten':
                print("entered")
                self.process_cabbage_rotten(next_event)

            elif next_event[0].type == 'cabbageArrived':
                self.process_cabbage_arrived(next_event)

            elif next_event[0].type == 'Displacement':
                self.get_cabbages_displacement(next_event)

            tobeconditioned = stop_after[0].count()
            counterr += 1


first_cabbages = GenerateAtStart(num=3)

cabbages_on_shelf = AdvanceTimeUniformDistributionRotten(low=7, high=12)

cabbage_rotten_cntr = EntityCounter()

cabbage_reorder_proc = AdvanceTimeUniformDistributionReordered(low=1, high=15)

first_cabbages.set_target(cabbages_on_shelf)

cabbages_on_shelf.set_target(cabbage_rotten_cntr)

cabbage_rotten_cntr.set_target(cabbage_reorder_proc)

cabbage_reorder_proc.set_target(cabbages_on_shelf)

cust_entry = GenerateEntityUniformDistribution(low=0, high=3)

cust_leave_happy_cntr = EntityCounter()

cust_leave_unhappy_cntr = EntityCounter()

cust_leave_happy = TerminateEntity()

cust_leave_unhappy = TerminateEntity()

get_cabbage = DisplaceEntity(from_place=cabbages_on_shelf, to=cabbage_reorder_proc)

cust_entry.set_target(get_cabbage)

get_cabbage.add_transition(cust_leave_happy_cntr, alternative=cust_leave_unhappy_cntr)

get_cabbage.set_target(cust_entry)

cust_leave_happy_cntr.set_target(cust_leave_happy)

cust_leave_unhappy_cntr.set_target(cust_leave_unhappy)


simulation = Simulation(cust_entry, first_cabbages)

simulation.run(stop_after=(cust_leave_happy, 10))

print(cust_leave_happy.count(), "customers went home happy with cabbages.")

print(cust_leave_unhappy.count(), "customers went home unhappy without cabbages.")

print(cabbage_rotten_cntr.total_count, "cabbages sadly went rotten.")
