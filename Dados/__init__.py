"""
This folder contains the data structure of the entire aplication.
It only has the data structure, it will be treated in the other packages
These subpackages are divided according to the SSA manual.
Some of these packages will be loaded and edited, others not. The importance
is that this code remains easy to expand in a more "reader-friendly" style.

Here is the order of the topics
1 - [Script Info]
2 - [V4Styles]
3 - [Events]

"""
__all__ = ["Events", "ScriptInfo", "V4Styles", "SubPackage", "ErrorPackage"]
