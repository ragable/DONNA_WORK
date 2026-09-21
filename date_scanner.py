r = list(range(1,3860))
def scan_dates():
    f = open('datescan.txt','w')
    for num in list(range(1,3860)):
        fname = f'/data/KEEPERS/2026_9/message{num}.txt'
        with open(fname,'r') as f1:
            data = f1.readlines()
            f.write(f'{num}: {data[3]}')
            f.flush()

if __name__ == '__main__':
    scan_dates()

