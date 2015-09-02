''''' 
Created on 2011-4-25 
 
@author: barton 
'''  
import os  
import shutil  
import sys  
  
source_folder = "/home/barton/Desktop/tmp" # 源　文件夹  
target_folder = "/home/barton/Desktop/tmp2" # 目标　文件夹  
  
  
def syncdir(source_folder, target_folder):  
    """ 这里递归同步每一个文件夹下的文件 """  
      
    if(not os.path.exists(target_folder)): #　目标文件夹不存在，就先建一个出来  
        os.mkdir(target_folder)  
  
    for file in os.listdir(source_folder): # 遍历　源文件夹下的所有文件（包括文件夹）。用os.path.walk，或许会更方便些，那样递归都省去了。  
          
        from_file = os.path.join(source_folder, file)  
        to_file = os.path.join(target_folder, file)  
          
        if(os.path.isdir(from_file)): # 如果是文件夹，递归  
            syncdir(from_file, to_file)  
        else:   
            if(iscopy(from_file, to_file)): # 看是否需要拷贝  
                shutil.copy2(from_file, target_folder) # 执行copy。。。   
                print("copy %s from %s to %s;" % (file , from_file , to_file)) # 
            else:  
                print("The file %s is exist" % to_file)  
  
  
def iscopy(from_file, to_file):  
    ''''' 决断　是否　需要　拷贝。如果需要，返回True，否则返回False '''  
      
    if(not os.path.exists(to_file)): # 目标文件还不存在，当然要拷过去啦  
        return True  
      
    from_file_modify_time = round(os.stat(from_file).st_mtime, 1) # 这里精确度为0.1秒  
    to_file_modify_time = round(os.stat(to_file).st_mtime, 1) # 拿到　两边文件的最后修改时间  
    if(from_file_modify_time > to_file_modify_time): # 比较　两边文件的　最后修改时间  
        return True  
      
    return False  
  
  
if __name__ == '__main__':  
    ''''' 这里是传说中的　主入口 '''  
#    if(not os.path.exists(source_folder) or not os.path.isdir(source_folder)):  
    if(not os.path.isdir(source_folder)): # 发现第一个条件没有，也是一样的  
        print("The source folder:%s is not exist" % source_folder)  
        sys.exit() # 这个时候，就要退出江湖了。。。最初写的时候，敲了个return，哈哈。。。  
          
    syncdir(source_folder, target_folder) # 这里是　同步的入口  
      
    print("All files has been sync") 