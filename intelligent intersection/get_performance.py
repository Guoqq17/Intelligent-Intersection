import sys
import traci
import traci.constants as tc
import numpy as np
import xml.etree.ElementTree as ET

def get_instant_fuel_external_model(lane_id):
    fuel = 0
    for i in range(len(lane_id)):
        cars_lane = traci.lane.getLastStepVehicleIDs(lane_id[i])
        for j in range(len(cars_lane) - 1, -1, -1):
            speed = traci.vehicle.getSpeed(cars_lane[j])
            acc = traci.vehicle.getAcceleration(cars_lane[j])
            fuel += 0.2736 + 0.0599*speed + 0.3547*acc - 0.0058*speed**2 + 0.0179*speed*acc + 0.0663*acc**2 + 0.0002*speed**3 + 0.002*speed**2*acc + 0.0245*speed*acc**2 - 0.0489*acc**3
    return fuel

def get_instant_fuel_sumo(lane_id):
    fuel = 0
    for i in range(len(lane_id)):
        cars_lane = traci.lane.getLastStepVehicleIDs(lane_id[i])
        for j in range(len(cars_lane) - 1, -1, -1):
            fuel +=  traci.vehicle.getFuelConsumption(cars_lane[j])
    return fuel

def get_average_waiting_time(file):
    tree = ET.parse(file)
    root = tree.getroot()
    cnt = 0
    wt = 0
    tl = 0
    for stu in root:
        wt += float(stu.attrib["waitingTime"])
        tl += float(stu.attrib["timeLoss"])
        cnt += 1
    print(cnt)
    return wt/cnt, tl/cnt

def get_average_queue_length(file):
    tree = ET.parse(file)
    root = tree.getroot()
    cnt = 0
    queue = 0
    for time in root:
        for lanes in time:
            for lane in lanes:
                queue += float(lane.attrib["queueing_length"])
                cnt += 1
    return queue/cnt

print(get_average_waiting_time("my_output_file.xml"))
print(get_average_queue_length("cfg/queues.xml"))
