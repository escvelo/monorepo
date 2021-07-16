# MotionPlanning

## Part 5: The first motion planning algorithm

Assuming the vacuum robot runs out of battery it has to navigate to its charging station.
1) Program a sPRM that will guide the robot to its goal.
1) Use uniform sampling of the configuration space.
2) For finding nearest neighbours use brute force.
3) For the metric use the Euclidean metric.
4) For finding the shortest path use a Djkstra (Use a lib, do not program it on your own)
2) Make sure you can edit the parameters of the algorithm in the UI.
3) Make sure you can run multiple tries of the algorithm.
Note: Use a challenging start and goal point.
4) Test your algorithm and give an approximate number of samples that are needed to solve the problem in 
90% of the tests.
Note: For this you have to run the algorithm multiple times (at least 10 times) with the same parameters and measure the success.
Optional:
Go online and find some Rooms and robots on your own and test your software with them.
![alt text](https://raw.githubusercontent.com/escvelo/monorepo/master/motionplanning/images/Room.bmp)


## Part 7: Implement a paper
Implement one of the following papers or search for a paper that you 
want to implement. For the second, please check with me first before 
you start to implement (Some papers are complex).
The order of the following papers are with increasing complexity. 
(simple -> medium)

### Paper 1: Bridge Test
Implement the paper for bridge Test sampling with your sPRM:
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.20.377&re
p=rep1&type=pdf

### Paper 2: Implement the Gaussian Sampling
Implement the paper for Gaussian sampling with your sPRM:
• http://www.cs.uu.nl/research/techreps/repo/CS-2001/2001-36.pdf


### Paper 3: Implement the RRTConnect
Implement the paper for the RRT Connect
https://www.researchgate.net/publication/221075120_RRTConnect_An_Efficient_Approach_to_SingleQuery_Path_Planning/link/00463538adeee00146000000/download


---------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Output


## Code snippets 

### Checking if path between two configuration is not in collision. 
![alt text](https://github.com/escvelo/monorepo/blob/master/motionplanning/output/isValidEdge.JPG)

### Finding shortest path between "start" and "end" configuration.
![alt text](https://github.com/escvelo/monorepo/blob/master/motionplanning/output/shortestPath.JPG)

### Check if robot can be placed at given configuration.
![alt text](https://github.com/escvelo/monorepo/blob/master/motionplanning/output/uniform_cfreeSpace.JPG)

### Implementation of Bridge Test paper
![alt text](https://github.com/escvelo/monorepo/blob/master/motionplanning/output/Bridge_test.JPG)

### Implement the Gaussian Sampling
![alt text](https://github.com/escvelo/monorepo/blob/master/motionplanning/output/Gaussian_sigma40.JPG)

## Configuration space overlaid on workspace

### number of samples n = 1000 and radius r = 100, with uniform sampling
![alt text](https://github.com/escvelo/monorepo/blob/master/motionplanning/output/cs_n_1000_r_100_BT_uniform.JPG)

### number of samples n = 100 and radius r = 100, with uniform sampling 
![alt text](https://github.com/escvelo/monorepo/blob/master/motionplanning/output/cs_n_100_r_100_sigma_40_uniform.JPG)

### number of samples n = 100 and radius r = 100, with bridgetest sampling 
![alt text](https://github.com/escvelo/monorepo/blob/master/motionplanning/output/cs_n_100_r_100_sigma_40_bridgetest.JPG)

### number of samples n = 100 and radius r = 100, with gaussian sampling 
![alt text](https://github.com/escvelo/monorepo/blob/master/motionplanning/output/cs_n_100_r_100_sigma_40_gaussian.JPG)























