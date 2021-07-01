import os
import argparse
import pathlib
import ast
from fnmatch import fnmatch
import csv, time

current_path = pathlib.Path().absolute()

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str, help="Specify the path", default=current_path)
args = parser.parse_args()

root = args.path
extension = "*.java"
# asserts classification
nb_assert = 0
nb_equals = 0
nb_not_equals = 0
nb_true = 0
nb_false = 0
nb_that = 0
nb_throws = 0
nb_not_null = 0
nb_not_same = 0
nb_timeout = 0
nb_fail = 0
nb_array_equals = 0
nb_does_not_throw = 0
nb_iterable_equals = 0
nb_lines_match = 0
nb_same = 0
nb_null = 0
nb_timeout_preemptively = 0
# primitives classification
nb_int = 0
nb_float = 0
nb_boolean = 0
nb_string = 0
nb_class = 0
nb_unclassified = 0
nb_error = 0


def count_type(str):
    global nb_class, nb_string, nb_int, nb_float, nb_boolean, nb_unclassified, nb_error
    if str == "UNKNOW": 
        nb_unclassified += 1 # We don't know if it's a string or a variable name
    elif str == "CLASS":
        nb_class += 1
    elif str == "STRING":
        nb_string += 1
    elif str == "BOOL":
        nb_boolean += 1
    elif str == "INT":
        nb_int += 1
    elif str == "FLOAT":
        nb_float += 1
    else:
        nb_error += 1

def check_type(str):
    str=str.strip()
    if len(str) == 0: return 'UNKNOW'
    elif str == "true" or str == "false":
        return 'BOOL'
    elif str.startswith('"') and str.endswith('"'):
        return 'STRING'
    elif str.endswith('.class'):
        return 'CLASS'
    try:
        t=ast.literal_eval(str)
    except ValueError:
        return 'UNKNOW'
    except SyntaxError:
        return 'UNKNOW'
    else:
        if type(t) in [int, float]:
            if type(t) is int :
                return 'INT'
            if type(t) is float:
                return 'FLOAT'
        else:
            return 'UNKNOW' 


for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, extension):
            file_path = os.path.join(path, name)
            with open(file_path) as fp:
                for line in fp:
                    if "assertEquals(" in line:
                        print(line.strip())
                        nb_assert += 1
                        nb_equals += 1
                        tmp = line.strip().replace("()", "") # remove lambda expression
                        tmp = tmp[tmp.find("(")+1:tmp.find(")")] # capture parameters
                        params = list(filter(None, tmp.split(",", 1)))
                        print(len(params), params)
                        if(len(params) == 2):
                            param1 = check_type(params[0])
                            param2 = check_type(params[1])
                            if(param1 == "UNKNOW" and param2 == "UNKNOW"):
                                count_type("UNKNOW")
                                print("UNKNOW")
                            elif(param1 != "UNKNOW" and param2 == "UNKNOW"):
                                count_type(param1)
                                print(param1)
                            elif(param1 == "UNKNOW" and param2 != "UNKNOW"):
                                count_type(param2)
                                print(param2)
                        else:
                            nb_unclassified += 1
                            print("UNCLASSIFIED")
                    elif "assertNotEquals(" in line:
                        nb_assert += 1
                        nb_not_equals += 1
                        tmp = line.strip().replace("()", "") # remove lambda expression
                        tmp = tmp[tmp.find("(")+1:tmp.find(")")] # capture parameters
                        params = list(filter(None, tmp.split(",", 1)))
                        print(len(params), params)
                        if(len(params) == 2):
                            param1 = check_type(params[0])
                            param2 = check_type(params[1])
                            if(param1 == "UNKNOW" and param2 == "UNKNOW"):
                                count_type("UNKNOW")
                                print("UNKNOW")
                            elif(param1 != "UNKNOW" and param2 == "UNKNOW"):
                                count_type(param1)
                                print(param1)
                            elif(param1 == "UNKNOW" and param2 != "UNKNOW"):
                                count_type(param2)
                                print(param2)
                        else:
                            nb_unclassified += 1
                            print("UNCLASSIFIED")
                    elif "assertTrue(" in line:
                        nb_assert += 1
                        nb_true += 1
                    elif "assertFalse(" in line:
                        nb_assert += 1
                        nb_false += 1
                    elif "assertThat(" in line:
                        nb_assert += 1
                        nb_that += 1
                    elif "assertThrows(" in line:
                        nb_assert += 1
                        nb_throws += 1
                    elif "assertNotNull(" in line:
                        nb_assert += 1
                        nb_not_null += 1
                    elif "assertNotSame(" in line:
                        nb_assert += 1
                        nb_not_same += 1
                    elif "assertTimeout(" in line:
                        nb_assert += 1
                        nb_timeout += 1
                    elif "fail(" in line:
                        nb_assert += 1
                        nb_fail += 1
                    elif "assertArrayEquals(" in line:
                        nb_assert += 1
                        nb_array_equals += 1
                    elif "assertDoesNotThrow(" in line:
                        nb_assert += 1
                        nb_does_not_throw += 1
                    elif "assertIterableEquals(" in line:
                        nb_assert += 1
                        nb_iterable_equals += 1
                    elif "assertLinesMatch(" in line:
                        nb_assert += 1
                        nb_lines_match += 1
                    elif "assertSame(" in line:
                        nb_assert += 1
                        nb_same += 1
                    elif "assertNull(" in line:
                        nb_assert += 1
                        nb_null += 1
                    elif "assertTimeoutPreemptively(" in line:
                        nb_assert += 1
                        nb_timeout_preemptively += 1

total_types = nb_class + nb_string + nb_int + nb_float + nb_boolean + nb_unclassified + nb_error
localtime = time.asctime(time.localtime(time.time()))

with open(localtime +'junit-parser.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["project"   ,"total_assert",  "nb_equals", "nb_not_equals", "nb_true", "nb_false", "nb_throws", "nb_does_not_throw", "nb_null", "nb_not_null", "nb_same", "nb_not_same", "nb_array_equals", "nb_timeout", "nb_timeout_preemptively", "nb_iterable_equals", "nb_lines_match", "nb_fail", "total_types", "nb_class", "nb_string", "nb_int", "nb_float", "nb_boolean", "nb_unclassified", "nb_error"])
    writer.writerow([ args.path  ,nb_assert,        nb_equals,   nb_not_equals,   nb_true,   nb_false,   nb_throws,   nb_does_not_throw,   nb_null,   nb_not_null,   nb_same,   nb_not_same,   nb_array_equals,   nb_timeout,   nb_timeout_preemptively,   nb_iterable_equals,   nb_lines_match,   nb_fail,   total_types,   nb_class,   nb_string,   nb_int,   nb_float,   nb_boolean,   nb_unclassified,   nb_error])
