import inspect
import ray

def make_method(composition_name, func_name):
    """
    インスタンスのメソッドをコンポジションのものに移譲する関数を出力する
    composition_name: str 
        移譲したいコンポジションの変数名(self.変数名)
    func_name: str
        移譲したい関数名
    """
    def inner_func(self, *args, **kwargs):
        composition_object = getattr(self, composition_name)  # self."composition_name"
        composition_object_func = getattr(composition_object, func_name) 
        return composition_object_func(*args, **kwargs)  # self."composition_name"."func_name"(*args, **kwargs)
    return inner_func


def delegation_all_method(cls, composition_name, composition_cls):
    """
    クラスにメソッドを追加する関数
    cls: classオブジェクト
        移譲元のリモートのためのクラス
    composition_name: str 
        移譲したいコンポジションの変数名(self.変数名)
    composition_cls: classオブジェクト
        移譲先のクラス
    """
    for name, _ in inspect.getmembers(composition_cls):
        if name.startswith('__'):
            continue
        if callable(getattr(composition_cls, name)):
            set_func = make_method(composition_name, name)
            setattr(cls, name, set_func) 


def make_remote_class(cls, composition_name, composition_cls):
    """
    インターフェースとなる関数．コンポジションの親クラスに，子クラスのメソッドに移譲されるメソッドを追加する．
    cls: classオブジェクト
        移譲元のリモートのためのクラス
    composition_name: str 
        移譲したいコンポジションの変数名(self.変数名)
    composition_cls: classオブジェクト
        移譲先のクラス
    returns
    -------
    メソッドが追加された新しいクラス
    """
    delegation_all_method(cls, composition_name, composition_cls)
    cls = ray.remote(cls)
    return cls