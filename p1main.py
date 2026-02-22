#V1 code
#.process_time() function returns the value of the sum of the system and user CPU time of the current process
#.process_time_ns() to avoid the precision loss caused by float type

#Libraries
import time

#PCB Class
#Version 1
class PCB1:
    def __init__(self, pid):
        self.pid = pid
        self.parent = -1
        self.children = []
        self.isActive = False
        
class ProcessHierarchyV1:
    def __init__(self, size = 16):
        self.pcbs = [PCB1(i) for i in range(size)]
        self.pcbs[0].isActive = True

    def create(self, parentPid):
        if not self.pcbs[parentPid].isActive:
            print(f"Error: Parent process {parentPid} does not exist")
            return -1
        
        #Finding the first available PCB 
        for q in range(len(self.pcbs)):
            if not self.pcbs[q].isActive:
                self.pcbs[q].isActive = True
                self.pcbs[q].parent = parentPid
                self.pcbs[q].children = []
                self.pcbs[parentPid].children.append(q)
                return q
        print("Maximum process limit reached!")    
        return -1

    def destroy(self, targetPid):
        #Recursively destroys a process and all its descendents
        if not self.pcbs[targetPid].isActive:
            return
            
        #recursively destroy all children in the list first
        for childPid in list(self.pcbs[targetPid].children):
            self.destroy(childPid)

        #remove this process from its parent's child list
        parentPid = self.pcbs[targetPid].parent
        if parentPid != -1:
            self.pcbs[parentPid].children.remove(targetPid)

        #Mark the PCB as free
        self.pcbs[targetPid].isActive = False

    def showProcessInfo(self):
        #Prints the hierarchy
        for p in self.pcbs:
            if p.isActive:
              child_string = ", ".join(map(str, p.children)) if p.children else "none"
              print(f"Process {p.pid}: parent is {p.parent} and children are {child_string}")

#PCB Class
#Version 2
class PCB2:
    pass
################Classes End#################
def main():
    command_list = []

    print("Process Management Simulation (version 1)")
    print("Enter commands: 'create N', 'destroy N', or 'end'")
    print("Where N = 0-15")

    while True:
        user_input = input("> ").lower().split()

        #check for end input
        if not user_input or user_input[0] == "end":
            break

        if len(user_input) < 2:
            print("Invalid input!")
            print("Use 'create N' or 'destroy N'")
            continue

        command = user_input[0]
        try:
            pid_argument = int(user_input[1])

            if command in ["create", "destroy"]:
                command_list.append((command, pid_argument))
            else:
                print("Invalid Input! Use 'create' or 'destroy'")

        except ValueError:
            print("Please enter a valid integer for the PID")

    if command_list:
        #create v1 object
        v1_hierarchy = ProcessHierarchyV1()

        print("\n---------Running Squence Once with process info---------")
        for action, pid in command_list:
            print(f"\nExecuting: {action} {pid}")

            if action == "create":
                v1_hierarchy.create(pid)
            elif action == "destroy":
                v1_hierarchy.destroy(pid)

            #showProcessInfo()
            v1_hierarchy.showProcessInfo()

        #timing
        print("\n----Measuring Performance (200 Iterations)----")

        start_clock = time.process_time_ns()

        for _ in range(200):
            #reset hierarchy for each iterarion
            test_bench = ProcessHierarchyV1()
            for action, pid in command_list:
                if action == "create":
                    test_bench.create(pid)
                elif action == "destroy":
                    test_bench.destroy(pid)
        
        end_clock = time.process_time_ns()

        print(f"Total CPU time for 200 runs: {end_clock - start_clock} nanoseconds")

    else:
        print("No commands were entered")

if __name__ == "__main__":
    main()
#-------------------------------------------------#
#V2 Code
