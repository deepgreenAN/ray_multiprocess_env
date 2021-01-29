# rayによる並列環境
強化学習で利用できるマルチプロセスの環境を提供する．
並列処理は[ray](https://github.com/ray-project/ray)をベースにしているが，google colab・jupyter notebook上でrayを使うにはインポートの定義が面倒なので，スクリプトで定義された環境を簡単に利用できる関数も利用できる．`ray_multiprocess_env.RayVectorEnv`は
[pfrl.envs.MultiprocessVectorEnv](https://github.com/pfnet/pfrl/blob/master/pfrl/envs/multiprocess_vector_env.py)と同じインターフェースを提供するが，より簡単に拡張できる．
```python
import ray
ray.init()
```

```python
from ray_multiprocess_env import make_remote_class, RayVectorEnv
```

### 既存の環境を利用する場合


```python
import gym
env = gym.make('CartPole-v0')
```

クラスを確認


```python
type(env)
```




    gym.wrappers.time_limit.TimeLimit



リモートにするクラスを定義し，適当にコンポジションとする．このとき定義するクラスは何も継承できず，コンストラクタで利用するモジュールをすべてインポートする必要がある．


```python
class RayCartPoleEnv():
    def __init__(self):
        import gym
        self.env = gym.make("CartPole-v0")
```

リモートにするクラスに，移譲対象のクラスのメソッドを追加する．


```python
RayCartPoleEnv = make_remote_class(RayCartPoleEnv, "env", gym.wrappers.time_limit.TimeLimit)
```

リモート環境のリストを作成する


```python
num_env = 10
env_list = [RayCartPoleEnv.remote() for _ in range(10)]
```

並列環境を作成する


```python
batch_env = RayVectorEnv(env_list)
```


```python
obs = batch_env.reset()
obs
```




    [array([ 0.02461302,  0.01928287, -0.0068589 , -0.0377357 ]),
     array([ 0.03538106,  0.02743172, -0.01528312,  0.01407842]),
     array([-0.00178945, -0.02463692, -0.0307724 , -0.04496953]),
     array([-0.02553268, -0.00845424, -0.02039917, -0.01796084]),
     array([0.02280669, 0.02903785, 0.03069296, 0.01329361]),
     array([ 0.01224265, -0.02623292, -0.0429974 ,  0.02580464]),
     array([-0.02554594,  0.00714119,  0.03910909,  0.04157897]),
     array([ 0.0384841 ,  0.01893693,  0.00226931, -0.03498861]),
     array([0.00553206, 0.01901613, 0.02214727, 0.01695266]),
     array([-0.0082226 , -0.009542  ,  0.03775137, -0.02103424])]




```python
obs, reward, done, info = batch_env.step([1]*num_env)
obs, reward, done, info
```




    ((array([ 0.02499868,  0.2145025 , -0.00761361, -0.33257476]),
      array([ 0.0359297 ,  0.22276948, -0.01500156, -0.28338706]),
      array([-0.00228219,  0.17091247, -0.03167179, -0.3472004 ]),
      array([-0.02570177,  0.18695423, -0.02075838, -0.3170095 ]),
      array([ 0.02338744,  0.22370649,  0.03095883, -0.2695495 ]),
      array([ 0.01171799,  0.16947843, -0.04248131, -0.2801284 ]),
      array([-0.02540311,  0.20168113,  0.03994067, -0.23851267]),
      array([ 0.03886284,  0.21402627,  0.00156954, -0.32695468]),
      array([ 0.00591238,  0.21381358,  0.02248632, -0.26866108]),
      array([-0.00841344,  0.18501879,  0.03733069, -0.30157122])),
     (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
     (False, False, False, False, False, False, False, False, False, False),
     ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}))



### jupyter内で定義する場合

ray.remoteでデコレートする必要があり，さらにこのクラスのすべてのメソッド，内部で利用しかつjypyterで定義されたすべてのクラスのメソッドと関数の最初に利用するモジュール・関数をインポートする必要がある．


```python
@ray.remote
class RaySimpleEnv():
    def __init__(self):
        self.init_number = None

    def reset(self):
        import numpy as np
        import multi_process_funcs
        from multi_process_funcs import identiti_func
    
        self.init_number = np.random.randint(0,100, size=(1,))
        return identiti_func(self.init_number)

    def step(self, action):
        self.init_number += action
        return self.init_number, 0, False, None 
```


```python
num_env = 10
env_list = [RaySimpleEnv.remote() for _ in range(10)]
```

    2021-01-29 00:39:12,431	WARNING worker.py:1034 -- WARNING: 11 PYTHON workers have been started. This could be a result of using a large number of actors, or it could be a consequence of using nested tasks (see https://github.com/ray-project/ray/issues/3644) for some a discussion of workarounds.
    2021-01-29 00:39:12,432	WARNING worker.py:1034 -- WARNING: 12 PYTHON workers have been started. This could be a result of using a large number of actors, or it could be a consequence of using nested tasks (see https://github.com/ray-project/ray/issues/3644) for some a discussion of workarounds.
    


```python
batch_env = RayVectorEnv(env_list)
obs = batch_env.reset()
obs
```

    2021-01-29 00:39:14,677	WARNING worker.py:1034 -- WARNING: 6 PYTHON workers have been started. This could be a result of using a large number of actors, or it could be a consequence of using nested tasks (see https://github.com/ray-project/ray/issues/3644) for some a discussion of workarounds.
    2021-01-29 00:39:15,577	WARNING worker.py:1034 -- WARNING: 7 PYTHON workers have been started. This could be a result of using a large number of actors, or it could be a consequence of using nested tasks (see https://github.com/ray-project/ray/issues/3644) for some a discussion of workarounds.
    2021-01-29 00:39:15,671	WARNING worker.py:1034 -- WARNING: 8 PYTHON workers have been started. This could be a result of using a large number of actors, or it could be a consequence of using nested tasks (see https://github.com/ray-project/ray/issues/3644) for some a discussion of workarounds.
    2021-01-29 00:39:16,563	WARNING worker.py:1034 -- WARNING: 9 PYTHON workers have been started. This could be a result of using a large number of actors, or it could be a consequence of using nested tasks (see https://github.com/ray-project/ray/issues/3644) for some a discussion of workarounds.
    2021-01-29 00:39:16,930	WARNING worker.py:1034 -- WARNING: 10 PYTHON workers have been started. This could be a result of using a large number of actors, or it could be a consequence of using nested tasks (see https://github.com/ray-project/ray/issues/3644) for some a discussion of workarounds.
    2021-01-29 00:39:17,756	WARNING worker.py:1034 -- WARNING: 11 PYTHON workers have been started. This could be a result of using a large number of actors, or it could be a consequence of using nested tasks (see https://github.com/ray-project/ray/issues/3644) for some a discussion of workarounds.
    




    [array([4]),
     array([81]),
     array([42]),
     array([27]),
     array([70]),
     array([29]),
     array([12]),
     array([16]),
     array([98]),
     array([6])]




```python
obs, reward, done, info = batch_env.step([10]*num_env)
obs, reward, done, info
```




    ((array([14]),
      array([91]),
      array([52]),
      array([37]),
      array([80]),
      array([39]),
      array([22]),
      array([26]),
      array([108]),
      array([16])),
     (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     (False, False, False, False, False, False, False, False, False, False),
     (None, None, None, None, None, None, None, None, None, None))



### おまけ(RayVectorEnvを拡張する場合)

`RayVectorEnv`のクラスは以下で定義される．各メソッドではリモート環境のリストを`self.remote_envs`として参照し，rayの構文としてidのリストを`ray.get`の引数とする．最後の処理は返り値が複数になる場合の処理であり，`unzip`を行っている．

```python
class RayVectorEnv():
    def __init__(self,remote_envs):
        self._remote_envs = remote_envs 

    @property
    def remote_envs(self):
        return self._remote_envs

    def reset(self, *args, **kwargs):
        id_list = [remote_env.reset.remote(*args, **kwargs) for remote_env in self.remote_envs]
        out_list = ray.get(id_list)
        # それぞれの返り値の長さが複数かどうか
        if len(out_list) > 0:
            if isinstance(out_list[0], tuple):  # 一つの返り値が複数の場合
                return zip(*out_list)  # それぞれの出力のリストに変換(unzip)
            else:
                return out_list  # そのまま出力
        return None

    def step(self, actions, *args, **kwargs):
        assert len(self.remote_envs) == len(actions)
        id_list = [remote_env.step.remote(action, *args, **kwargs) for remote_env, action in zip(self.remote_envs, actions)]
        out_list = ray.get(id_list)
        if len(out_list) > 0:
            if isinstance(out_list[0], tuple):  # 一つの返り値が複数の場合
                return zip(*out_list)  # それぞれの出力のリストに変換(unzip)
            else:
                return out_list  # そのまま出力
        return None
```

上のクラスを拡張する場合は，継承してメソッドを追加すればよい．


```python

```
