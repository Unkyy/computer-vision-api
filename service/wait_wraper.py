from time import sleep


def wait_wrapper(function,arg):
    inc = 1
    try:
        return function(arg)
    except:
        print("error")
        sleep(1)
        print(arg)
        if(inc > 5):
            return("error")
        inc +=1 
        wait_wrapper(function,arg)
