import os


class FileManagement:
    """
        Object for managing file input and output.
    """
    def __init__(self, pathname=None):
        """
            :param pathname: Path for Input/Output folders. If not specified. It will use the default folder. Default
            folder is 2020ASSEditor/Testing/
        """

        if pathname is not None:
            if os.path.isdir(pathname) is False:
                raise ValueError(f"Not an existing directory path.")

            self.__inputlocation__ = self.connectpath(f"{pathname}", "Input/")
            self.__outputlocation__ = self.connectpath(f"{pathname}", "Output/")
        else:
            # This is expecting that the module wasn't imported by a project outside 2020ASSEditor
            thisplace = FileManagement.upperpath(f"{__file__}")
            thisplace = FileManagement.upperpath(thisplace)
            thisplace = FileManagement.upperpath(thisplace)
            thisplace = FileManagement.connectpath(thisplace, "Testing//")

            self.__inputlocation__ = self.connectpath(f"{thisplace}", "Input/")
            self.__outputlocation__ = self.connectpath(f"{thisplace}", "Output/")

    @staticmethod
    def connectpath(path1, path2):
        """Trying to connect 2 paths in a way compatible for both windows and unix"""
        outpath = os.path.normcase(path1)
        outpath = os.path.join(outpath, os.path.normcase(path2))
        outpath = os.path.normpath(outpath)
        return outpath

    @staticmethod
    def upperpath(path1):
        """ Returns path1 upper directory."""
        return os.path.split(path1)[0]

    def __repr__(self):
        saida = f"{self.__inputlocation__}    {os.path.isdir(self.__inputlocation__)}\n"
        saida += f"{self.__outputlocation__}    {os.path.isdir(self.__outputlocation__)}"
        return saida


if __name__ == "__main__":
    # thisplace = FileManagement.upperpath(f"{__file__}")
    # thisplace = FileManagement.upperpath(thisplace)
    # thisplace = FileManagement.upperpath(thisplace)
    # thisplace = FileManagement.connectpath(thisplace, "Testing//")
    # for _ in range(2):
    #     thisplace = os.path.split(thisplace)[0]
    # x = FileManagement(thisplace)
    # print(thisplace)
    # y = os.path.dirname(thisplace)
    # print(y)
    x = FileManagement()
    print(f"{x}")




