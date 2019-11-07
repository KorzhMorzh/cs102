def func():
    return 'sdsgjf'


if __name__=="__main__":
    import dispy, logging
    cluster = dispy.SharedJobCluster(computation=func, scheduler_node='192.168.43.37')
    job = cluster.submit()
    word = job()
    print(word)
    print('worked')
