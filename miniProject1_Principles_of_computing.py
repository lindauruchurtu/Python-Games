"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random


# Used to increase the timeout, if necessary
import codeskulptor
#codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    def __init__(self):
        """
        Initialise relevant variables
        """
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0 # this is the rate
        
        # History tuple: time, item bought yes/no, cost of item, no cookies produced at time
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        string_rep = "\n" + "Time: " + str(self.get_time()) + " Current Cookies: " + str(self.get_cookies()) + " CPS: " + str(self.get_cps()) + " Total Cookies: " + str(self._total_cookies) + " History: " +str(self._history) 
        return string_rep
  
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        # How many cookies do we have to gain
        cookie_diff = cookies - self._current_cookies
        if cookie_diff <= 0.0:
            return 0.0
        elif cookie_diff > 0:
        # Compute the time we have to wait
            return math.ceil(cookie_diff / self._cps)
  
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            # update current cookies
            self._current_cookies = self._current_cookies + time * self._cps
            # update time
            self._time = self._time + time
            # update total number of cookies
            self._total_cookies = self._total_cookies + time * self._cps
            # update history
            #self._history.append((self._time, None , 0.0, self._total_cookies))  
        else:
            pass
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        
        if (self._current_cookies >= cost):
            # buy cookies
            self._current_cookies = self._current_cookies - cost
            self._cps = self._cps + additional_cps
            # update history
            self._history.append((self._time, item_name , cost, self._total_cookies))
            
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    # Clone build_info
    build = build_info.clone()

    # Create ClickerState object
    clicker = ClickerState()

    # Initialise simulation timer
    timer = 0

    while timer <= duration:
        
        # Call strategy function with right parameters
        item = strategy(clicker.get_cookies(), clicker.get_cps(), duration - timer, build)

        if item == None:
            # print "No items can be purchased"
            break
        else:
            # determine how much time do we need to wait to buy item
            item_cost = build.get_cost(item) # in units of cookies

            # wait so we can buy cookies
            wait_time = clicker.time_until(item_cost)
            
            # compute additional CPS associated to item
            added_cps = build.get_cps(item)
            
            if wait_time > duration - timer:
                break
            
            # wait until that time
            clicker.wait(wait_time)
            
            # buy the item
            clicker.buy_item(item, item_cost, added_cps)
            
            # update the build information
            build.update_item(item)
    
        # update simulation timer
        timer = timer + wait_time


    # Check if there is time left
    if timer < duration:
        clicker.wait(duration-timer) # aggregate more cookies
        timer = duration
    return clicker


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Returns item that is the cheapest one
    can buy with the amount of cookies one has / time left
    """
    # iterate over items and compare cookies with cost
    # we can afford cookies + cookies generated while waiting for time_left
    effective_cookies = cookies + time_left * cps
    list_items = build_info.build_items()
    
    # build dictionary
    list_costs = {}
    for item in list_items:
        if build_info.get_cost(item) <= effective_cookies:
            list_costs[item] = build_info.get_cost(item)
    
    # Check if there are still items one can buy
    if len(list_costs) == 0:
        return None
    
    # find minimum 
    min_value = min(list_costs.values())
    for item in list_costs.items():
        if item[1] == min_value:
            cheapest_item = item[0]
            return cheapest_item

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Returns item that is the most expensive
    can buy with the amount of cookies one has / time left
    """
    # iterate over items and compare cookies with cost
    # we can afford cookies + cookies generated while waiting for time_left
    effective_cookies = cookies + time_left * cps
    list_items = build_info.build_items()

    # build dictionary with items that are cheaper than eff_cookies
    list_costs = {}
    for item in list_items:
        if build_info.get_cost(item) <= effective_cookies:
            list_costs[item] = build_info.get_cost(item)
    
     # Check if there are still items one can buy
    if len(list_costs) == 0:
        return None
    
    # find maximum
    max_value = max(list_costs.values())
    for item in list_costs.items():
        if item[1] == max_value:
            expensive_item = item[0]
            #print "Bought: ", expensive_item
            return expensive_item

def strategy_best(cookies, cps, time_left, build_info):
    """
    Returns random item among those that can be
    bought with the amount of cookies one has / time left
    """
    # iterate over items and compare cookies with cost
    # we can afford cookies + cookies generated while waiting for time_left
    effective_cookies = cookies + time_left * cps
    list_items = build_info.build_items()
    
    # randomly pick an item
    # build dictionary with items that are cheaper than eff_cookies
    list_costs = {}
    for item in list_items:
        if build_info.get_cost(item) <= effective_cookies:
            list_costs[item] = build_info.get_cost(item)

    # Check if there are still items one can buy
    if len(list_costs) == 0:
        return None
    
    return random.choice(list_costs.items())[0]
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print "Strategy used: ", strategy_name, "\n", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #print history
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    #run_strategy("none", SIM_TIME, strategy_none)    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #run_strategy("Best", SIM_TIME, strategy_best)
    
run()

