import sys
# Convert integer into hex string format for output
def dec_to_hex(x):
    string = ""
    hex_num = hex(int(x))
    if hex_num[0] == "-":
        string += "-"
    string += hex_num.split('x')[-1]
    return string.upper()


# Find the sum of the given array of lengths of binary numbers and return as int
# Binary numbers always consist of a single '1' followed by a number of '0's
def calc_sum(array):
    bin_arr = []
    sum = 0
    if len(array) > 0:
        bin_arr.append('0')
    for n in array:
        while n >= len(bin_arr):
            bin_arr.append('0')
        if bin_arr[n] == '1':
            bin_arr[n] = '0'
            bin_arr.append('1')
        else:
            bin_arr[n] = '1'
    if len(bin_arr) > 0:
        sum = int(''.join(bin_arr[::-1]), 2)
    return sum


# Subtract the x-array of the negative pos 2-d array from the x-array of the
# positive pos 2-d array, and repeat with the corresponding y-arrays
def calc_final_pos(p_pos, n_pos):
    p_pos[0] = p_pos[0][::-1]
    p_pos[1] = p_pos[1][::-1]
    n_pos[0] = n_pos[0][::-1]
    n_pos[1] = n_pos[1][::-1]
    pos = [0, 0]
    pos[0] = calc_sum(p_pos[0]) - calc_sum(n_pos[0])
    pos[1] = calc_sum(p_pos[1]) - calc_sum(n_pos[1])
    return pos


# Add (m - 1) % 2 to pos array based on angle around origin, where m
# is the length of the binary number being considered in the chunking algorithm
def find_n(m, p_pos, n_pos, polarity):
    n = m - 1
    x = n // 2
    theta = n % 8
    x_p = polarity
    y_p = polarity
    if 5 <= theta <= 7:
        x_p *= -1
    if 3 <= theta <= 5:
        y_p *= -1
    if n % 2 == 1:
        if x_p == 1:
            p_pos[0].append(x)
        else:
            n_pos[0].append(x)
        if y_p == 1:
            p_pos[1].append(x)
        else:
            n_pos[1].append(x)
    elif n % 4 == 0:
        if y_p == 1:
            p_pos[1].append(x)
        else:
            n_pos[1].append(x)
    elif n % 2 == 0:
        if x_p == 1:
            p_pos[0].append(x)
        else:
            n_pos[0].append(x)


# Efficient implementation of chunking algorithm
def get_pos(bin_m):
    chunk_sign = 1
    bit_sign = 1
    flip = False
    size = len(bin_m)
    p_pos = [[], []]
    n_pos = [[], []]
    for i in range(size):
        if bin_m[i] == '1':
            if i > 0 and bin_m[i-1] == '0':
                chunk_sign *= -1
                bit_sign = 1
                flip = True
            polarity = chunk_sign * bit_sign
            find_n(size - i, p_pos, n_pos, polarity)
            if flip:
                bit_sign = -1
                flip = False
            if i == 0:
                bit_sign = -1
    return calc_final_pos(p_pos, n_pos)

### END OF FUNCTION DEFINITIONS - START OF MAIN ###

# identify if file used as input, or using STDIN
if len(sys.argv) > 1:
    infile = open(sys.argv[1])
else:
    infile = sys.stdin

# parse through content and operate
q = int(infile.readline())
for i in range(q):
    infile.readline()
    m = int(infile.readline(), 16)
    pos = get_pos(bin(m)[2:])
    print(dec_to_hex(pos[0]))
    print(dec_to_hex(pos[1]))
