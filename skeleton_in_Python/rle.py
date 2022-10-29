#helper functions the perform run-length encoding and decoding

def convert_to_binary(number):
    # input: number
    # output: binary representation of the number
    binary = []
    while number > 0:
        binary.append(number % 2)
        number = number // 2
    string = ''.join(str(x) for x in binary)
    return string

def encode(array):
    # input: of '0's and '1's
    # output: list of the '0' symbol run lengths and '1' symbol run lengths
    char = ''
    values = []
    global count
    count = 0
    run_lengths = []
    runs = []
    intial_value = array[0]
    print('Before RLE:', len(array))
    for i in array:
        # if the value is the same as the initial value
        if i == intial_value:
            count += 1
        # get the run lengths of the '0' and '1' symbols
        else:
            run_lengths.append(count)
            values.append(intial_value)
            count = 1
            intial_value = i
    # get the last run length
    for run_length in run_lengths:
        run_length = convert_to_binary(run_length)
        # binary of run lengths
        runs.append(run_length)
    final = ("".join("{}{}".format(x, y) for x, y in zip(values, run_lengths)))
    return str(final)

def get_bit_count(value):
    # get bit count from json file
   bit = 0
   before = len(value) * 8
   after = 0
   while value:
       bit += 1
       after += bit * len(value)
   print("Before RLE:", before)
   print("After RLE:", after)

def get_run_lengths(array):
    # input: of '0's and '1's
    # output: list of the '0' symbol run lengths and '1' symbol run lengths
    run_lengths = []
    initial_value = array[0]
    count = 0
    for i in array:
        if i != initial_value:
            count += 1
            run_lengths.append(i)
        else:
            initial_value = i
            count = 1
    return run_lengths

def get_values(array):
    # get the values of the run lengths
    values = []
    initial_value = array[0]
    for i in array:
        if i == initial_value:
            values.append(i)
        else:
            initial_value = i
            count = 1
    return values

def decode(array):
    # input: list of the '0' symbol run lengths and '1' symbol run lengths
    # output: of '0's and '1's
    list1 = []
    values = list(array[::2])
    run_lengths = list(array[1::2])
    values = [int(i) for i in values]
    run_lengths = [int(i) for i in run_lengths]
    for i in range(len(run_lengths)):
        list1.append(str(values[i]) * run_lengths[i])
    list_string = "".join(list1)
    print('After RLE decode', list_string.__len__())
    return list_string

def calculate_bits(array):
    # get bit count from json file
    bit = 0
    for i in array:
        bit += len(i)
    return bit