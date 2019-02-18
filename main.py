import math

def get_leftmost(b):
    # Ex: 1101 -> 1000
    return "1" + ("0" * (len(b)-1))

def dec_to_hex(m):
    string  = ""
    hex_num = hex(int(m))
    if (hex_num[0] == "-"):
        string += "-"
    string += hex_num.split('x')[-1]
    return string.upper()

def find_n_pos(m):
    #Finds position numerically when m can be written as 2^n
    n         = int(math.log(m, 2))
    magnitude = pow(math.sqrt(2), n)
    theta     = (math.pi/2) - ((math.pi/4)*n)
    return [int(magnitude*math.cos(theta)), int(magnitude*math.sin(theta))]

def find_coordinate(m):
    pos = [0, 0]
    # If m can be written as 2^n, go straight to find_n_pos
    if (math.ceil(math.log(m, 2)) == math.floor(math.log(m, 2))):
        pos = find_n_pos(m)
    # Otherwise break binary form of m into chunks and solve recursively
    else:
        bin_m          = bin(m)[2:]
        reached_middle = False
        f_chunk        = ""
        s_chunk        = ""
        # Break m into chunks, Ex: 1100101 -> 1100000 and 101
        for bit in bin_m:
            if not reached_middle:
                if (bit == "0"):
                    reached_middle = True
                f_chunk += bit
            else:
                f_chunk += "0"
                s_chunk += bit
        # Get pos for first chunk: pos of first bit - pos of other bits
        pos = find_n_pos(int(get_leftmost(f_chunk), 2))
        for i in range(1, len(f_chunk)):
            if f_chunk[i] == "0":
                break
            t_pos = find_n_pos(int(get_leftmost(f_chunk[i:]), 2))
            pos[0] -= t_pos[0]
            pos[1] -= t_pos[1]
        # Recursively find pos for second chunk, subtract from first chunk
        if (len(s_chunk) > 0 and int(s_chunk, 2) != 0):
            t_pos = find_coordinate(int(s_chunk, 2))
            pos[0] -= t_pos[0]
            pos[1] -= t_pos[1]
    return pos

if __name__ == "__main__":
    q = int(input())
    for i in range(q):
        n   = input()
        m   = int(input().strip(), 16)
        pos = find_coordinate(m)
        print(dec_to_hex(pos[0]))
        print(dec_to_hex(pos[1]))
