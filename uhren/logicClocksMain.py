from locigclocks import Process, Message
from random import randint, random


def print_clock_states(processes, comment="", title=False):
    # print title if required
    if title:
        print_str = ""
        for p in processes:
            print_str += str(p.get_name()) + "\t"

        print_str += "| comment"
        print(print_str)
        print("-"*len(print_str)+"-"*len(processes)*5)

    # print clock states
    print_str = ""
    for p in processes:
        print_str += str(p.get_lc()) + "\t"

    print_str += "| "+comment

    print(print_str)


if __name__ == '__main__':
    # Number of processes to be created:
    p_count = 3
    # create the processes
    processes = []
    for i in range(0, p_count):
        processes.append(Process('p' + str(i), 0))

    # Events:
    # Total count:
    e_count = 100
    # Probability of a message
    m_prob = .2

    for i in range(0, e_count):

        # draw random process
        p_idx = randint(0, p_count - 1)

        # raise an event on the selected process
        e = processes[p_idx].get_name() + ": event " + str(i)
        processes[p_idx].handle_event(e)
        print_clock_states(processes, e, i==0)

        # insert messages in-between the processes
        if random() <= m_prob:
            p_idx2 = randint(0, p_count - 1)
            while p_idx == p_idx2:
                p_idx2 = randint(0, p_count - 1)

            m = Message(processes[p_idx].get_name()+": message to " + processes[p_idx2].get_name(), processes[p_idx].get_lc())
            processes[p_idx2].handle_message(m)

            # output of the clock states
            print_clock_states(processes, m.get_message())



