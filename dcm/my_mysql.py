import pymysql


# class Mysql:


# 获取医院列表
def select_hospital():
    sql = 'SELECT hospital_name,id FROM dicom_hospital'
    try:
        db = pymysql.connect(host='192.168.1.20',
                             user='root',
                             password='MneXQvu_NZaJhg8j',
                             database='braineuroo-dcm')
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()


# 插入患者记录
def insert_dicom(dicom):
    sql = 'SELECT id FROM dicom_information WHERE id = "' + dicom.id + '"'
    try:
        db = pymysql.connect(host='192.168.1.20',
                             user='root',
                             password='MneXQvu_NZaJhg8j',
                             database='braineuroo-dcm')
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is None:
            if not dicom.get('PatientName'):
                if not dicom.get('InstitutionAddress'):
                    dicom.InstitutionAddress = ''
            sql = 'INSERT INTO dicom_information ( id, hospital_id, patient_name, patient_id, institution_name ,institution_address)' \
                  'VALUES("' + dicom.id + '","' + dicom.hospital_id + '","' + str(
                dicom.PatientName).strip() + '","' + dicom.PatientID + '","' + dicom.InstitutionName + '","' + dicom.InstitutionAddress + '")'

            cursor.execute(sql)
            db.commit()
            return str(dicom.PatientName).strip()
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        cursor.close()
        db.close()


# 获取患者信息
def select_dicom(dicom_id):
    sql = 'SELECT 	b.hospital_name,a.patient_id,a.patient_name,a.institution_name,a.institution_address FROM dicom_information a ' \
          'LEFT JOIN dicom_hospital b ON a.hospital_id=b.id WHERE a.id = "' + dicom_id + '"'
    try:
        db = pymysql.connect(host='192.168.1.20',
                             user='root',
                             password='MneXQvu_NZaJhg8j',
                             database='braineuroo-dcm')
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchone()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    # mysql = Mysql()
    a = select_hospital()

    from pydicom import dataset

    b = select_dicom('3fda34f7e8da3a5f95b3f439c79614ef')
    print(a)
    print('----')
    print(b)
