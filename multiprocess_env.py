import ray

class RayVectorEnv():
    """
    リモートの環境をまとめて一般的な環境のインターフェースを提供する．
    """
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