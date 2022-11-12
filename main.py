from step_driver import StepDriver

if __name__ == '__main__':
    driver = StepDriver()
    # print('Please input COM-port number need to use:')
    # port_number = input('> ')
    port_number = '3'
    driver.set_port(port_name='COM' + port_number)
    driver.find_address()
    # driver.ping()
    # driver.get_info()

    driver.get_status()
    print(driver.status)

    driver.run(1000, 100)
    # driver.stop()
    for i in range(100):
        driver.get_status()
        print(i, driver.status['encoder'], driver.status['step_generator'])
