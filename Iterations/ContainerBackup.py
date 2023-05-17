import numpy as np

class Battery:
    def __init__(self, max_capacity, current_capacity):
        self.max_capacity = max_capacity
        self.current_capacity = current_capacity


class Container:
    def __init__(self, batteries):
        self.batteries = batteries
class ContainerArray:
    def __init__(self, num_containers_per_section, num_batteries_per_container):
        self.num_containers_per_section = num_containers_per_section
        self.num_batteries_per_container = num_batteries_per_container
        self.num_sections = len(num_containers_per_section)
        self.my_array = np.empty((self.num_sections,), dtype=object)
        for i in range(self.num_sections):
            num_containers = num_containers_per_section[i]
            containers = []
            for j in range(num_containers):
                batteries = []
                num_batteries = num_batteries_per_container[i][j]
                for k in range(num_batteries):
                    capacity = (i+1) * (j+1) * (k+1) * 100 # example formula to generate battery capacity
                    batteries.append(Battery(capacity, 0))
                containers.append(Container(batteries))
            self.my_array[i] = containers


# Define the number of sections, containers per section, and number of batteries per container
with open('config.txt', 'r') as f:
    config = f.read()

num_sections = 3
# 2 for section 1 3 for section 2 ect 
num_containers_per_section = [2, 3, 1]
#contaier [x,x] Now this means section x container 1 container 2 and the x is how many batteries
num_batteries_per_container = [[4, 4], [3, 3, 3], [5]]
a = ContainerArray(num_containers_per_section, num_batteries_per_container)

for i in range(num_sections):
    print("Section", i+1)
    for j in range(len(a.my_array[i])):
        print("\tContainer", j+1)
        container = a.my_array[i][j]
        for k, battery in enumerate(container.batteries):
            print("\t\tBattery", k+1)
            print("\t\tMaximum Capacity:", battery.max_capacity)
            print("\t\tCurrent Capacity:", battery.current_capacity)




with open('config.txt', 'r') as f:
    config = f.read()

sections = config.split('Section')[1:]

num_sections = len(sections)
num_containers_per_section = []
num_batteries_per_container = []
container_batteries = []

for i, section in enumerate(sections):
    containers = section.split('Container')[1:]
    num_containers_per_section.append(len(containers))

    batteries_per_container = []
    container_batteries_per_section = []

    for j, container in enumerate(containers):
        batteries = container.split('Battery')[1:]
        batteries_per_container.append(len(batteries))

        container_batteries_per_container = []
        for k, battery in enumerate(batteries):
            capacity_info = battery.strip().split('Capacity: ')
            if len(capacity_info) > 1:
                capacity_info = capacity_info[1].split(', max Capacity = ')
                if len(capacity_info) > 1:
                    current_capacity = int(capacity_info[0])
                    max_capacity = int(capacity_info[1])
                    container_batteries_per_container.append(Battery(max_capacity, current_capacity))

        container_batteries_per_section.append(container_batteries_per_container)

    num_batteries_per_container.append(batteries_per_container)
    container_batteries.append(container_batteries_per_section)

print(f'The configuration file contains {num_sections} sections.')
print(f'num_containers_per_section: {num_containers_per_section}')
print(f'num_batteries_per_container: {num_batteries_per_container}')

# Accessing the batteries in each container
for i, section_batteries in enumerate(container_batteries):
    section_number = i + 1
    for j, container_batteries in enumerate(section_batteries):
        container_number = j + 1
        for k, battery in enumerate(container_batteries):
            battery_number = k + 1
            print(f'Section {section_number}, Container {container_number}, Battery {battery_number}:')
            print(f'\tMax Capacity: {battery.max_capacity}')
            print(f'\tCurrent Capacity: {battery.current_capacity}')


