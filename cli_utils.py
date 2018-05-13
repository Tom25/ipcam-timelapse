import sys

def get_cli_arg(arg_name):
    return get_cli_arg_with_default(arg_name, None)

def get_cli_arg_with_default(arg_name, default_value):
    arg_value = default_value
    if has_cli_arg(arg_name):
        arg_value_index = sys.argv.index(arg_name) + 1
        if len(sys.argv) >= arg_value_index + 1:
            arg_value = sys.argv[arg_value_index]

    return arg_value

def has_cli_arg(arg_name):
    if len(sys.argv) > 1 and arg_name in sys.argv:
        return True
    return False
