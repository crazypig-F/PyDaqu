import pandas as pd


class StackData:
    """堆积图的数据预处理
    输入表格格式：
        index是微生物物种名称，columns为样品名称
    处理后的数据格式：
        N行三列的表格
        第一行为列名：Samples Strains Values，分别表示样品名称，物种名称，丰度值
    """

    def __init__(self, sheet):
        self.sheet = sheet

    def abundance(self, rel=True):
        """
        :param rel: 是否为相对丰度
        :return: 符合堆叠图数据格式的数据表
        """
        index_list = []
        column_list = []
        values = []
        for idx in self.sheet.index:
            for col in self.sheet.columns:
                index_list.append(idx)
                column_list.append(col)
                if rel:
                    values.append(self.sheet.loc[idx, col] / sum(self.sheet.loc[idx, :]) * 100)
                else:
                    values.append(self.sheet.loc[idx, col])
        sheet = pd.DataFrame({"Index": index_list, "Column": column_list, "Values": values, })
        return sheet
