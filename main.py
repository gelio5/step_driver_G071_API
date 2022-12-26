from step_driver import StepDriver
from time import sleep

if __name__ == '__main__':
    driver = StepDriver(modbus_address=2, port='COM3')
    import logging

    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    # driver.stop()
    driver.search_home()
    # print(driver.get_full_info())
    # driver.move_to_pos(position=20000, speed=4000)
    print(driver.get_status())
    # print(driver.get_full_info())
    # for _ in range(5):
    #     sleep(2)
    #     print(driver.get_full_info())
