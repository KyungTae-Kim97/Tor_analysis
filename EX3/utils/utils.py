import math

def last_percent_elements(tensor, percent):
    assert 0 < percent <= 100, "Percent must be between 0 and 100"
    n = math.ceil(tensor.size(1) * percent / 100)
    modified_tensor = tensor.detach().clone()
    # modified_tensor[:,0:-n,:]=0
    modified_tensor[:,n:,:]=0
    return modified_tensor

def get_value_of_last_percent_elements(size, percent):
    n = math.ceil(size * percent / 100)
    return n
