import sys
from contextlib import redirect_stdout

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
                print('Submessage')
                return -1
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
        return False
    output = lines[ndcs[0]:ndcs[1]]
    ofname = f'Messages/message{mspan[0]}.txt'

    with open(ofname, "w") as f:
        f.writelines(output)
    for line in output:
        sys.stdout.write(line)
    return True


if __name__ == "__main__":
    i = 3001
    j = 0
    while True: 
        stat = process('Donna_Letters_2.txt',[i,j])    
        j += 1
        if i == 4000:
            break
        if not stat:
            i += 1
            j = 0

                       




