import argparse
import os
import h5py
from helpers import *

parser = argparse.ArgumentParser()
parser.add_argument('type', choices=['temp', 'comp', '2d'])
parser.add_argument('source_file', type=str)
parser.add_argument('output_directory', type=str)
args = parser.parse_args()

finput = open(args.source_file)

for i, l in enumerate(finput):
  parts = l.strip().split()
  filename = ' '.join(parts[:-1])
  ref = parts[-1]
  h5 = h5py.File(filename, "r")
  
  fo = open(os.path.join(args.output_directory, "%s.txt" % i), "w")
  print >>fo, ref
  base_loc = get_base_loc(h5)
  if args.type == 'temp':
    scale, scale_sd, shift, drift = extract_scaling(h5, "template", base_loc)
    events = h5[base_loc+"/BaseCalled_%s/Events" % "template"]
    index = 0.0
    data = []
    for e in events:
      mean = (e["mean"] - shift) / scale
      stdv = e["stdv"] / scale_sd
      length = e["length"]
      print >>fo, " ".join(map(str, preproc_event(mean, stdv, length))),
      move = e["move"]
      if move == 0:
        print >>fo, "NN"
      if move == 1:
        print >>fo, "N%s" % e["model_state"][2]
      if move == 2:
        print >>fo, "%s%s" % (e["model_state"][1], e["model_state"][2])
  if args.type == 'comp':
    scale, scale_sd, shift, drift = extract_scaling(h5, "complement", base_loc)
    events = h5[base_loc+"/BaseCalled_%s/Events" % "complement"]
    index = 0.0
    data = []
    for e in events:
      mean = (e["mean"] - shift) / scale
      stdv = e["stdv"] / scale_sd
      length = e["length"]
      print >>fo, " ".join(map(str, preproc_event(mean, stdv, length))),
      move = e["move"]
      if move == 0:
        print >>fo, "NN"
      if move == 1:
        print >>fo, "N%s" % e["model_state"][2]
      if move == 2:
        print >>fo, "%s%s" % (e["model_state"][1], e["model_state"][2])
  if args.type == '2d':
    tscale, tscale_sd, tshift, tdrift = extract_scaling(h5, "template", base_loc)
    cscale, cscale_sd, cshift, cdrift = extract_scaling(h5, "complement", base_loc)
    al = h5["Analyses/Basecall_2D_000/BaseCalled_2D/Alignment"]
    temp_events = h5[base_loc+"/BaseCalled_template/Events"]
    comp_events = h5[base_loc+"/BaseCalled_complement/Events"]
    prev = None
    for a in al:
      ev = []
      if a[0] == -1:
        ev += [0, 0, 0, 0, 0]
      else:
        e = temp_events[a[0]]
        mean = (e["mean"] - tshift) / cscale
        stdv = e["stdv"] / tscale_sd
        length = e["length"]
        ev += [1] + preproc_event(mean, stdv, length)
      if a[1] == -1:
        ev += [0, 0, 0, 0, 0]
      else:
        e = comp_events[a[1]]
        mean = (e["mean"] - cshift) / cscale
        stdv = e["stdv"] / cscale_sd
        length = e["length"]
        ev += [1] + preproc_event(mean, stdv, length)
      print >>fo, " ".join(map(str, ev)),
      if prev == a[2]:
        print >>fo, "NN"
      elif not prev or a[2][:-1] == prev[1:]:
        print >>fo, "N%c" % a[2][2]
      else:
        print >>fo, "%c%c" % (a[2][1], a[2][2])


  fo.close()
  h5.close()
