
This file has been created automatically. Please adapt it to your needs.

## Content

The content of this DUNE module has been extracted from the module `dumux`.
In particular, the following subfolders of `dumux` have been extracted:
*   `examples`

Additionally, all headers in `dumux` that are required to build the
executables from the sources
*   `/Users/ouetsu/dumuxday/dumux/examples/1protationsymmetry/main.cc`
*   `/Users/ouetsu/dumuxday/dumux/examples/2pinfiltration/main.cc`
*   `/Users/ouetsu/dumuxday/dumux/examples/1ptracer/main.cc`
*   `/Users/ouetsu/dumuxday/dumux/examples/liddrivencavity/main.cc`
*   `/Users/ouetsu/dumuxday/dumux/examples/freeflowchannel/main.cc`
*   `/Users/ouetsu/dumuxday/dumux/examples/biomineralization/main.cc`
*   `/Users/ouetsu/dumuxday/dumux/examples/shallowwaterfriction/main.cc`
*   `/Users/ouetsu/dumuxday/dumux/examples/porenetwork_upscaling/main.cc`

have been extracted. You can configure the module just like any other DUNE
module by using `dunecontrol`. For building and running the executables,
please go to the build folders corresponding to the sources listed above.


## Version Information

| module folder                                      | branch                                             | commit hash                                        | commit date                    |
| -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- | ------------------------------ |
| dune-alugrid                                       | origin/releases/2.7                                | 178a69b69eca8bf3e31ddce0fd8c990fee4931ae           | 2020-08-17 21:21:32 +0200      |
| dune-istl                                          | origin/releases/2.7                                | 761b28aa1deaa786ec55584ace99667545f1b493           | 2020-11-26 23:29:21 +0000      |
| dune-grid                                          | origin/releases/2.7                                | b7741c6599528bc42017e25f70eb6dd3b5780277           | 2020-11-26 23:30:08 +0000      |
| dumux                                              | origin/master                                      | ab9389eb2bd5527163a5518f9a858328c003cad0           | 2021-06-28 13:23:57 +0000      |
| dune-localfunctions                                | origin/releases/2.7                                | 68f1bcf32d9068c258707d241624a08b771b6fde           | 2020-11-26 23:45:36 +0000      |
| dune-geometry                                      | origin/releases/2.7                                | 9d56be3e286bc761dd5d453332a8d793eff00cbe           | 2020-11-26 23:26:48 +0000      |
| dune-foamgrid                                      | origin/master                                      | d49187be4940227c945ced02f8457ccc9d47536a           | 2020-01-06 15:36:03 +0000      |
| dune-common                                        | origin/master                                      | fae77c751103bd6effa9d215ffc4c32b434e0ae4           | 2021-01-20 10:09:50 +0000      |


## Installation

The installation procedure is done as follows :
Create a root folder, e.g. `DUMUX`, enter the previously created folder,
clone the remote and use the install script `install_dumux-test.py`
provided in this repository to install all dependent modules.

```sh
mkdir DUMUX
cd DUMUX
git clone git@github.com:tkdxwb/testpy.git
python3 dumux-test/install_dumux-test.py
```

This will clone all modules into the directory `DUMUX`,
configure your module with `dunecontrol` and build tests.

