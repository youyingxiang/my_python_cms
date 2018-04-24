from redis import Redis

redis_crud = Redis(host='127.0.0.1',port='6379')

def set(key,value,ex=''):
    return redis_crud.set(key,value,ex)

def get(key):
    return redis_crud.get(key)

def delete(key):
    return redis_crud.delete(key)