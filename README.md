# Simple-Distributed-Storage-System
 
 CE7490 2021 Fall - Advanced Topics in Distributed System - Project 2: RAID-6 based distributed storage system


# Overview
RAID 6, also regarded as the double-parity RAID, is a RAID schemes that work by placing data on multiple disks and allowing input/output (I/O) operations to overlap in a balanced way, improving performance and offers redundancy to allow for disk failures within the RAID set and prevent data lost. 

Raid6 is a great filesystem, we try to reimplement its userland tools quick and frienfly.


You can explore the bullit from either:
- Store and access abstract “data objects” across storage nodes using RAID-6 for fault-tolerance.
- Include mechanisms to determine failure of storage nodes.
- Carry out rebuild of lost redundancy at a replacement storage node.
- Accommodate real files of arbitrary size, taking into account issues like RAID mapping, etc.
- Support mutable files, taking into account update of the content, and consistency issues.
- Support larger set of configurations
- read or write bigsize fileo bject by chunk mode
- recover <=2 disks
- detect 1 corrupted disk
- find which disk is corrupted
- recover 2-disk case
- mutable files
- concurrent actual read/write
- optimized and raw gf8 multiplication
- data types can be text-only or arbitrary bytes


Basically it turns this:
![btrfs_sub_list](https://user-images.githubusercontent.com/218502/53362053-99564e00-3939-11e9-9072-1d9ef617971f.PNG)



## Installation Guide
The RAID-6 system is devloped in Python environment with corresponding dependencies.

The project is supported on Linux or MacOS. 

### Installing Anaconda
Anaconda is a library that includes Python and many useful packages, as well as an environment manager called conda that makes package management simple.

Follow the [official instrutions](https://www.anaconda.com/distribution/) of Anaconda to install. Once it has been successfully installed, run the following command at terminal:

```
git clone https://github.com/GuluDeemo/CE7490-RAID6.git
cd CE7490-RAID6
conda env create -f environment.yml
```

To use Python from the environment you just created, activate the environment with

```
conda activate RAID6
```

### or Install from req

```
pip install -r requirement.txt
```


# Usage

## storage
store and access abstract “data objects” across storage nodes using RAID-6 for fault-tolerance

## mechanisms to determine failure of storage nodes


## rebuild of the lost redundancy at a replacement storage node



## RAID-6 data recovery


## analysis, synchronization mechanism and 

## disaster tolerance and recovery


## RAID-6 Data Recovery Analysis


```
Usage: btrfs-list [options] [mountpoint]

If no [mountpoint] is specified, display info for all btrfs filesystems.

  -h, --help                 display this message
  -d, --debug                enable debug output
  -q, --quiet                silence the quota disabled & quota rescan warnings
      --color=WHEN           colorize the output; WHEN can be 'never', 'always',
                               or 'auto' (default, colorize if STDOUT is a term)
  -n, --no-color             synonym of --color=never
  -H, --no-header            hide header from output

  -s, --hide-snap            hide all snapshots
  -S, --snap-only            only show snapshots
      --snap-min-excl SIZE   hide snapshots whose exclusively allocated extents
                               take up less space than SIZE
      --snap-max-excl SIZE   hide snapshots whose exclusively allocated extents
                               take up more space than SIZE
  -f, --free-space           only show free space on the filesystem

  -p, --profile PROFILE      consider data profile as 'dup', 'single', 'raid0',
                               'raid1', 'raid10', 'raid5' or 'raid6', for
                               realfree space calculation (default: autodetect)

      --show-all             show all information for each item
      --show-gen             show generation of each item
      --show-cgen            show generation at creation of each item
      --show-id              show id of each item
      --show-uuid            show uuid of each item

SIZE can be a number (in bytes), or a number followed by k, M, G, T or P.
```




```
Server Usage: 
 python  ./server.py runserver  [options] [mountpoint]

 # Start the server, different nodes under same 127.0.0.1 with different port from 1 to 13
 
[options] [mountpoint]

If no [mountpoint] is specified, display info for all btrfs filesystems.

  -h, --help                 display this message
  -d, --debug                enable debug output
  -q, --quiet                silence the quota disabled & quota rescan warnings
      --color=WHEN           colorize the output; WHEN can be 'never', 'always',
                               or 'auto' (default, colorize if STDOUT is a term)
  -p, --port              different port number

SIZE can be a number (in bytes), or a number followed by k, M, G, T or P.
```




 ## Operating Steps

 * Get into ./Nodes/node_1. node_2, node_3, node_4... as the same (you can only open 1 to 4 for test)

 * 'python ./server.py runserver' (Start the server, different nodes under same 127.0.0.1 with different port from 1 to 13)

 * Go back to master folder ./ and input 'python ./superserver.py runserver' to start the super node_

 * Open browser and get access to 'http://127.0.0.1:5000'

 * click 'Select File' to select file and upload it

 * 'http://127.0.0.1:5000/file/list' can see the file you uploaded and click the needed file to download

 * Or 'http://127.0.0.1:5000/file/download/<filename>' to download

 * 'http://127.0.0.1:5000/file/delete/<filename>' to delete files

 * Open postman and 'http://127.0.0.1:5001/rebuild/<filename+node>' to rebuild node, one request for one file synchronization
 
 
 
 
 RAID 6 Parity
-------------

RAID 6 uses 2 parity techniques to allow for up to 2 disks to become
unreadable, an xor-based technique, and a Reed-Solomon-based one (which is
based on Galois Fields).  As a way to explore these I built this simple
program based on a PDF from Kernel.org:
https://www.kernel.org/pub/linux/kernel/people/hpa/raid6.pdf

Example output:

    Original: 48 45 4c 4c 4f 
    Parity:   42 31
    
    Missing Datum
    48 45 4c 00 4f 
    48 45 4c 4c 4f 
    Pass: YES
    
    Missing Dataum and XOR Parity
    00 45 4c 4c 4f 
    48 45 4c 4c 4f 
    Pass: YES
    
    Missing 2 Data
    48 00 00 4c 4f 
    48 45 4c 4c 4f 
    Pass: YES


