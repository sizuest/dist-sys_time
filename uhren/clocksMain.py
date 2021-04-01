from clockutils import Process, VectorClock, LogicClock
import random


# print clock states
def clock_states_to_str(processes_to_print, vec_e_width=3):

    print_str = ""
    for p in processes_to_print:
        print_str += str(p.get_clock().to_string(vec_e_width)) + "\t"

    return print_str


# print the results of potential candidates for the happened before relation
def events_to_str(processes_to_print, event_source):

    # print clock states
    print_str = ""
    for p in processes_to_print:
        if p is event_source:
            print_str += " E "
        elif p.get_clock().is_less(event_source.get_clock()):
            if processes_to_print.index(p) > processes_to_print.index(event_source):
                if p.get_clock().can_do_happened_before_relation():
                    print_str += "<--"
                else:
                    print_str += "<?-"
            else:
                if p.get_clock().can_do_happened_before_relation():
                    print_str += "-->"
                else:
                    print_str += "-?>"
        elif (not p.get_clock().is_less(event_source.get_clock())) and \
                (not event_source.get_clock().is_less(p.get_clock())):
            print_str += "|| "
        elif event_source.get_clock().is_less(p.get_clock()):
            if processes_to_print.index(p) > processes_to_print.index(event_source):
                print_str += "</-"
            else:
                print_str += "-/>"
        else:
            print_str += "?"

        print_str += "\t"

    return print_str


# generate the output
def print_output(processes, event_source, comment="", title=False):
    # print title if required
    if title:
        vec_e_width = 3

        print_str = ""
        for p in processes:
            print_str += str(p.get_name()) + "\t"

        vec_width = len(processes[0].get_clock().to_string(vec_e_width))
        for p in processes:
            print_str += str(p.get_name()) + " "*(vec_width-len(p.get_name())) + "\t"
        print_str += "comment"
        print(print_str)
        print("-" * len(print_str) + "-" * 25)

    print(events_to_str(processes, event_source)+clock_states_to_str(processes)+comment)


def run_simulation(clock_type, p_count, e_count, m_prob):

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("SIMULATION OF", str(p_count), "processes with", clock_type, "clocks over", str(e_count), "events")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    processes = []
    for i in range(0, p_count):
        if clock_type == "LOGIC":
            processes.append(Process('p' + str(i), LogicClock(i)))
        elif clock_type == "VECTOR":
            processes.append(Process('p' + str(i), VectorClock(p_count, i)))

    # Reset the random generator to obtain the same values each time
    random.seed(30)

    # bins for statistics
    concurrent_events = 0

    # no message in pipe before the first event
    p_idx_destination = -1
    m = None

    for i in range(0, e_count):

        # last event did not include sending a message
        if p_idx_destination < 0:
            # draw random process
            p_idx = random.randint(0, p_count - 1)
            e = processes[p_idx].get_name() + ": event " + str(i)

            p_out = processes[p_idx].handle_event(e)

            if random.random() <= m_prob:
                # draw random destination
                p_idx_destination = random.randint(0, p_count - 1)
                while p_idx == p_idx_destination:
                    p_idx_destination = random.randint(0, p_count - 1)

                m = processes[p_idx].new_message("event " + str(i) + ", message from " + processes[p_idx].get_name())

        # last event did  include sending a message
        else:
            p_idx = p_idx_destination
            p_idx_destination = -1

            p_out = processes[p_idx].handle_message(m)

        # evaluate
        if processes[0].get_clock().can_do_happened_before_relation():
            concurrent = True
            for p in processes:
                if p is not processes[p_idx]:
                    if not ((not p.get_clock().is_less(processes[p_idx].get_clock()))
                            and (not processes[p_idx].get_clock().is_less(p.get_clock()))):
                        concurrent = False
                        break

            if concurrent:
                concurrent_events += 1

        # print
        print_output(processes, processes[p_idx], p_out, i == 0)

    print("\nLegend:\n  E\tevent\n  <?-\tHBR candidate\n  </-\tHBR not feasible\n  <--\tHBR\n  ||\tconcurrent")
    print("\nCONCURRENT EVENTS (DETECTED): "+str(round(concurrent_events/e_count*100)) + "%\n\n")


if __name__ == '__main__':
    # CONFIGURATION
    number_of_processes = 3    # Number of processes
    number_of_events = 20      # Number of events
    message_probability = .33  # Probability of a message (m=.33 --> 33% of the events will cause a message)

    # Run Simulations
    run_simulation("LOGIC", number_of_processes, number_of_events, message_probability)
    run_simulation("VECTOR", number_of_processes, number_of_events, message_probability)
