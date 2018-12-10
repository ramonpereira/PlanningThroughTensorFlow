import tensorflow as tf
import numpy as np


class RESERVOIR(object):
    def __init__(self,
                 batch_size,
                 instance_settings,
                 **unused):
        self.batch_size = batch_size
        self.reservoirs = instance_settings['reservoirs']
        self.reservoir_num = len(instance_settings['reservoirs'])
        self.biggestmaxcap = tf.constant(instance_settings["biggestmaxcap"], dtype=tf.float32)
        self.zero = tf.constant(0, shape=[self.batch_size, self.reservoir_num], dtype=tf.float32)
        self._high_bounds(instance_settings["high_bound"])
        self._low_bounds(instance_settings["low_bound"])
        self._rains(instance_settings["rain"])
        self._max_cap(instance_settings["max_cap"])
        self._downstream(instance_settings["downstream"])
        self._downtosea(instance_settings["downtosea"])

    def _max_cap(self, max_cap_list):
        self.max_cap = tf.constant(max_cap_list, dtype=tf.float32)

    def _high_bounds(self, high_bound_list):
        self.high_bound = tf.constant(high_bound_list, dtype=tf.float32)

    def _low_bounds(self, low_bound_list):
        self.low_bound = tf.constant(low_bound_list, dtype=tf.float32)

    def _rains(self, rain_list):
        self.rain = tf.constant(rain_list, dtype=tf.float32)

    def _downstream(self, downstream):
        np_downstream = np.zeros((self.reservoir_num, self.reservoir_num))
        for i in downstream:
            m = self.reservoirs.index(i[0])
            n = self.reservoirs.index(i[1])
            np_downstream[m, n] = 1
        self.downstream = tf.constant(np_downstream, dtype=tf.float32)

    def _downtosea(self, downtosea):
        np_downtosea = np.zeros((self.reservoir_num,))
        for i in downtosea:
            m = self.reservoirs.index(i)
            np_downtosea[m] = 1
        self.downtosea = tf.constant(np_downtosea, dtype=tf.float32)

    def MAXCAP(self):
        return self.max_cap

    def HIGH_BOUND(self):
        return self.high_bound

    def LOW_BOUND(self):
        return self.low_bound

    def RAIN(self):
        return self.rain

    def DOWNSTREAM(self):
        return self.downstream

    def DOWNTOSEA(self):
        return self.downtosea

    def BIGGESTMAXCAP(self):
        return self.biggestmaxcap

    def Reward(self, states, actions):
        new_rewards = tf.where(
            tf.logical_and(tf.greater_equal(states, self.LOW_BOUND()), tf.less_equal(states, self.HIGH_BOUND())),
            self.zero,
            tf.where(tf.less(states, self.LOW_BOUND()),
                     -5 * (self.LOW_BOUND() - states),
                     -100 * (states - self.HIGH_BOUND()))
            )
        new_rewards += tf.abs(((self.HIGH_BOUND() + self.LOW_BOUND()) / 2.0) - states) * (-0.1)
        return tf.reduce_sum(-new_rewards, 1, keepdims=True)


class NAVI(object):
    def __init__(self,
                 batch_size,
                 instance_settings,
                 **unused):
        self.__dict__.update(instance_settings)
        self.batch_size = batch_size

    def MINMAZEBOUND(self):
        return self.min_maze_bound

    def MAXMAZEBOUND(self):
        return self.max_maze_bound

    def MINACTIONBOUND(self):
        return self.min_act_bound

    def MAXACTIONBOUND(self):
        return self.max_act_bound

    def GOAL(self):
        return self.goal

    def CENTER(self):
        return self.centre

    def Reward(self, states, actions):
        new_reward = -tf.reduce_sum(tf.abs(states - self.GOAL()), 1, keepdims=True)
        return new_reward

class LQR_1D_NAV(object):
    def __init__(self,
                 batch_size,
                 instance_settings,
                 **unused):
        self.__dict__.update(instance_settings)
        self.batch_size = batch_size

        self._dt(instance_settings["dt"])
        self._gx(instance_settings["gx"])
        self._h(instance_settings["H"])

    def _dt(self, dt):
        self.dt = tf.constant(dt, dtype=tf.float32)

    def _gx(self, gx):
        self.gx = tf.constant(gx, dtype=tf.float32)

    def _h(self, h):
        self.h = tf.constant(h, dtype=tf.float32)

    def DT(self):
        return self.dt

    def GX(self):
        return self.gx

    def H(self):
        return self.h

    def Reward(self, states, actions):
        value_horizon_achieved = 0
        if tf.less(states, self.h) is not None:
            value_horizon_achieved = ((actions * actions) * 0.01)

        value_x_gx = ((states - self.GX()) * (states - self.GX()))
        reward = -tf.reduce_sum(value_x_gx + value_horizon_achieved, 1, keepdims=True)
        return reward

class LQG_1D_NAV(object):
    def __init__(self,
                 batch_size,
                 instance_settings,
                 **unused):
        self.__dict__.update(instance_settings)
        self.batch_size = batch_size

        self._dt(instance_settings["dt"])
        self._gx(instance_settings["gx"])
        self._h(instance_settings["H"])

    def _dt(self, dt):
        self.dt = tf.constant(dt, dtype=tf.float32)

    def _gx(self, gx):
        self.gx = tf.constant(gx, dtype=tf.float32)

    def _h(self, h):
        self.h = tf.constant(h, dtype=tf.float32)

    def DT(self):
        return self.dt

    def GX(self):
        return self.gx

    def H(self):
        return self.h

    def Reward(self, states, actions):
        value_horizon_achieved = 0
        if tf.less(states, self.h) is not None:
            value_horizon_achieved = ((actions * actions) * 0.01)

        value_x_gx = ((states - self.GX()) * (states - self.GX()))
        reward = -tf.reduce_sum(value_x_gx + value_horizon_achieved, 1, keepdims=True)
        return reward        

# Matrix computation version update
class HVAC(object):
    def __init__(self,
                 batch_size,
                 instance_settings,
                 default_settings):
        self.__dict__.update(default_settings)
        self.rooms = instance_settings['rooms']
        self.batch_size = batch_size
        self.room_size = len(self.rooms)
        self.zero = tf.constant(0, shape=[self.batch_size, self.room_size], dtype=tf.float32)
        self._init_ADJ_Matrix(instance_settings['adj'])
        self._init_ADJOUT_MATRIX(instance_settings['adj_outside'])
        self._init_ADJHALL_MATRIX(instance_settings['adj_hall'])

    def _init_ADJ_Matrix(self, adj):
        np_adj = np.zeros((self.room_size, self.room_size))
        for i in adj:
            m = self.rooms.index(i[0])
            n = self.rooms.index(i[1])
            np_adj[m, n] = 1
            np_adj[n, m] = 1
        self.adj = tf.constant(np_adj, dtype=tf.float32)
        print('self.adj shape:{0}'.format(self.adj.get_shape()))

    def _init_ADJOUT_MATRIX(self, adj_outside):
        np_adj_outside = np.zeros((self.room_size,))
        for i in adj_outside:
            m = self.rooms.index(i)
            np_adj_outside[m] = 1
        self.adj_outside = tf.constant(np_adj_outside, dtype=tf.float32)

    def _init_ADJHALL_MATRIX(self, adj_hall):
        np_adj_hall = np.zeros((self.room_size,))
        for i in adj_hall:
            m = self.rooms.index(i)
            np_adj_hall[m] = 1
        self.adj_hall = tf.constant(np_adj_hall, dtype=tf.float32)

    def ADJ(self):
        return self.adj

    def ADJ_OUTSIDE(self):
        return self.adj_outside

    def ADJ_HALL(self):
        return self.adj_hall

    def R_OUTSIDE(self):
        return self.outside_resist

    def R_HALL(self):
        return self.hall_resist

    def R_WALL(self):
        return self.wall_resist

    def CAP(self):
        return self.cap

    def CAP_AIR(self):
        return self.cap_air

    def COST_AIR(self):
        return self.cost_air

    def TIME_DELTA(self):
        return self.time_delta

    def TEMP_AIR(self):
        return self.temp_air

    def TEMP_UP(self):
        return self.temp_up

    def TEMP_LOW(self):
        return self.temp_low

    def TEMP_OUTSIDE(self):
        return self.temp_outside

    def TEMP_HALL(self):
        return self.temp_hall

    def PENALTY(self):
        return self.penalty

    def AIR_MAX(self):
        return self.air_max

    def ZERO(self):
        return self.zero

    def Reward(self, states, actions):
        break_penalty = tf.where(tf.logical_or(tf.less(states, self.TEMP_LOW()),
                                               tf.greater(states, self.TEMP_UP())),
                                                self.PENALTY()+self.ZERO(), self.ZERO())
        dist_penalty = tf.abs(((self.TEMP_UP() + self.TEMP_LOW()) / tf.constant(2.0, dtype=tf.float32)) - states)
        ener_penalty = actions * self.COST_AIR()
        new_rewards = tf.reduce_sum(tf.constant(10.0, tf.float32) * dist_penalty + ener_penalty + break_penalty,
                                    axis=1,
                                    keepdims=True)
        return new_rewards