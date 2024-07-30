import sys
import time

debug = True
header = ' debug start '
tail = ' debug end '
str_len = 100
line_info = '''
try:
    raise Exception
except:
    f = sys.exc_info()[2].tb_frame.f_back
print(f'  code name: "{f.f_code.co_name}";    code line No: {f.f_lineno}  '.center(str_len, '*'))
'''
# def DebugPrint(*args, **kwargs):
#     if debug:
#

def debug(func): # Decorator
    def run(*args, **kwargs):
        print(header.center(str_len, '*'))
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back
        print(f'  code name: "{f.f_code.co_name}";    code line No: {f.f_lineno}  '.center(str_len, '*'))
        result = func(*args, **kwargs)
        print(tail.center(str_len, '*'), end='\n\n')
        return result
    return run

def timer(func): # Decorator
    def run(*args, **kwargs):
        print(header.center(str_len, '*'))
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back
        print(f'  code name: "{f.f_code.co_name}";    code line No: {f.f_lineno}  '.center(str_len, '*'))
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        t = t1 - t0
        print(f' <{func.__name__}> has run {1000 * t:.3f}ms '.center(str_len, '*'), end='\n')
        print(tail.center(str_len, '*'), end='\n\n')
        return result
    return run

@debug
def print_time():
    ticks = time.time()
    tick_str = str(ticks).ljust(20, '0')
    pidx = tick_str.find('.')
    lct = time.localtime(ticks)
    year = lct.tm_year
    month = lct.tm_mon
    day = lct.tm_mday
    hour = lct.tm_mday
    minute = lct.tm_min
    sec = lct.tm_sec
    msec = tick_str[pidx+1:pidx+4]
    usec = tick_str[pidx+4:pidx+7]
    nsec = tick_str[pidx+7:pidx+10]
    print(f'\t\t{year}-{month}-{day} {hour}:{minute}:{sec}\n\t\t{msec}ms {usec}us {nsec}ns')

@debug
def print_mark(*args, **kwargs):
    print_paremeter_list = ['sep', 'end', 'file', 'flush']
    for key in dict(kwargs).keys():
        if key not in print_paremeter_list:
            del kwargs['key']
    print(*args, **kwargs)

@debug
def print_list(*args, **kwargs):
    def get_list(*args):
        for data in args:
            if type(data)==list or type(data)==tuple or type(data)==set:
                get_list(*data)
            elif type(data)==int or type(data)==float or type(data)==str or type(data)==bool:
                lst.append(data)
            else:
                warning(f'{data} type is {type(data)}, has not define')
    lst = []
    get_list(*args)
    print_paremeter_list = ['sep', 'end', 'file', 'flush']
    for key in dict(kwargs).keys():
        if key not in print_paremeter_list:
            del kwargs['key']
    print(*lst, **kwargs)

@debug
def print_dict(dictionary:dict):
    for key, value in dictionary.items():
        print(f'{key}\t: {value}')

@debug
def print_class(clst, *args):
    """
    :param clst: class list or class multiple list
    :param args: class parameter name(string)
    :return: None
    """
    def inner(clst, *args):
        if len(args) != 0:
            print(*args, sep='\t')
        for cls in clst:
            if type(cls) in [list, set, tuple]:
                inner(cls)
            else:
                if len(args) == 0:
                    print(cls)
                else:
                    for param in args:
                        item = f'cls.{param}'
                        try:
                            print(eval(item), end='\t')
                        except Exception:
                            print('NA', end='\t')
                    print()
    inner(clst, *args)

@debug
def print_parameter(**kwargs):
    title = ''
    data = ''
    for key, value in kwargs.items():
        l = max(len(str(key)), len(str(value)))
        title += str(key).center(l + 4, ' ')
        data += str(value).center(l + 4, ' ')
    print(title[2:-2], data[2:-2], sep='\n')

@debug
def print_sympy_result(result:dict):
    rDict = {}
    for key, value in result.items():
        rDict[str(key)] = value
    print_parameter(**rDict)


def warning(string:str, show_type:int=0, front_color:int=33, back_color:int=40, **kwargs):
    """
    :param string:打印字符
    :param show_type:显示方式
        0:默认值;  1:高亮;  22:非粗体;  4:下划线;  24:非下划线;  5:闪烁;  25:非闪烁; 7:反显;  27:非反显
    :param front_color:前景色
        30:黑色;  31:红色;  32:绿色;  33:黄色;  34:蓝色;  35:品红;  36:青色;  37:白色
    :param back_color:背景色
        40:黑色;  41:红色;  42:绿色;  43:黄色;  44:蓝色;  45:品红;  46:青色;  47:白色
    :return:
    """
    print_paremeter_list = ['sep', 'end', 'file', 'flush']
    for key in dict(kwargs).keys():
        if key not in print_paremeter_list:
            del kwargs['key']
    result = f'\033[{show_type};{front_color};{back_color}m[WARNING]{string}\033[0m'
    print(result, **kwargs)

def error(s:str):
    return f' {s} '.center(str_len, '*')

class TIME:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
    def __repr__(self):
        keep = True
        if self.start_time != 0:
            str_start = 'time start : %f\n' %self.start_time
        else:
            str_start = 'time start : None\n'
            keep = False
        if self.end_time != 0:
            str_end = 'time end   : %f\n' %self.end_time
        else:
            str_end = 'time end   : None\n'
            keep = False
        if keep:
            str_keep = 'time continue : %f\n' %(self.end_time - self.start_time)
        else:
            str_keep = ''
        rstr = header + '\n' + str_start + str_end + str_keep + tail + '\n\n'
        return rstr
    def start(self):
        self.end_time = 0
        self.start_time = time.time()
    def timing(self, reset=False):
        _time = time.time()
        if self.start_time == 0:
            self.start_time = _time
        elif reset:
            retention = _time - self.start_time
            self.start_time = _time
            self.end_time = 0
            print_mark('function has run %f s' %retention)
            return retention
        else:
            retention = _time - self.start_time
            self.end_time = _time
            print_mark('function has run %f s' % retention)
            return retention
    def end(self):
        self.end_time = time.time()
        retention = self.end_time - self.start_time
        print_mark('function has run %f s'%retention)
        return retention
    def reset(self):
        self.start_time = 0
        self.end_time = 0

if __name__ == '__main__':
    warning('adfsfsdf')