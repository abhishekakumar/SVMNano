### DeepNano: alternative basecaller for MinION reads

DeepNano is alternative basecaller for Oxford Nanopore MinION reads
based on deep recurrent neural networks.

Currently it works with SQK-MAP-006 and SQK-MAP-005 chemistry and as a postprocessor for Metrichor.

Here are our benchmarks for SQK-MAP-006 chemistry, which compare mapping accuracy (we trained on reads which align to one half on the
Ecoli and tested on other half of Ecoli and Klebsiela):

|                  | Ecoli Metrichor | Ecoli DeepNano | Klebsiella Metrichor | Klebsiella DeepNano |
|------------------|-----------------|----------------|----------------------|---------------------|
| Template reads   | 71.3%           | 77.9%          | 68.1%                | 76.3%               |
| Complement reads | 71.4%           | 76.4%          | 69.5%                | 75.7%               |
| 2D reads         | 86.8%           | 88.5%          | 84.8%                | 86.7%               |

Links to datasets with reads:

- http://www.ebi.ac.uk/ena/data/view/ERR1147230
- https://www.ebi.ac.uk/ena/data/view/SAMEA3713789


Requirements
================

We use Python 2.7.

Here are versions of Python packages, that we used:

- Cython==0.23.4
- numpy==1.10.2
- h5py==2.5.0
- Theano==0.7.0
- python-dateutil==2.5.0

Basic usage:
================

For SQK-MAP-006 chemistry just use:

`OMP_NUM_THREADS=1 python basecall.py <list of fast5 files>`

or 

`OMP_NUM_THREADS=1 python basecall.py --directory <directory with reads>`

It outputs basecalls for template, complement and 2D into file named output.fasta.

For SQK-MAP-005 chemistry use:

`OMP_NUM_THREADS=1 python basecall.py --template_net nets_data/map5temp.npz --complement_net nets_data/map5comp.npz --big_net nets_data/map5-2d.npz <list of fast5 files>`

For R9 and R9.4 check r9 directory.

Advanced arguments:
=================

- `-h` - prints help message
- `--template_net PATH` - path to network which basecalls template (has reasonable default)
- `--complement_net PATH` - path to network which basecalls complement (has reasonable default)
- `--big_net PATH` - path to network which basecalls 2D (has reasonable default)
- `--timing` - if set, display timing information for each read
- `--type template/complement/2d/all` - type of basecalling output (defaults to all)
- `--output FILENAME` - output filename
- `--output_orig` - if set, outputs also Metrichor basecalls
- `--directory DIRECTORY` Directory where read files are stored

Usage without metrichor:
================

Basecaller above used spliting to template and
complement, scaling parameters and alignment from metrichor.

The tools below does not require metrichor at some expense at accuracy.
Currently the accuracy for 1D basecall is almost similar as for the tools above
(except for some reads where we really mess up scaling).
The accuracy for 2D basecall is approximatelly 0.5% lower than for metrichor (whereas
the tool above was 2% better than metrichor). 

To use this tool, first compile alignment code:
`g++ -O2 -std=gnu++0x align_2d.cc -o align_2d`

Then run:

`OMP_NUM_THREADS=1 python basecall_no_metrichor.py <list of fast5 files>`

Arguments:

- `-h` - prints help message
- `--template_net PATH` - path to network which basecalls template (has reasonable default)
- `--complement_net PATH` - path to network which basecalls complement (has reasonable default)
- `--big_net PATH` - path to network which basecalls 2D (has reasonable default)
- `--type template/complement/2d/all` - type of basecalling output (defaults to all)
- `--output FILENAME` - output filename
- `--directory DIRECTORY` Directory where read files are stored

If you want to watch a directory for new files, first install:

- watchdog==0.8.3

And then use (the output parameter has no effect, we output separate fasta files for each fast5 file):

`OMP_NUM_THREADS=1 python basecall_no_metrichor.py --watch <directory name>`

