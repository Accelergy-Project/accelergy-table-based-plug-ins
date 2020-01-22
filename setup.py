from setuptools import setup
import os, yaml, sys

def readme():
      with open('README.md') as f:
            return f.read()


def generate_data_files():
    """ generate all the data files that need to be included in the share folder """
    # include all table identifiers
    all_files = {}
    sets_of_tables_path = os.getcwd() + os.sep + 'set_of_table_templates'
    for root, directories, file_names in os.walk(sets_of_tables_path):
        for file_name in file_names:
            relative_root = os.path.relpath(root, os.getcwd())
            if relative_root not in all_files:
                all_files[relative_root] = [relative_root + os.sep + file_name]
            else:
                all_files[relative_root].append(relative_root + os.sep + file_name)

    data_files = []
    share_root = 'share/accelergy/estimation_plug_ins/accelergy-table-based-plug-ins/'
    for relative_root, list_of_files in all_files.items():
        root = share_root + relative_root
        subfolder_tuple = (root, list_of_files)
        data_files.append(subfolder_tuple)
    # include top-level py and yaml files
    data_files.append((share_root, ['sets_of_tables.py', 'table.estimator.yaml']))
    return data_files


setup(
      name = 'accelergy-table-based-plug-ins',
      version='0.1',
      description='An entry point for table-based plug-ins for Accelergy framework',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
      ],
      keywords='accelerator hardware energy estimation',
      author='Yannan Wu',
      author_email='nelliewu@mit.edu',
      license='MIT',
      data_files = generate_data_files(),
      packages=['accelergy_table_based_plug_ins'],
      entry_points={
        'console_scripts': ['accelergyTables=accelergy_table_based_plug_ins.console:main'],
      },
      install_requires = ['pyYAML'],
      python_requires = '>=3.6',
      include_package_data = True,
      zip_safe = False,
    )
