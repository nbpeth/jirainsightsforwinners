import pandas as pd
import sys

# What?
# This script aggregates a JIRA issues CSV export by issue type and story points.
# Download a CSV export of your JIRA issues and run this script to get a summary of the story points by issue type.

def parse_args(args):
    arg_dict = {}
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=')
            arg_dict[key] = value
    return arg_dict

args = parse_args(sys.argv[1:])

if not args:
    raise ValueError(
        '''
        No arguments provided

        csvpath: (required) path to the csv file
        point-field-name: (optional) name of the field that contains the story points (default: Custom field (Story Points))
        type-field-name: (optional) name of the field that contains the issue type (default: Issue Type)

        Example: `$ python3 issues.py csvpath=issues.csv point-field-name=StoryPoints type-field-name=Type`

        ''')

csv_file_path = args.get('csvpath')
if not csv_file_path:
    raise ValueError("csvpath is required")

point_field_name = args.get('point-field-name')
type_field_name = args.get('type-field-name')

if not point_field_name:
    point_field_name = "Custom field (Story Points)"
if not type_field_name:
    type_field_name = "Issue Type"

print("loading file", csv_file_path)
raw_df = pd.read_csv(csv_file_path)

aggregate_df = raw_df[[point_field_name, type_field_name]].groupby(type_field_name).agg({type_field_name: 'count', point_field_name: 'sum'})

print(aggregate_df)
