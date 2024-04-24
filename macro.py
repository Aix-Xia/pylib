# import sys
# class __LINE__(object):
#     def __repr__(self):
#         try:
#             raise Exception
#         except:
#             return str(sys.exc_info()[2].tb_frame.f_back.f_lineno)

import inspect

class __LINE__:
    def __repr__(self):
        try:
            raise Exception
        except:
            stack_t = inspect.stack()
            ttt = inspect.getframeinfo(stack_t[1][0])
            return str(ttt.lineno)
class __FILE__:
    def __repr__(self):
        try:
            raise Exception
        except:
            stack_t = inspect.stack()
            ttt = inspect.getframeinfo(stack_t[1][0])
            return ttt.filename
class __FUNC__:
    def __repr__(self):
        try:
            raise Exception
        except:
            stack_t = inspect.stack()
            ttt = inspect.getframeinfo(stack_t[1][0])
            return str(ttt.function)


__FILE__ = __FILE__()
__LINE__ = __LINE__()
__FUNC__ = __FUNC__()

if __name__ == '__main__':
    print("this line is %s" %__LINE__)
