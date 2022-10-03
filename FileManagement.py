from ImageObj import ImageObj
class FileManager:
    def get_info(self, file_name):
        dataList = dict()
        with open(file_name, 'r') as f:
            for line in f.readlines():
                raw_data = line.rstrip("\n").split(";")
                f_name = raw_data[0]
                xPos = int(raw_data[1])
                yPos = int(raw_data[2])
                shape = raw_data[3]
                dataList[f_name] = ImageObj(f_name,xPos, yPos, shape)
        return dataList


