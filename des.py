from random import randint

class Entity:

    def __init__(self):
        self.target = None

    def set_target(self,target):
        self.target = target


class DisplaceEntity(Entity):

    def __init__(self, From, to):
        super().__init__()
        self.taget = None
        self.From = From                  #cabbages_on_shelf
        self.to = to                      #cabbage_reorder_proc
        self.firstchoice = None
        self.secondchoice = None
        self.type = 'Displacement'
        
    def set_target(self,target):
        self.taget = target
        
    def add_transition(self,firstchoicehappy, alternative):
        self.firstchoice = firstchoicehappy
        self.secondchoice = alternative
        
        
class GenerateAtStart(Entity):

    def __init__(self, num):
        self.type = 'cabbageGeneration'
        self.num = num

    def set_target(self, target):
        self.target = target


class AdvanceTimeUniformDistribution(Entity):

    def __init__(self, low, high):
        super().__init__()
        self.count = 0
        self.type = 'cabbageAdvanced'
        self.low = low
        self.high = high
        self.target = None

    def set_target(self, target):
        self.target = target

    def return_random(self):
        return randint(self.low, self.high)
    
        
class GenerateEntityUniformDistribution(Entity):

    def __init__(self,low,high):
        super().__init__() # call the super-class constructor
        self.low = low
        self.high = high
        self.type = 'CustEntry'
        self.target = None

    def set_target(self, target):
        self.target = target
        
    def returnrand(self):
        return randint(self.low,self.high)
  

class EntityCounter(Entity):

    def __init__(self):
        super().__init__()
        self.total_count = 0
        self.type = 'Counter'
        
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


class Simulation(Entity):
    
    def __init__(self, firstCustomer, firstCabbages):

        self.firstCustomer = firstCustomer
        self.firstCabbages = firstCabbages
        self.clock = 0
        self.stock = firstCabbages.num
        self.future_event_list = []
        self.future_event_list.append((self.firstCustomer,self.clock + self.firstCustomer.returnrand()))
        
    def advanceTimeCabbage(self, next_event):
        self.future_event_list.append((next_event[0].target,self.clock))
      
    def process_entry_event(self,next_event):
        self.future_event_list.append((next_event[0].target,self.clock))
        
    def get_cabbages_displacement(self, next_event):
        if self.stock == 0:
            next_event.secondchoice.total_count += 1
            self.future_event_list.append((next_event[0].secondchoice, self.clock))
        else:
            next_event[0].firstchoice.total_count += 1
            self.future_event_list.append((next_event[0].firstchoice, self.clock))
            self.stock -= 1
        entity = AdvanceTimeUniformDistribution(next_event[0].to.low, next_event[0].to.high)
        customerEntity = GenerateEntityUniformDistribution(next_event[0].target.low, next_event[0].target.high)
        self.future_event_list.append((entity,self.clock + entity.returnrandom()))
        self.future_event_list.append((customerEntity, self.clock + customerEntity.returnrand()))
                   
    def process_counter_event(self,next_event,):
        next_event[0].total_count += 1
        self.future_event_list.append((next_event[0].target,self.clock))
        
    def process_EntryCabbages(self, next_event):
        self.stock = next_event[0].num
        self.future_event_list.append((next_event[0].target,self.clock))
        
    def process_termination_event(self,next_event):
        next_event[0].customersLeft += 1
        self.future_event_list.append(next_event[0].target, self.clock)
        
    def run(self, stop_after):
        while(len(self.future_event_list)!=0 and stop_after[0].count()<=stop_after[1]):
            print(self.future_event_list, self.clock)
            self.future_event_list.sort(key=lambda x: x[1])
            next_event = self.future_event_list[0]
            del self.future_event_list[0]
            #print(f'processing event {next_event[0].type} at time {self.clock}')
            self.clock = next_event[1]
            if(next_event[0].type == 'CustEntry'):
                print('entered')
                self.process_entry_event(next_event)
            elif(next_event[0].type == 'Counter'):
                self.process_counter_event(next_event)
            elif(next_event[0].type == 'Counter'):
                self.process_termination_event(next_event)
            elif(next_event[0].type == 'cabbageGeneration'):
                self.process_EntryCabbages(next_event)                
            elif(next_event[0].type == 'cabbageAdvanced'):
                self.advanceTimeCabbage(next_event)
            elif(next_event[0].type == 'Displacement'):
                self.get_cabbages_displacement(next_event)


