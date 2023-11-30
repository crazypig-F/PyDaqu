import numpy as np
import pandas as pd
import seaborn
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
# rcParams['font.sans-serif'] = 'Arial'
plt.rcParams["font.sans-serif"] = ["SimSun"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题


def plot_cm_process(name, y_test, y_p):
    cm = confusion_matrix(y_test, y_p)
    cm = pd.DataFrame(cm, index=["传统曲", "机械曲"], columns=["传统曲", "机械曲"])
    seaborn.heatmap(cm, cmap='viridis', annot=True)
    plt.tick_params(axis='both', labelsize=10)
    plt.xlabel("Predict Label", fontsize=12)
    plt.ylabel("True Label", fontsize=12)
    # plt.show()
    plt.savefig(f'./pdf/ml/process/cm/{name}.pdf')
    plt.close()


def plot_feature(name, model, feat_labels):
    importance = model.feature_importances_
    indices = np.argsort(importance)[::-1]
    index = []
    values = []
    for i in range(len(feat_labels)):
        index.append(feat_labels[indices[i]])
        values.append(importance[indices[i]])
        print("%2d) %-*s %f" % (i + 1, 30, feat_labels[indices[i]], importance[indices[i]]))

    plt.figure(figsize=(12, 5))
    seaborn.barplot(x=values, y=index, errorbar=None, color='#3A923A', orient='h')
    plt.tick_params(axis='both', labelsize=10)
    plt.xlabel("Feature importance", fontsize=12)
    # 获取当前坐标轴对象
    # ax = plt.gca()
    # 设置 y 轴刻度标签的旋转角度为45度
    # ax.set_yticks(ax.get_yticks())
    # ax.set_yticklabels(ax.get_yticklabels(), rotation=30, ha='right')
    # plt.show()
    plt.savefig(f'./pdf/ml/process/feature/{name}.pdf')
    plt.close()
