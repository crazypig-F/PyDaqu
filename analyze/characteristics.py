class NumCharacteristics:
    """计算均值和标准差
       输入表格格式：
            第一行是各个属性名称
            第一列是样品名称，平行样的样品名称最后一个字符用于区分平行样
    """
    def __init__(self, sheet):
        self.sheet = sheet

    def get_mean(self, prefix=-1, save_type="float"):
        """对有平行样的数据取平均值，样品的命名必须前n个字符相同，最后一个字符用于区分平行样
            例如SampleA，SampleB，SampleC
            prefix: 样品前缀相同的长度
            save_type: 保存的数据类型
        :return: 取平均值之后的数据组成的数据表
        """
        sheet_mean = self.sheet.copy()
        sheet_mean["name"] = [i[:prefix] for i in sheet_mean.index]
        return sheet_mean.groupby(by="name").mean().astype(save_type)

    def get_std(self, prefix=-1, save_type="float"):
        """
        :return: 标准差
        """
        sheet_std = self.sheet.copy()
        sheet_std["name"] = [i[:prefix] for i in sheet_std.index]
        return sheet_std.groupby(by="name").std().astype(save_type)
