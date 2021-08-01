import re
# Convert input function to a mathematical expression
def input_formatted_to_func(inp):
    """Function converts input expression to a mathematical expression."""
    # Constants
    allowed_symbols = ("x", "/", "*", "-", "+", "^", "sin", "cos", "tan", "e")
    replaced_inputs = {
        "sin": "np.sin",
        "cos": "np.cos",
        "e": "np.exp",
        "^": "**"
    }

    # check if the function is valid
    if inp == "":
        raise ValueError(f"Enter a function to plot!")

    for char in re.findall("[a-zA-Z_]+", inp):
        if char not in allowed_symbols:
            # Error will communicate over stderr pipeline
            raise ValueError(f"'{char}' is not in the allowed as an input character!")

    """Here we manage spaical chars [cos - sin - ....]"""
    # Replace allowed chars with suitable methods for eval compiling.
    for before, after in replaced_inputs.items():
        inp = inp.replace(before, after)

    #  When no 'x' in the function
    if "x" not in inp:
        inp = f"({inp})*(x**0)"

    # Return a function to be used for y value calculation.
    def func(x):
        return eval(inp)

    return func

