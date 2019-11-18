# accelergy-table-based-plug-in

An energy estimation plug-in template for [Accelergy framework](https://github.com/nelliewu95/accelergy)
This template is designed to provide a starting point for table-based estimation plug-ins.


## Get started 
- Install [Accelergy framework](https://github.com/nelliewu95/accelergy)

## Overview of the Plug-in
This plug-in serves as the entry point for all user-defined sets of tables of different hardware attributes,
action types, technologies, etc. 

## Create your own set of tables

### YAML identifier file
A YAML identifier file for your set of tables should be placed in  ```YAML_identifiers```.

#### Examples
```YAML_identifiers``` contains two example YAML identifier files.

#### Rules
The name of the YAML file must end with ```table.yaml``` and following information needs to be provided in the file:
 - The name of the set of tables
 - The supported technology 
 - The accuracy of your set of tables
 - The path to the directory that contains all your csv data files

You should install the plug-in (with the same option as the Accelergy installation) every time you add more identifier file(s) by ```pip install .```


### CSV data tables 
You can create your csv tables anywhere in you file structure as long as the path pointer in the identifier file is correct.

#### Examples
```example_csv_tables``` folder provides the necessary headers for all default primitive component classes.  
```counter.csv``` and ```regfile.csv``` are populated with random data to show what should be filled in the cells.
#### Rules
There are several rules for creating these data files:
- Data tables must be in csv format.
- The name of the file should be ```<primitive component class name>.csv```, e.g., SRAM.csv for SRAM energy data.
- The necessary hardware attribute names, action names, argument names are the headers(the first row) of the csv, and their corresponding values are filled in the cells.
- The energy column must have a header called "energy".
 
 
