# -*- coding:utf8 -*-
import time

from state_machine import before, after, State, Event, acts_as_state_machine,\
    InvalidStateTransition
import pymysql



@acts_as_state_machine
class Process:
    started = State(initial=True)
    running = State()
    waiting = State()
    endding = State()

    run = Event(from_states=started, to_state=running)
    wait = Event(from_states=(started, running), to_state=waiting)
    end = Event(from_states=(waiting, running), to_state=endding)

    def __init__(self, name):
        self.name = name
        self.con = pymysql.connect(host="127.0.0.1", port=3306, user="hekaijia", passwd="123456", db="my_test")
        self.cur = self.con.cursor()
        print("connect to database")

    @after("run")
    def run_info(self):
        self.cur.execute("select current_date()")
        data = self.cur.fetchall()
        print("Today is : {}".format(data[0]))
        print("{} is running".format(self.name))

    @before("wait")
    def wait_info(self):
        time.sleep(3)
        print("{} is waiting".format(self.name))

    @after("end")
    def end_info(self):
        print("{} is finished".format(self.name))


def transition(process, event, event_name):
    try:
        event()
    except InvalidStateTransition as err:
        print("Error: transition of {} from {} to {} failed".format(process.name, process.current_state, event_name))

def main():
    p = Process("test1")
    transition(p, p.run, "running")
    transition(p, p.wait, "waiting")
    transition(p, p.end, "ending")
    transition(p, p.run, "running")
    # p.run()
    # p.wait()
    # p.end()


if __name__ == '__main__':
    main()