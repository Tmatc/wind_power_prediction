import os
from src.utils.DataSetting import DataSetting



if __name__ == "__main__":
    ds = DataSetting()
    flist = ds("dasai_dhp")
    print(flist)