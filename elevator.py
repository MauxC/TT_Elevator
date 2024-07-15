import threading
import time

class ElevatorHardware:
    def goUp(self):
        pass
    
    def goDown(self):
        pass

class Elevator(threading.Thread):

    currFloor = 0
    targetFloor = None
    goingUp = False
    goingDown = False
    occupied = False

    def __init__(self, id: int):
        super().__init__()
        self.id = id
        self.hardware = ElevatorHardware()
        self.running = True
        self.lock = threading.Lock()
        self.start()

    def run(self):
        while self.running:
            if self.targetFloor is not None:
                self.move()
            time.sleep(1)

    def stop(self):
        self.running = False

    def move(self) -> None:
        with self.lock:
            if self.currFloor < self.targetFloor:
                self.hardware.goUp()
                self.currFloor += 1
                self.goingUp = True
            elif self.currFloor > self.targetFloor:
                self.hardware.goDown()
                self.currFloor -= 1
                self.goingDown = True
            else:
                self.targetFloor = None
                self.goingDown = False
                self.goingUp = False
                self.occupied = False
                print(f"Elevator n°{self.id} on {self.currFloor} floor")

    def addFloorRequest(self, floor):
        with self.lock:            
            print(f"Elevator {self.id}, floor {floor} requested")
            self.targetFloor = floor
            self.occupied = True


class ElevatorManager:
    elevators = []

    def __init__(self, nbElevators):
        for i in range(nbElevators):
            self.elevators.append(Elevator(i))
            
    def getClosestElevator(self, requestedFloor):
        closestElevator = None
        minDist = None

        for elevator in self.elevators:
            dist = None

            if requestedFloor < elevator.currFloor and not elevator.occupied:
                dist = abs(elevator.currFloor - requestedFloor)
            elif requestedFloor > elevator.currFloor and not elevator.occupied:
                dist = abs(elevator.currFloor - requestedFloor)
            elif not elevator.occupied:
                dist = 0

            if dist is not None and (minDist is None or minDist > dist):
                minDist = dist
                closestElevator = elevator

        return closestElevator

    def requestElevator(self, floor: int) -> Elevator:
        closestElevator: Elevator = None

        print(f"Requesting elevator on the {floor} floor")
        
        while True:
            closestElevator = self.getClosestElevator(floor)

            if closestElevator is not None:
                self.sendElevatorToFloor(closestElevator, floor)
                return
            time.sleep(1)

    def sendElevatorToFloor(self, elevator, floor: int):
        elevator.addFloorRequest(floor)

    def stopElevators(self):
        for elevator in self.elevators:
            elevator.stop()

if __name__ == "__main__":
    print("Elevator simulation\n")
    manager = ElevatorManager(5)

    try:
        elevator = manager.requestElevator(5)
        time.sleep(0.5)
        elevator = manager.requestElevator(7)
        elevator = manager.requestElevator(17)
        elevator = manager.requestElevator(6)
        time.sleep(10)
        elevator = manager.requestElevator(9)
        time.sleep(3)
        elevator = manager.requestElevator(9)
        elevator = manager.requestElevator(0)
        time.sleep(5)
        elevator = manager.requestElevator(20)
        elevator = manager.requestElevator(5)
        time.sleep(5)
        elevator = manager.requestElevator(11)
        time.sleep(10)
        
        
        for e in manager.elevators:
            print(f"Elevator {e.id} on the {e.currFloor} floor")
        

    finally:
        manager.stopElevators()