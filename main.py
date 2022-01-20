import filecmp
import os.path

def Myreport(self):  # Print a report on the differences between a and b
    # Output format is purposely lousy
    print('check in:', self.left, self.right)
    if self.left_only:
        self.left_only.sort()
        print('Only in', self.left, ':', self.left_only)
    if self.right_only:
        self.right_only.sort()
        print('Only in', self.right, ':', self.right_only)
    if self.diff_files:
        self.diff_files.sort()
        print('Differing files :', self.diff_files)
    if self.funny_files:
        self.funny_files.sort()
        print('Trouble with common files :', self.funny_files)
    if self.common_funny:
        self.common_funny.sort()
        print('Common funny cases :', self.common_funny)


def are_dir_trees_equal(dir1, dir2):
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    @param dir1: First directory path
    @param dir2: Second directory path

    @return: True if the directory trees are the same and
        there were no errors while accessing the directories or files,
        False otherwise.
   """
    dirs_cmp = filecmp.dircmp(dir1, dir2)
    Myreport(dirs_cmp)
    if len(dirs_cmp.left_only)>0 or len(dirs_cmp.right_only)>0 or \
        len(dirs_cmp.funny_files)>0:
        return False
    (_, mismatch, errors) =  filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False)
    if len(mismatch)>0 or len(errors)>0:
        return False
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not are_dir_trees_equal(new_dir1, new_dir2):
            return False
    return True

print(are_dir_trees_equal('dir1','dir2'))
