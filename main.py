from step_driver import StepDriver

if __name__ == '__main__':
    driver = StepDriver()
    print('Please input COM-port number need to use:')
    port_number = input('> ')
    driver.set_port(port_name='COM' + port_number)
    driver.find_address()
    driver.ping()
    driver.get_status()
    driver.get_info()
