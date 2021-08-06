import threading
import argparse
import wget

myfile = ""
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", type=str, help="Input file", required=True)
parser.add_argument("-t", "--threads", type=int, help="how many threads?", default=10)

args = parser.parse_args()

if args.file.strip() == "":
    print("You need to specify a file")
    exit()


def run_download(Self, line):
    for url in line:
        if url[:4] == "http":
            print('\nDownloading file' + wget.filename_from_url(url))
            wget.download(str(url))


myfile = open(args.file.strip(), "r")
alllines = myfile.read()
list_lines = alllines.splitlines();
urldown = []
start = 0
threads = []

lines_per_thread = int(len(list_lines) / args.threads)

print ("Lines per thread: " + str(lines_per_thread))

for x in range(0, args.threads):
    if x + 1 == args.threads:
        urldown.append(list_lines[start:])
    else:
        urldown.append(list_lines[start:lines_per_thread])
    start = start + lines_per_thread + 1

for i in range(10):
    t = threading.Thread(target=run_download, args=(None, urldown[i],))
    threads.append(t)
    t.start()

for i in threads:
    i.join()

print("finished...")
