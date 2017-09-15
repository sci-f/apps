#!/usr/env python

# Generate a crapton of robots, every color for each of the bases!
import pandas
import os
import json
from glob import glob
from colorthief import ColorThief
# https://github.com/fengsp/color-thief-py

colors = pandas.read_csv('colors.csv',header=None)
colors.columns = ['identifier','color_name','code','R','G','B']
bases = glob('bases/*.png')
basepath = "assets/img/robots"

print('Found %s robot bases!' %len(bases))

# Generate a json file for the robots
robots = []

# We will keep a record of primary colors
lookup = dict()

def get_primary_color(image):
    color_thief = ColorThief(image)
    return color_thief.get_color(quality=1)


count=1
for index,color in colors.iterrows():
    for base in bases:
        robot = {'name': color.color_name,
                 'color': color.code,
                 'uri': color.identifier }

        if base not in lookup:
            lookup[base] = get_primary_color(base)
        primary_color = lookup[base]

        # Compute scale factors to get differences
        scaleR = color.R / primary_color[0]
        scaleG = color.G / primary_color[1]
        scaleB = color.B / primary_color[2]

        robot['base'] = "%s/%s" %(basepath,base)
        robot_file = "robot%s.png" %count
        robot['url'] = "%s/%s" %(basepath,robot_file)
        os.system('/bin/bash makeColorVariants.sh %s %s %s %s %s' %(base, robot_file, scaleR, scaleG, scaleB))
        robots.append(robot)
        count+=1
        

# Finally, make a robot manifest
robot_manifest = 'robot-manifest.json'
with open(robot_manifest, 'w') as filey:
    filey.writelines(json.dumps(robots, indent=4, separators=(',',': ')))

# And robot data
robot_data = 'robots.csv'
with open(robot_data, 'w') as filey:
    # header
    filey.writelines("name,color,colorName,base,url\n")
    for robot in robots:
        filey.writelines('"%s",%s,%s,%s,%s\n' %(robot['name'],
                                                robot['color'],
                                                robot['uri'],
                                                robot['base'],
                                                robot['url']))
        seen.append(robot['url'])
