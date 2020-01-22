# MIT License
#
# Copyright (c) 2019 Yannan (Nellie) Wu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, yaml, sys, csv
class SetsOfTables(object):
    def __init__(self):
        self.estimator_name = 'table-based-plug-ins'
        self.sets_of_tables = self.summarize_sets_of_tables()
        self.holder = [] # holds the results retrieved by primitive_action_supported/primitive_area_supported
    
    # 
    # ERT interface functions 
    #
        # (1) primitive_action_supported(interface)
        # (2) estimate_energy(interface)

    def primitive_action_supported(self, interface):
        technology = interface['attributes']['technology'] \
                     if 'technology' in interface['attributes'] else None
        if technology is None:
            print(self.estimator_name, ': ',
                  '"technology" attribute needs to be provided to locate the correct set of tables')
            return 0
        max_accuracy, estimated_energy = self.select_best_set(interface)
        # record the retrieved result to avoid potential repetitive search
        if max_accuracy:
            self.holder = [] # reset energy holder
            self.holder.append(interface)
            self.holder.append(estimated_energy)
        return max_accuracy

    def estimate_energy(self, interface):
        if len(self.holder) == 0 or not self.holder[0] == interface:
            print(self.estimator_name, ': ERROR -- There is no energy held in energy holder or held energy incorrect')
            print('Received Request: ', interface)
            print('Energy Holder Data: ', self.holder)
            sys.exit(0)
        else:
            return self.holder[1]

    # 
    # ART interface functions 
    #
        # (1) primitive_area_supported(interface)
        # (2) estimate_area(interface)

    def primitive_area_supported(self, interface):
        technology = interface['attributes']['technology'] \
                     if 'technology' in interface['attributes'] else None
        if technology is None:
            print(self.estimator_name, ': ',
                  '"technology" attribute needs to be provided to locate the correct set of tables')
            return 0
        max_accuracy, estimated_area = self.select_best_set(interface)
        # record the retrieved result to avoid potential repetitive search
        if max_accuracy:
            self.holder = [] # reset energy holder
            self.holder.append(interface)
            self.holder.append(estimated_area)
        return max_accuracy

    def estimate_area(self, interface):
        if len(self.holder) == 0 or not self.holder[0] == interface:
            print(self.estimator_name, ': ERROR -- There is no energy held in energy holder or held energy incorrect')
            print('Received Request: ', interface)
            print('Energy Holder Data: ', self.holder)
            sys.exit(0)
        else:
            return self.holder[1]

    # -------- Utility functions -------#
    def select_best_set(self, interface):
        """ Select the best set of tables according to the recorded identifiers """
        max_accuracy = 0
        estimated_result = None
        primitive_class_name = interface['class_name']
        for set_name, set_identifier in self.sets_of_tables.items():
            if str(interface['attributes']['technology']) == str(set_identifier['technology']) and \
               set_identifier['accuracy'] > max_accuracy and \
               primitive_class_name in set_identifier['supported_primitive_classes']:
                # check if there are matching attributes( and actions)
                area_query = False if 'action_name' in interface else True
                supported, estimated_result = self.walk_csv(interface, set_identifier['path_to_data_dir'], area_query)
                if supported:
                    max_accuracy = set_identifier['accuracy']
        return max_accuracy, estimated_result


    def walk_csv(self, interface, data_dir_path, area_query = False):
        """ Check if there is corresponding entry for the requested attributes (and actions) """
        supported = False
        result = None
        csv_file_path = os.path.join(data_dir_path, interface['class_name'] + '.csv')
        with open(csv_file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if supported:
                    break
                attr_matched = True
                # check if hardware attributes are present in the csv file
                for attr_name, attr_val in interface['attributes'].items():
                    if attr_name in row and not row[attr_name] == str(attr_val):
                        # only check if the attributes in the provided csv match the interface,
                        # ignore the ones that are in the interface but not in csv
                        # (the users do not care the ones that are not specified in the csv)
                        attr_matched = False
                        break # attributes not matched, next row
                # check if action name (and arguments) are present in the csv file (given attributes are there)
                if attr_matched and not area_query:
                    # action query requires action and action argument check
                    if row['action'] == interface['action_name']: # if action name match
                        arg_matched = True
                        if interface['arguments'] is not None:
                            for arg_name, arg_val in interface['arguments'].items():
                                if not arg_name in row or not row[arg_name] == str(arg_val):
                                    arg_matched = False
                                    break  # arg not matched, next row
                        if arg_matched:
                            supported = True
                            result = float(row['energy'])

                if attr_matched and area_query:
                    # area query does not require action and action argument check
                    supported = True
                    result = float(row['area'])

        return supported, result


    def summarize_sets_of_tables(self):
        """ Collect the information stored in identifier YAML files for all sets of tables"""
        sets_of_tables_info = {}
        file_dir = os.path.dirname(__file__)
        accelergy_config_file = os.path.join(os.path.expanduser('~'),'.config/accelergy/accelergy_config.yaml')
        config_file_content = yaml.load(open(accelergy_config_file), Loader=yaml.SafeLoader)
        if 'table_plug_ins' not in config_file_content:
            print(self.estimator_name, ': ERROR -- cannot find the listed roots for the sets of tables')
            print('Please initialize by running: accelergyTables')
            print('A pointer to the default set of tables will be created in ~/.config/accelergy/accelergy_config.yaml')
            sys.exit(0)
        table_roots = config_file_content['table_plug_ins']['roots']

        for table_root in table_roots:
            for root, directories, filenames in os.walk(table_root):
                for filename in filenames:
                    if 'table.yaml' in filename:  # locate a set of tables
                        identifier_path = root + os.sep + filename
                        identifier = yaml.load(open(identifier_path), Loader=yaml.SafeLoader)
                        set_name = identifier['name']

                        # Check the required keys
                        if 'accuracy' not in identifier or 'technology' not in identifier \
                                or 'name' not in identifier or 'path_to_data_dir' not in identifier:
                            print('ERROR-- ', identifier_path,
                                  'Identifier YAML file for each set of tables must contain the following keys: \n'
                                  '"name", "technology", "accuracy", "path_to_data_dir"')
                            sys.exit(0)

                        if not os.path.isabs(identifier['path_to_data_dir']):
                            abs_path = os.path.abspath(os.path.join(os.path.join(root), identifier['path_to_data_dir']))
                            if not os.path.exists(abs_path):
                                print('ERROR-- ', identifier_path,
                                      'The sepcified data directory cannot be located...')
                                print('Intepreted absolute path to the specified data directory: ', abs_path)
                                sys.exit(0)
                            identifier['path_to_data_dir'] = abs_path

                        supported_primitive_classes = []
                        for data_root, data_directories, data_filenames in os.walk(identifier['path_to_data_dir']):
                            for data_filename in data_filenames:
                                if '.csv' in data_filename:
                                    supported_primitive_classes.append(data_filename[0:-4])
                        identifier['supported_primitive_classes'] = supported_primitive_classes
                        set_name in sets_of_tables_info and print(self.estimator_name, ':',
                            ' WARN -- Repeated table set name:', set_name)
                        sets_of_tables_info[set_name] = identifier
                        print(self.estimator_name, 'Identifies a set of tables named: ',set_name )

        return sets_of_tables_info
