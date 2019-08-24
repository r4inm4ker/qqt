import os

class IconManager(object):
    icon_dirs = []
    icon_dirs.append()

    @classmethod
    def get_icon(cls, iconName, **kwargs):
        
        # TODO : to be completed
        itype = kwargs.get("type","path")
        size = kwargs.get("size",(20,20))

        if itype == "path":
            dirName = os.path.dirname(__file__)
            # print(dirName)
            iconDir = os.path.join(dirName,"icons")
            iconPath = os.path.join(iconDir,iconName)

            return iconPath
