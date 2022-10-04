from Classes.ImageObj import ImageObj
import os
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

    @classmethod
    def remove_allfiles(cls, folder_dir):
        lst_files = list()
        try:
            lst_files = os.listdir(folder_dir)
        except Exception as e:
            print("Error Retrieving files on %s, cause: %s"%(folder_dir, e))
        
        for filename in lst_files:
            curr_file_path = os.path.join(folder_dir,filename)
            try:
                if os.path.isfile(curr_file_path):
                    os.unlink(curr_file_path)
                elif os.path.isdir(curr_file_path):
                    cls.remove_allfiles(curr_file_path)
            except Exception as e:
                print("Deletion of file %s, cause: %s"%(curr_file_path, e))

    @classmethod
    def check_file_ifexists(cls, curr_file_path):
        return os.path.exists(curr_file_path)