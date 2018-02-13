from maat import maat_scale, Invalid

def validate_args(validation_dic, fail_is_none=False, custom_exception=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(args) > 0:
                kwargs.update(zip(func.func_code.co_varnames, args))
            try:
                cleaned_kwargs = maat_scale(kwargs, validation_dic)
            except Invalid as e:
                if fail_is_none:
                    return None
                elif custom_exception is not None:
                    raise custom_exception
                else:
                    raise
            return func(**cleaned_kwargs)
        return wrapper
    return decorator


def valid_kwargs(func, kwargs):
    return {k: v for k, v in  kwargs.items() if k in func.__code__.co_varnames}


def chain_validation(validation_func, fail_is_none=False, custom_exception=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(args) > 0:
                kwargs.update(zip(func.func_code.co_varnames, args))
            try:
                kwargs['val']= validation_func(**valid_kwargs(validation_func, kwargs))
                result = func(**valid_kwargs(func, kwargs))
            except Invalid as e:
                if fail_is_none:
                    return None
                elif custom_exception is not None:
                    raise custom_exception
                else:
                    raise
            return result 
        return wrapper
    return decorator

