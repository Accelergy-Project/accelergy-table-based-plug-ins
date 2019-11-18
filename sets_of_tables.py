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
        self.estimator_name = 'sets_of_tables'
        self.sets_of_tables = self.summarize_sets_of_tables()
        self.energy_holder = [] # holds the results retrieved by primitive_action_supported
        print('-------', self.sets_of_tables)
    # ------- Interface functions with Accelergy --------#
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
            self.energy_holder = [] # reset energy holder
            self.energy_holder.append(interface)
            self.energy_holder.append(estimated_energy)
        return max_accuracy

    def estimate_energy(self, interface):
        if len(self.energy_holder) == 0 or not self.energy_holder[0] == interface:
            print(self.estimator_name, ': ERROR -- There is no energy held in energy holder or held energy incorrect')
            print('Received Request: ', interface)
            print('Energy Holder Data: ', self.energy_holder)
            sys.exit(0)
        else:
            return self.energy_holder[1]

    # -------- Utility functions -------#
    def select_best_set(self, interface):
        """ Select the best set of tables according to the recorded identifiers """
        max_accuracy = 0
        estimated_energy = None
        primitive_class_name = interface['class_name']
        for set_name, set_identifier in self.sets_of_tables.items():
            if str(interface['attributes']['technology']) == str(set_identifier['technology']) and \
               set_identifier['accuracy'] > max_accuracy and \
               primitive_class_name in set_identifier['supported_primitive_classes']:
                # check if there are matching attributes and actions
                supported, estimated_energy = self.walk_csv(interface, set_identifier['path_to_data_dir'])
                if supported:
                    max_accuracy = set_identifier['accuracy']
        return max_accuracy, estimated_energy


    def walk_csv(self, interface, data_dir_path):
        """ Check if there is corresponding entry for the requested attributes and actions """
        supported = False
        energy = None
        csv_file_path = os.path.join(data_dir_path, interface['class_name'] + '.csv')
        with open(csv_file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if supported:
                    break
                attr_matched = True
                # check if hardware attributes are present in the csv file
                for attr_name, attr_val in interface['attributes'].items():
                    if not attr_name in row or not row[attr_name] == str(attr_val):
                        attr_matched = False
                        break # attributes not matched, next row
                # check if action name (and arguments) are present in the csv file (given attributes are there)
                if attr_matched:
                    if row['action'] == interface['action_name']: # if action name match
                        arg_matched = True
                        if interface['arguments'] is not None:
                            for arg_name, arg_val in interface['arguments'].items():
                                if not arg_name in row or not row[arg_name] == str(arg_val):
                                    arg_matched = False
                                    break  # arg not matched, next row
                        if arg_matched:
                            supported = True
                            energy = float(row['energy'])
        return supported, energy


    def summarize_sets_of_tables(self):
        """ Collect the information stored in identifier YAML files for all sets of tables"""
        sets_of_tables_info = {}
        file_dir = os.path.dirname(__file__)
        for root, directories, filenames in os.walk(os.path.join(file_dir, 'sets_of_tables')):
            for filename in filenames:
                if 'table.yaml' in filename:  # locate a set of tables
                    identifier_path = root + os.sep + filename
                    identifier = yaml.load(open(identifier_path), Loader=yaml.SafeLoader)
                    set_name = identifier['name']

                    # Check the required keys
                    if 'accuracy' not in identifier or 'technology' not in identifier \
                            or 'name' not in identifier or 'path_to_data_dir' not in identifier:
                        print('ERROR-- ', os.path.join(root, identifier_path),
                              'Identifier YAML file for each set of tables must contain the following keys: \n'
                              '"name", "technology", "accuracy", "path_to_data_dir"')
                        sys.exit(0)


                    if not os.path.isabs(identifier['path_to_data_dir']):
                        # must provide absolute path the directory that stores the csv tables
                        print(self.estimator_name, ': ERROR in ', set_name, 'identifier YAML',
                                                   ' -- not absolute path to the data folder')
                        sys.exit(0)

                    supported_primitive_classes = []
                    for data_root, data_directories, data_filenames in os.walk(identifier['path_to_data_dir']):
                        for data_filename in data_filenames:
                            if '.csv' in data_filename:
                                supported_primitive_classes.append(data_filename[0:-4])
                    identifier['supported_primitive_classes'] = supported_primitive_classes
                    set_name in sets_of_tables_info and print(self.estimator_name, ':',
                        ' WARN -- Repeated table set name:', set_name)
                    sets_of_tables_info[set_name] = identifier

        return sets_of_tables_info