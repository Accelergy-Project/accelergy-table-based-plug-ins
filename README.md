# accelergy-table-based-plug-in

An energy estimation plug-in template for [Accelergy framework](https://github.com/nelliewu95/accelergy)
This template is designed to provide a starting point for table-based estimation plug-ins


## Get started 
- Install [Accelergy framework](https://github.com/nelliewu95/accelergy)

## Overview of the Plug-in
This plug-in serves as the entry point for all user-defined sets of tables of different hardware attributes,
action types, technologies, etc. 

## Create your own set of tables
The set of tables should be in csv format and stored in a folder called ```data```, and a YAML file that specifies 
the basic information about the set of tables should be placed in the same directory as the ```data``` folder.

The name of the YAML file must end with ```table.yaml``` and following information needs to be provided in the file:
 - The name of the set of tables
 - The supported technology 
 - The list of supported primitive component types  
 - The accuracy of the your set of tables
 
Example YAML specification of the user-defined set of tables:
 ```yaml
name: eyeriss_tables             # name of the set of tables
technology: 65nm                 # technology supported by the set of tables
accuracy： 95                    # the accuracy of the provided tables(in your units)
path_to_data_dir: ./data         # absolute paths to set of tables
supported_primitive_components:  # primitive components supported by the set of tables
 - SRAM
 - regfile
 - intmac
 - counter
 - FIFO
 - wire
 - comparator
```
 


## Create your own table-based plug-in
- Clone the repo by ```git clone https://github.com/nelliewu95/accelergy-aladdin-plug-in.git```
- Populate the csv files in the ```/data/``` folder according to your process technology
    - If you are using the default primitive component library provided by Accelergy:   
      The attribute and argument names are already provided.
      You can find the possible action names and argument values for the primitive components in Accelergy's
      provided [default primitive component library](https://github.com/nelliewu95/accelergy/blob/master/share/primitive_component_libs/primitive_component.lib.yaml)
    - If you are using you own primitive component library.  
      You might need to modify the csv files such that the attribute names and argument names match with your specification.
- Create files needed to for a plug-in installation
   ```python
   python init_script.py <estimator_name>
  ```
    The command above created the files needed to install a plug-in called ```estimator_name```. You should see three
    files generated in the root directory: ```setup.py```, ```<estimator_name>.estimator.yaml```, and ```<estimator_name>.py```.
 - Install the plug-in. Make sure you use the same arguments as installing Accelergy
   ```
    pip3 install .
   ```
   The plug-in should not be installed in the ```$YourPythonInstallationPath$/share/accelergy/estimation_plug_ins/``` folder
 - When you run Accelergy, it should now be able to identify your plug-in.
 
 ## Clean up 
 If you want to clean up the generated files, run ```python init_script clean```