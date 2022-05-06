import ray
print("init ray")
ray.init()

@ray.remote
def f(x):
    return x *x

print("construct futures")
futures = [f.remote(i) for i in range(4)]
print("get futures")
print(ray.get(futures))
