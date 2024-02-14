import multiprocessing
import Sensors as sens

def SensorsProc():
    sens.main()

def NotifProcess():
    noif.Send_Notif()

def main():
    process_sensors = multiprocessing.Process(target=SensorsProc)
    process_sensors.start()

if __name__ == "__main__":
    main()