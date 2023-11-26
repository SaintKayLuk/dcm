import pydicom
import os
import uuid
from dcm import my_mysql


# 加密dcm
def dcm_encryption(dcm_path, hospital_id):
    dicom = pydicom.dcmread(dcm_path)
    name = str(dicom.PatientName)
    # id已经是uuid则跳过，判断是否32位
    # 是否已经脱敏了，但是数据库里没有的数据
    if not len(dicom.PatientID) == 32:
        dicom.id = ''.join(str(uuid.uuid3(uuid.NAMESPACE_URL, dicom.PatientID)).split('-'))
        # 写入数据库
        dicom.hospital_id = hospital_id
        my_mysql.insert_dicom(dicom)
        # 更新属性
        dicom.PatientName = '000'
        dicom.PatientID = dicom.id
        dicom.InstitutionName = hospital_id
        dicom.InstitutionAddress = '000'
        if 'ContributingEquipmentSequence' in dicom:
            dicom.__delattr__('ContributingEquipmentSequence')

        dicom.save_as(dcm_path, dicom)
        # dicom.sa
        # print(patient_name, ' 已成功脱敏')
        # 参数不够，或者去除所有，保留需要的
        return name + ' 脱敏成功 \n'
        # if name not in name_set:
        #     name_set.add(name)
        # output_text(name)
    else:
        return dicom.PatientID + ' 已经脱敏,不需要重复操作 \n'


# 解密
def dcm_decryption(path):
    # 判断文件是否存在，并且为后缀为 dcm
    if os.path.exists(path):
        if os.path.isfile(path):
            if path.split('.')[-1] == 'dcm':
                dicom = pydicom.dcmread(path)
                dicom.id = dicom.PatientID
                result = my_mysql.select_dicom(dicom.id)
                if result is not None:
                    return '医院：' + result[0] + '\n' + '患者id：' + result[1] + '\n' + '患者姓名：' + result[2] + '\n' + '机构名称：' + result[3] + '\n' + '机构地址：' + result[
                        4] + '\n'
                else:
                    return '没有这个记录 \n'
            else:
                return '文件不是dcm文件 \n'
        else:
            return '路径不是文件 \n'
    else:
        return '路径不存在 \n'
