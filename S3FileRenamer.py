#!/usr/bin/env python3

"""
Find and remove characters from directories and files that pose difficulty in Amazon S3.
See https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html for a list of characters.

This will generate a double pipe-delimited file for review.
Default behavior is to only generate the log file for review.  Pass the "--rename" or "-r" flag to rename files
and/or the "--delete" or "-d" flag to delete files.

Renaming will replace the following characters with an underscore:
 "&", "$", "@", "=", ";", "+", ",", "?", "\\", "{", "^", "}", "%", "`", "]", "\"", ">", "[", "~", "<", "#", "|"

 Deleting will delete files and folders that match these patterns:
    Start with "." or "~$"
    Ends with ".tmp"
    Is named "Thumbs.db"
 """

from os import walk, remove
from os.path import exists, join, splitext, isfile
from shutil import rmtree, move
from argparse import ArgumentParser


def needs_rename(string):
    """Search input string for illegal characters.  If found, return True, list of characters found, cleaned name.
      If not, return False and two empty strings"""
    bad_characters = ["&", "$", "@", "=", ";", "+", ",", "?", "\\", "{", "^", "}", "%", "`", "]", "\"", ">", "[", "~",
                      "<", "#", "|"]
    replacement_character = "_"
    found_bad_characters = []
    cleaned_name = ""
    for char in string:
        if char in bad_characters:
            found_bad_characters.append(char)
            cleaned_name += replacement_character
        else:
            cleaned_name += char
    if len(found_bad_characters) > 0:
        return True, found_bad_characters, cleaned_name
    else:
        return False, "", ""


def is_temp_file(fname):
    """Determine if file matches pattern of temp files"""
    if fname.startswith("~$") or fname.startswith(".") or fname == "thumbs.db" or \
            splitext(fname)[1].lower() == ".tmp":
        return True
    else:
        return False


def is_temp_dir(dname):
    """Determine if directory matches pattern for temp directory"""
    if dname.startswith("."):
        return True
    else:
        return False


def generate_log(log_dir, path):
    """Generate double-pipe delimited log file of all actions to be taken."""
    log_file = open(join(log_dir, "rename.log"), "w")
    log_file.write("ACTION||CHARACTERS||ORIGINAL NAME||NEW NAME||TYPE\n")
    for root, dirs, files in walk(path):
        for file in files:
            log_line = False
            if is_temp_file(file):
                log_line = "DELETE||''||{}||''||FILE\n".format(join(root, file))
            else:
                found, characters_found, new_name = needs_rename(file)
                if found:
                    log_line = "RENAME||{}||{}||{}||FILE\n".format(" ".join(characters_found), join(root, file),
                                                                   join(root, new_name))
            if log_line:
                log_file.write(log_line)
        for dir in dirs:
            log_line = False
            if is_temp_dir(dir):
                log_line = "DELETE||''||{}||''||DIR\n".format(join(root, dir))
            else:
                found, characters_found, new_name = needs_rename(dir)
                if found:
                    log_line = "RENAME||{}||{}||{}||FILE\n".format(" ".join(characters_found), join(root, dir),
                                                join(root, new_name))
            if log_line:
                log_file.write(log_line)
        log_file.close()
        return join(log_dir, "rename.log")


if __name__ == "__main__":
    parser = ArgumentParser(description="Find and replace S3-illegal characters")
    parser.add_argument("-r", "--rename", help="Perform rename action.", action="store_true", default=False)
    parser.add_argument("-p", '--path', help="Path to data directory", required=True)
    parser.add_argument("-l", '--log', help="Path to log file directory", required=True)
    parser.add_argument("-d", "--delete", help="Delete temp files and directories.", action="store_true", default=False)
    args = vars(parser.parse_args())
    path = args["path"]
    do_rename = args["rename"]
    do_delete = args["delete"]
    log_directory = args["log"]
    logfile = generate_log(log_directory, path)
    if do_delete or do_rename:
        log = open(logfile, "r")
        for line in log:
            line = line.strip()
            action, chars, original, new, objtype = line.split("||")
            if do_delete and action == "DELETE":
                print("DELETING {} {}".format(objtype, original))
                if objtype == "DIR":
                    rmtree(original)
                if objtype == "FILE":
                    try:
                        remove(original)
                    except FileNotFoundError:
                        pass
            if do_rename and action == "RENAME":
                print("Renaming {} {}".format(objtype, original))
                try:
                    move(original, new)
                except FileNotFoundError:
                    pass


