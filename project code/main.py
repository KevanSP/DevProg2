import multiprocessing
import Sensors as sens
import AIDetect as AID

def SensorsProc():
    sens.main()

def AIDProcess():
    AID.main()

def main():
    process_sensors = multiprocessing.Process(target=SensorsProc)
    process_sensors.start()
    process_AIDetect = multiprocessing.Process(target=AIDProcess)
    process_AIDetect.start()


if __name__ == "__main__":
    main()
