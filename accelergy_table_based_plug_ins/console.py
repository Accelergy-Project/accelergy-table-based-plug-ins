import argparse,os,sys,yaml

def main():
    parser = argparse.ArgumentParser(
        description='accelergy_table_plug_ins serves as an entry point to search for various sets of energy tables '
                    'given the root directories configured in the accelergy config file.',
        epilog = 'To initialize to default set of energy tables, run command without arguments. \n '
                 'Examples: (1) accelergyTables (2) accelergyTables ~/tables/')
    parser.add_argument('-r', '--root', type=str, default=None,
                        help = 'add a new root to search for energy tables')
    args = parser.parse_args()
    new_root = args.root
    accelergy_config_file_path = os.path.join(os.path.expanduser('~'),'.config/accelergy/accelergy_config.yaml')
    if not os.path.exists(accelergy_config_file_path):
        print('ERROR: Cannot find exisiting accelergy config file at: ', accelergy_config_file_path)
        print('Please make sure Accelergy is properly installed and at least ran once')
        sys.exit(0)
    config_content = yaml.load(open(accelergy_config_file_path), Loader=yaml.SafeLoader)
    if 'table_plug_ins' not in config_content:
        curr_file_path = os.path.abspath(__file__)
        accelergy_share_folder_path = os.path.abspath(curr_file_path + '../../../../../../share/accelergy/')
        table_estimator_path = os.path.abspath(accelergy_share_folder_path +
                                               '/estimation_plug_ins/accelergy-table-based-plug-ins/example_set_of_tables')
        config_content['table_plug_ins'] = {'roots': [table_estimator_path]}

    if new_root is not None:
        config_content['table_plug_ins']['roots'].append(new_root)

    config_file = open(accelergy_config_file_path, 'w')
    config_file.write(yaml.dump(config_content, Dumper=yaml.SafeDumper))
    config_file.close()


