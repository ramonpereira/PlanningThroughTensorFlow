Commands
===
The following commands are used in generating experiment results on our paper.

## Training

We train 3 domains in the paper: Reservoir, HVAC, Navigation.

Reservoir : 1 hidden layer, 32 neurons in layer, densely connected
HVAC: 1 hidden layer, 32 neurons in layer, densely connected
Navigation: 2 hidden layers, 32 neurons in each layer, densely connected

### LQR 1D Navigation

1-Layer:

```bash
python train.py -p data/LQR_1D_NAV/ -x lqr_nav_1d-data.txt -y lqr_nav_1d-label.txt -w weights/lqr_1d_nav-1_layer/ -s 4 -d LQG_1D_NAV -l 1
```

2-Layers:

```bash
python train.py -p data/LQR_1D_NAV/ -x lqr_nav_1d-data.txt -y lqr_nav_1d-label.txt -w weights/lqr_1d_nav-2_layers/ -s 4 -d LQG_1D_NAV -l 2
```

### LQG 1D Navigation

1-Layer:

```bash
python train.py -p data/LQG_1D_NAV/ -x lqg_1d_nav-data.txt -y lqg_1d_nav-label.txt -w weights/lqg_1d_nav-1_layer/ -s 4 -d LQG_1D_NAV -l 1
```

2-Layers:

```bash
python train.py -p data/LQG_1D_NAV/ -x lqg_1d_nav-data.txt -y lqg_1d_nav-label.txt -w weights/lqg_1d_nav-2_layers/ -s 4 -d LQG_1D_NAV -l 2
```

### Reservoir 3
```bash
python train.py -p data/Reservoir/Reservoir_3/ -x Reservoir_Data.txt -y Reservoir_Label.txt -w weights/reservoir/reservoir3 -s 3 -d Reservoir -l 1
```

### Reservoir 4
```bash
python train.py -p data/Reservoir/Reservoir_4/ -x Reservoir_Data.txt -y Reservoir_Label.txt -w weights/reservoir/reservoir4 -s 4 -d Reservoir -l 1
```

### HVAC 3
```bash
python train.py -p data/HVAC/ROOM_3/ -x HVAC_Data.txt -y HVAC_Label.txt -w weights/hvac/hvac3 -s 3 -d HVAC -l 1

```

### HVAC 6
```bash
python train.py -p data/HVAC/ROOM_6/ -x HVAC_Data.txt -y HVAC_Label.txt -w weights/hvac/hvac6 -s 6 -d HVAC -l 1
```

### Navigation 8x8
```bash
python train.py -p data/Navigation/8x8/ -x Navigation_Data.txt -y Navigation_Label.txt -w weights/nav/8x8 -s 2 -d Navigation -l 2
```

### Navigation 10x10
```bash
python train.py -p data/Navigation/10x10/ -x Navigation_Data.txt -y Navigation_Label.txt -w weights/nav/10x10 -s 2 -d Navigation -l 2
```

## Tensorflow Planning

Planning on trained domain should connected to the real domain simulator for evaluation purpose,
Since the learned transition function is not the one in real world. Directly using this planner 
could end up meeting different state in the real world.

Note: 
1. The initial state should be provided by the "real world" state from RDDL simulator.
2. The last action given by this planner is not counted in reward, so may be arbitrary. 
3. Change code for the action constraints, not given as parameters currently.

If you only want to check if the planner works in general. Please run following commands with pseudo initial state.

### LQR 1D Navigation

```bash
python plan.py -w weights/lqr_1d_nav-1_layer/ -d LQR_1D_Navigation -i LQR0 -s 3 -a 1 --get_state temp/test/lqr_1d_nav/init_problem_instance_0 --constraint -1 1 -hz 100 -l 1
```

```bash
python plan.py -w weights/lqr_1d_nav-2_layers/ -d LQR_1D_Navigation -i LQR0 -s 3 -a 1 --get_state temp/test/lqr_1d_nav/init_problem_instance_0 --constraint -1 1 -hz 100 -l 2
```

### LQG 1D Navigation

```bash
python plan.py -w weights/lqg_1d_nav-1_layer/ -d LQG_1D_Navigation -i LQG0 -s 3 -a 1 --get_state temp/test/lqg_1d_nav/init_problem_instance_0 --constraint -1 1 -hz 100 -l 1
```

```bash
python plan.py -w weights/lqg_1d_nav-2_layers/ -d LQG_1D_Navigation -i LQG2 -s 3 -a 1 --get_state temp/test/lqg_1d_nav/init_problem_instance_2 --constraint -1 1 -hz 100 -l 2
```

### Navigation 8x8

```bash
python plan.py -w weights/nav/8x8 -d Navigation -i Navigation8 -s 2 -a 2 --get_state temp/test/nav/8x8/state --constraint -1 1
```

### Navigation 10x10
```bash
python plan.py -w weights/nav/10x10 -d Navigation -i Navigation10 -s 2 -a 2 --get_state temp/test/nav/10x10/state --constraint -1 1
```


### HVAC 3
```bash
python plan.py -w weights/hvac/hvac3 -d HVAC -i HVAC3 -s 3 -a 3 --get_state temp/test/hvac/hvac3/state -l 1 --constraint 0 10
```

### HVAC 6
```bash
python plan.py -w weights/hvac/hvac6 -d HVAC -i HVAC6 -s 6 -a 6 --get_state temp/test/hvac/hvac6/state -l 1 --constraint 0 10
```

### Reservoir 3
```bash
python plan.py -w weights/reservoir/reservoir3 -d Reservoir -i Reservoir3 -s 3 -a 3 --get_state temp/test/reservoir/reservoir3/state -l 1
```

### Reservoir 4
```bash
python plan.py -w weights/reservoir/reservoir4 -d Reservoir -i Reservoir4 -s 4 -a 4 --get_state temp/test/reservoir/reservoir4/state -l 1
```

## RDDL Simulator Planning

The following commands are used in RDDL simulator we provided [here](https://github.com/wuga214/PULLREQUEST_rddlsim)
The RDDL simulator would call python code in this repository. Please note the TensorflowPolicy needs the python code address in your computer.
Modify `Python_Repo` in the TensorflowPolicy.java before running.

### Navigation 8x8
```bash
./run rddl.sim.Simulator -R /media/wuga/Storage/JAIR-18/rddls/Navigation/8x8/Navigation_Radius.rddl -P rddl.policy.domain.navigation.TensorflowPolicy -I is1 -V rddl.viz.GenericScreenDisplay
```

### Navigation 10x10
```bash
./run rddl.sim.Simulator -R /media/wuga/Storage/JAIR-18/rddls/Navigation/10x10/Navigation_Radius.rddl -P rddl.policy.domain.navigation.TensorflowPolicy -I is1 -V rddl.viz.GenericScreenDisplay
```

### HVAC 3
```bash
./run rddl.sim.Simulator -R /media/wuga/Storage/JAIR-18/rddls/HVAC/ROOM_3/HVAC_VAV.rddl2 -P rddl.policy.domain.HVAC.TensorflowPolicy -I inst_hvac_vav_fix -V rddl.viz.GenericScreenDisplay
```
Planning through Backpropagation
===

This is a refined version of Tensorflow planner on planning problem. 

In the training stage, we train the transition functions through the previous observations.
In another words, we assume the trainsition function is unknown while the reward function is given.

The code is able to connect to the RDDL simulator by calling python through commandline tools.


# Example
Train
```bash
python train.py \
-p data/res/reservoir4/ \
-x Reservoir_Data.txt \
-y Reservoir_Label.txt \
-w weights/reservoir/reservoir4 \
-s 4 \
-d Reservoir
```

Plan
```bash
python plan.py \
-w weights/reservoir/reservoir3 \
-d Reservoir \
-i Reservoir3 \
-s 3 \
-a 3 \
--initial temp/state
```

More concrete examples could be found in `Commands.md` file.

Note: 
1. the initial state is optional, and the default is zero state.
2. Action constrain need to manually set before running planner.



### HVAC 6
```bash
./run rddl.sim.Simulator -R /media/wuga/Storage/JAIR-18/rddls/HVAC/ROOM_6/HVAC_VAV.rddl2 -P rddl.policy.domain.HVAC.TensorflowPolicy -I inst_hvac_vav_fix -V rddl.viz.GenericScreenDisplay
```

### Reservoir 3
```bash
./run rddl.sim.Simulator -R /media/wuga/Storage/JAIR-18/rddls/Reservoir/Reservoir_3/Reservoir.rddl -P rddl.policy.domain.reservoir.TensorflowPolicy -I is1 -V rddl.viz.GenericScreenDisplay
```

### Reservoir 4
```bash
./run rddl.sim.Simulator -R /media/wuga/Storage/JAIR-18/rddls/Reservoir/Reservoir_4/Reservoir.rddl -P rddl.policy.domain.reservoir.TensorflowPolicy -I is1 -V rddl.viz.GenericScreenDisplay
```