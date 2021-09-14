import logging
import time

from pomp_driver import Pump, PumpDriver
import datetime
from classes.TimeKeeper import TimeKeeper
import sys, os
import signal


class Plant:

    def __init__(self, name: str, pump_number: int, watering_length: float, watering_time: list, logging):
        """
        Create a new plant
        :param name: Name of plant
        :param pump_number: number of rpi pin which connect to controlled pump
        :param watering_length: length time on pump
        :param watering_time: list of time which a plant will by irrigating
        :param logging: logger object
        """
        self.logger = logging
        self.name = name
        self.pump_nr = pump_number
        self.water_time = watering_time
        self.watering_length = watering_length  # in seconds
        self.time_keeper = TimeKeeper(TimeKeeper.get_current_time(), pump_nr=pump_number)
        self.logger.info(f'\nCreate plant: {self.name}\n'
                         f'pump_pin_nr: {self.pump_nr}\n'
                         f'watering length {self.watering_length}\n'
                         f'watering timing: {self.water_time}')

    def get_name(self):
        return self.name

    def get_pump_nr(self):
        return self.pump_nr

    def get_watering_time(self):
        return self.water_time

    def get_watering_length(self):
        return self.watering_length

    def set_watering_length(self, watering_length):
        self.watering_length = watering_length

    def add_watering_time(self, new_watering_time):
        self.water_time.append(new_watering_time)

    def set_watering_time(self, watering_time: list):
        self.water_time = watering_time

    def del_watering_time(self, time_to_del):
        if time_to_del in self.water_time:
            self.water_time.remove(time_to_del)
            return True, "Done"
        else:
            return False, "Time is not exist"

    def get_time_keeper(self):
        return self.time_keeper


class PlantWater(PumpDriver):
    # czas podlewania
    LARGE_PEPPER_P1 = 5.5
    PEPPERS_AND_ROSE_P2 = 3
    FLYCATCHER_P3 = 5
    JALAPENO_PEPPERS_P4 = 3
    HERBS_P5 = 6.5
    NONE_P6 = 5

    # czasy w ktorych sa podlewane kwiaty
    # WATERING_LARGE_PEPPER = ['08:10:00', '11:55:30', '12:35:30', '15:28:40', '18:28:40', '21:15:00']
    WATERING_LARGE_PEPPER = ['11:55:30', '12:35:30', '18:28:40', '21:15:00']
    WATERING_PEPPERS_AND_ROSE = ['11:30:20', '21:16:00']
    WATERING_FLYCATCHER = ['09:00:20', '17:44:11', '21:17:00']
    # WATERING_FLYCATCHER = ['21:17:00']
    WATERING_JALAPENO_PEPPERS = ['10:25:50', '14:24:30']
    WATERING_HERBS = ['12:49:50', '18:49:50']

    def __init__(self):
        super(PlantWater, self).__init__()
        self.start_time = TimeKeeper.get_current_time()
        signal.signal(signal.SIGTERM, self.terminate_process)
        self.large_pepper = Plant(name="Papryka w pomaranczowej donicy",
                                  pump_number=Pump.PUMP1,
                                  watering_length=self.LARGE_PEPPER_P1,
                                  watering_time=self.WATERING_LARGE_PEPPER,
                                  logging=self.logger)
        self.peppers_and_roze = Plant(name="Papryka w donicy z roza",
                                      pump_number=Pump.PUMP2,
                                      watering_length=self.PEPPERS_AND_ROSE_P2,
                                      watering_time=self.WATERING_PEPPERS_AND_ROSE,
                                      logging=self.logger)
        self.flycatcher = Plant(name="Mucholowka",
                                pump_number=Pump.PUMP3,
                                watering_length=self.FLYCATCHER_P3,
                                watering_time=self.WATERING_FLYCATCHER,
                                logging=self.logger)
        self.jalapeno_peppers = Plant(name="Papryka jalapeno",
                                      pump_number=Pump.PUMP4,
                                      watering_length=self.JALAPENO_PEPPERS_P4,
                                      watering_time=self.WATERING_JALAPENO_PEPPERS,
                                      logging=self.logger)
        self.herbs = Plant(name="Zioła: Lubczyk, Pietruszka, Rozmaryn",
                           pump_number=Pump.PUMP5,
                           watering_length=self.HERBS_P5,
                           watering_time=self.WATERING_HERBS,
                           logging=self.logger)

    def __enter__(self):
        self.logger.info("enter method called")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()

    def terminate_process(self, signal_number, frame):
        """
        This function is used to close ports after the script receives a SIGTERM signal from .service
        @param signal_number:
        @param frame:
        @return:
        """
        self.clear()
        self.logger.info(f'(SIGTERM): {signal_number}, terminating the process')
        sys.exit()

    def water_plant(self, pump, time_delay):
        self.on_pump(pump)
        self.logger.info("Plant is being watered!")
        time.sleep(time_delay)
        self.logger.info("Watering is finished!")
        self.off_pump(pump)

    def sleep_time(self, times):
        self.logger.debug(f"wait 1s czas = {TimeKeeper.get_current_time()}")
        self.off_all()
        time.sleep(times)

    def start_water_new(self, my_plant: Plant):
        self.water_plant(my_plant.get_pump_nr(), my_plant.watering_length)
        my_plant.get_time_keeper().set_time_last_watered(TimeKeeper.get_current_time())
        self.logger.info(f"\nPlant {my_plant.get_name()} was last watered at "
                         f"{my_plant.get_time_keeper().time_last_watered}")

    def check_time_to_water(self, watering_plant: Plant, current_time):
        for watering in watering_plant.get_watering_time():
            if watering == current_time:
                self.start_water_new(watering_plant)

    def run(self):

        current_time = TimeKeeper.get_current_time()
        # self.logger.info(f"Time: {current_time}")
        self.check_time_to_water(watering_plant=self.large_pepper, current_time=current_time)
        self.check_time_to_water(watering_plant=self.peppers_and_roze, current_time=current_time)
        self.check_time_to_water(watering_plant=self.flycatcher, current_time=current_time)
        self.check_time_to_water(watering_plant=self.jalapeno_peppers, current_time=current_time)
        self.check_time_to_water(watering_plant=self.herbs, current_time=current_time)


if __name__ == '__main__':
    print(f"Start time: {datetime.datetime.now()}")
    with PlantWater() as plant:
        try:
            while True:
                plant.sleep_time(1)
                plant.run()
        except KeyboardInterrupt:
            plant.logger.info(f"End time: {datetime.datetime.now()}")
            print("ending...")
