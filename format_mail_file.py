import sys
from contextlib import redirect_stdout
message_key1 = 'MESSAGE'
message_key2 = 'Original Message'
class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, data):
        for f in self.files:
            f.write(data)

    def flush(self):
        for f in self.files:
            f.flush()

def format(lines):
    output_lines = []
    for line in lines:
        while len(line) > 80:
            line_length_array = list(range(len(line)))
            pairs = list(zip(line,line_length_array))
            blank_indices = [pair[1] for pair in pairs if pair[0] == ' ']
            bool_array = [bi >= 80 for bi in blank_indices]
            if True in bool_array:
                cutoff = blank_indices[bool_array.index(True)]
            else:
                output_lines.append(line)
                line = line[len(line):]
                continue
            output_lines.append(line[:cutoff] + '\n')
            line = line[cutoff + 1:]
        if line:
            output_lines.append(line)

    return output_lines

        

def get(mspan,messages,submessages):
    submsgnos = []
    for msgno in messages:
        for submsgno in submessages[list(messages).index(msgno)]:
            submsgnos.append(submsgno)
    all_messages = sorted(list(messages.values()) + submsgnos)
    second  = None
    if mspan[1]:
        ndx = list(messages.values()).index(messages[mspan[0]])
        if 0 < mspan[1] <= len(submessages[ndx] ):               
            first = submessages[list(messages).index(mspan[0])][mspan[1]-1]
            ndx = all_messages.index(first)
            ndx += 1
            if ndx < len(all_messages):
                second = all_messages[ndx]
            else:
                print(f"{mspan[1]} is out of range, sorry. Bye")
                return -1    
        else:
            print(f"{mspan[1]} is out of range. Sorry. Bye")
            return -1
    else:
        first = messages[mspan[0]]
        ndx = all_messages.index(first)
        if ndx < len(all_messages):
            next_ndx = ndx + 1
            second = all_messages[next_ndx]
        else:
            pass
    return [first,second]



    
    


def process(infname,mspan):
    #with open(infname,'r') as f:
    #    lines = f.readlines()
    #    lines = [line for line in lines if line != '\n']
    #    ofname = infname.split('.')[0] + '_1.' + infname.split('.')[1]
    #with open(ofname,'w') as f:
    #    f.writelines(lines)
    #with open(infname,'r') as f:
    #    lines = f.readlines()
    #lines = format(lines)
    #ofname = infname.split('.')[0] + '_2.' + infname.split('.')[1]
    #with open(ofname,'w') as f:
    #    f.writelines(lines)
    with open(infname,'r') as f:
        lines = f.readlines()

    msgnos = {}
    submsgnos = []
    for i,line in enumerate(lines):
        if "MESSAGE " in line:
            msgnos[int(line.split()[1])] = i - 1
            submsgnos.append([])
        elif "Original Message" in line:
            submsgnos[-1].append(i)
    submsgnos[-1].append(i)



    ndcs = get(mspan,msgnos,submsgnos)
    if ndcs == -1:
        return
    output = lines[ndcs[0]:ndcs[1]]
    ofname = f'message{mspan[0]}_sub{mspan[1]}.txt'
    #print("TYPE:", type(output))
    #print("NUMBER OF ELEMENTS:", len(output))

    #for i in range(min(10, len(output))):
    #   print(i, repr(output[i]))
    with open(ofname, "w") as f:
        f.writelines(output)
    for line in output:
        sys.stdout.write(line)


if __name__ == "__main__":
    process('/data/DONNA_WORK/Donna_Letters_2.txt',[150,0])
                   




