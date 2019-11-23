# accelergy-table-based-plug-ins

An energy estimation plug-in for [Accelergy framework](https://github.com/nelliewu96/accelergy). This plug-in provides an entry point for easy creation of various energy tables.


## Get started 
- Install [Accelergy framework](https://github.com/nelliewu95/accelergy) (if you have not yet).
- Run ```pip install .``` with the same options you used for installing Accelergy.   
- The installation installs a command ```accelergyTables``` to your system.


## Try the provided example set of table templates
#### Populate the provided table templates (can skip if don't want to add more data to templates)
At least one row of example filled cells are provided in the templates.
Populate the cells with your own data.
Run ```pip install .``` to reinstall the updated data files

#### Add root
Add the root to the provided set of tables by running ```accelergyTables```. 

#### Run accelergy

You should see the following in the printed log：
  - The ```table-based-plug-ins``` is found by accelergy.
  - The ```table-based-plug-ins``` identifies a set of tables called ```test_tables```.
  
Note that most of the provided energy tables do not contain numerical data. 

## Create your own set of tables

### Add the root to your sets of tables 
Add the root to your sets of tables to the Accelergy config file by running
```
accelergyTables -r $myRoot
```

You can also manually add the root in the ```~/.config/accelergy/accelergy_config.yaml``` file.

The plug-in will recursively search the subdirectories of the provided root to locate various sets of tables

### YAML identifier file
A YAML identifier file that describes the basic information of your set of tables needs to be created.  
```set_of_table_templates``` contains an example YAML identifier file ```test.table.yaml```.

The name of the YAML file must end with ```table.yaml``` and following information needs to be provided in the file:
 - The name of the set of tables
 - The supported technology 
 - The accuracy of your set of tables
 - The path to the directory that contains all your csv data files


### CSV data tables 
You can create your csv tables anywhere in you file structure as long as the path pointer in its identifier file is correct.

```set_of_table_templates/data``` folder provides the necessary headers for all default primitive component classes.  
```counter.csv``` and ```regfile.csv``` are populated with random data to show what should be filled in the cells.

There are several rules for creating these data files:
- Data tables must be in csv format.
- The name of the file should be ```<primitive component class name>.csv```, e.g., SRAM.csv for SRAM energy data.
- The necessary hardware attribute names, action names, argument names are the headers(the first row) of the csv, and their corresponding values are filled in the cells.
- The energy column must have a header called "energy".
 
