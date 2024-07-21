import common
from collections import deque, defaultdict
from multiprocessing import Process, Queue
from time import sleep
year_common = common.import_year_common(2019)

tape = common.extract_numbers(common.read_file())

def run_computer(address, mem, q_in: Queue, q_out: Queue, q_state: Queue):
    operations = deque(maxlen=50)

    def manage_state(new_op):
        operations.append(new_op)
        new_state = q_in.empty() and q_out.empty()
        if new_state:
            for op in operations:
                if op != -1:
                    new_state = False
                    break
        q_state.put((address, new_state))
        if new_state:
            sleep(0.1)
        return new_state

    def gen_input():
        yield address
        while True:
            if not q_in.empty():
                pair = q_in.get()
                yield pair[0]
                yield pair[1]
                manage_state('in')
            else:
                yield -1
                manage_state(-1)

    it = year_common.run_intcode(mem, gen_input())
    try:
        while True:
            addr = next(it)
            x = next(it)
            y = next(it)
            q_out.put((addr, x, y))
            manage_state('out')
    except StopIteration:
        pass

computers_count = 50

def run_nat(mem, q_in: Queue, q_out: Queue, q_state: Queue):
    states = [False]*computers_count
    last_x = None
    last_y = None
    last_sent = None
    part_2_solved = False

    last_x, last_y = q_in.get()
    while True:
        # last_x, last_y = q_in.get()
        while not q_in.empty():
            last_x, last_y = q_in.get()
        # addr, state = q_state.get()
        # states[addr] = state
        while not q_state.empty():
            addr, state = q_state.get()
            states[addr] = state
        if all(states) and q_in.empty():
            # while not q_in.empty():
            #     last_x, last_y = q_in.get()
            q_out.put((0, last_x, last_y))
            if not part_2_solved and (last_x, last_y) == last_sent:
                print(last_y)
                part_2_solved = True
            last_sent = last_x, last_y

            # read until 0 reports not idle
            while True:
                addr, state = q_state.get()
                states[addr] = state
                if addr == 0 and state == False:
                    break

queues = defaultdict(lambda: Queue())
processes = []
q_out = Queue()
q_state = Queue()

for i in range(computers_count):
    q = queues[i]
    mem = year_common.tape_to_mem(tape)
    p = Process(name='PC'+str(i), target=run_computer, args=(i, mem, q, q_out, q_state))
    p.start()
    processes.append(p)

mem = year_common.tape_to_mem(tape)
p_nat = Process(name='NAT', target=run_nat, args=(mem, queues[255], q_out, q_state))
p_nat.start()
processes.append(p_nat)

part_1_solved = False
while True:
    address, x, y = q_out.get()
    if not part_1_solved and address == 255:
        print(y)
        part_1_solved = True
    queues[address].put((x, y))

for p in processes:
    p.terminate()
exit(0)
