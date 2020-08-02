
class Village(object):
    '''
    小区
    '''

    def __init__(self):
        # id 唯一标识符
        id = 0
        #小区名字
        name = ''
        #地理位置
        location = ''
        #占地面积
        area_covery = 0
        #开发商
        developer = ''
        #物业公司
        property_company = ''
    pass

class House(object):
    '''
    房产信息
    '''
    def __init__(self):
        #楼栋编号
        building_number = ''
        # 层数
        level = 0
        # 门牌号
        house_number = ''
