from abc import ABC, abstractmethod
import logging
import functools

logging.basicConfig(level=logging.INFO)

def log_action(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        logging.info(f"{self.name} is starting {func.__name__}")
        result = func(self, *args, **kwargs)
        logging.info(f"{self.name} finished {func.__name__}")
        return result
    return wrapper

class InsufficientBatteryError(Exception):
    def __init__(self, robot_name, required, available):
        self.robot_name = robot_name
        self.required = required
        self.available = available
        message = f"{robot_name} needs {required}% battery for this task but only has {available}%."
        super().__init__(message)
class Robot(ABC):
    manufacturer = "Blitz"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        self._battery = max(0, min(100, value))

    def use_battery(self, amount):
        if amount > self.battery:
            raise InsufficientBatteryError(self.name, amount, self.battery)
        self.battery -= amount

    @classmethod
    def from_config(cls, config):
        return cls(**config)
        
    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, battery={self.battery})"

    @abstractmethod
    def perform_task(self):
        pass

class DeliveryRobot(Robot):
    def __init__(self, name, battery=100, max_package_weight=10):
        super().__init__(name, battery)
        self.max_package_weight = max_package_weight  # in kg

    @log_action
    def perform_task(self):
        cost = 15
        self.use_battery(cost)
        return f"{self.name} delivers a package (up to {self.max_package_weight}kg). Battery used: {cost}%"

class SecurityRobot(Robot):
    def __init__(self, name, battery=100, patrol_radius=50):
        super().__init__(name, battery)
        self.patrol_radius = patrol_radius  # in meters

    def perform_task(self):
        cost = 8
        self.use_battery(cost)
        return f"{self.name} patrols a {self.patrol_radius}m radius. Battery used: {cost}%"


class CookingRobot(Robot):
    def __init__(self, name, battery=100, recipe_count=20):
        super().__init__(name, battery)
        self.recipe_count = recipe_count  # number of recipes it knows
    def perform_task(self):
        cost = 20
        self.use_battery(cost)
        return f"{self.name} cooks a meal from its {self.recipe_count}-recipe repertoire. Battery used: {cost}%"

def fleet_report(robots):
    for robot in robots:
        print(str(robot))

def run_task_safely(robot, **kwargs):
    try:
        result = robot.perform_task(**kwargs)
    except InsufficientBatteryError as e:
        logging.error(e)
    else:
        print(result)
    finally:
        print(f"{robot.name}'s battery is now at {robot.battery}%")
