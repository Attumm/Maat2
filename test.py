import maat
from maat import registered_functions, chain_validation, Invalid


@chain_validation(registered_functions['str']) 
def valid_filename(val, extensions=('jpg',)):
    """Validates a filename extension and returns the 'str' validated value.

    Raises:
        Invalid: invalid filename extension
    """
    if not '.' in val or val.split('.')[-1].lower() not in extensions:
        raise Invalid('filename {} has an invalid extension'.format(val))
    return val 


registered_functions['valid_filename'] = valid_filename

counter = {'filename': {'validator': 'valid_filename',  'max_length': 24, 'extensions': ['png', 'jpg']}}

a = maat.scale({'filename': 'a.jpg'}, counter)
print(a)

