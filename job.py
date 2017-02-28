#!/usr/bin/python

from worker import *
import csv
import threading
import sys

god_lock = threading.Lock()
results = []

with open(sys.argv[1], 'rb') as the_file:
  reader = csv.DictReader(the_file)
  for line in reader:
    w = Worker(line, god_lock, results)
    w.start()
    w.join()
  if not os.path.exists('./output'):
    os.makedirs('./output')

  with open('output/results.json', 'w') as outfile:
    json.dump(results, outfile)
