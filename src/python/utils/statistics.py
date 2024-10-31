import pandas as pd
import config


def get_mean_std(df, prefix=-1, save_type="float"):
    """对有平行样的数据取平均值，样品的命名必须前n个字符相同，最后一个字符用于区分平行样
        例如SampleA，SampleB，SampleC
        prefix: 样品前缀相同的长度
        save_type: 保存的数据类型
    :return: 取平均值之后的数据组成的数据表
    """
    df_copy = df.copy()
    df_copy["name"] = [i[:prefix] for i in df.index]
    df_mean = df_copy.groupby(by="name").mean().astype(save_type)
    df_std = df_copy.groupby(by="name").std().astype(save_type)
    return df_mean, df_std


def col(df, prefix, save_type):
    return get_mean_std(df.transpose(), prefix, save_type)


def raw(df, prefix, save_type):
    return get_mean_std(df, prefix, save_type)


def order(df):
    df_RC = df.loc[df.index.str.contains("RC")]
    df_YF = df.loc[df.index.str.contains("YF")]
    df_EF = df.loc[df.index.str.contains("EF")]
    df_CC = df.loc[df.index.str.contains("CC")]
    return pd.concat([df_RC, df_YF, df_EF, df_CC])


def micro_asv_mean_std():
    df_b = pd.read_csv(config.basedir + '/data/raw/Daqu bacteria asv.csv', index_col=0)
    # 去除物种分类那一列
    df_b = df_b.iloc[:, :-1]
    df_f = pd.read_csv(config.basedir + '/data/raw/Daqu fungi asv.csv', index_col=0)
    # 去除物种分类那一列
    df_f = df_f.iloc[:, :-1]
    df_b_mean, df_b_std = col(df_b, -1, 'int')
    df_f_mean, df_f_std = col(df_f, -1, 'int')
    order(df_b_mean).to_csv(config.basedir + '/data/result/micro/mean/bacteria asv.csv')
    order(df_b_std).to_csv(config.basedir + '/data/result/micro/std/bacteria asv.csv')
    order(df_f_mean).to_csv(config.basedir + '/data/result/micro/mean/fungi asv.csv')
    order(df_f_std).to_csv(config.basedir + '/data/result/micro/std/fungi asv.csv')


def micro_genus_top_20_mean_std():
    df_b = pd.read_csv(config.basedir + '/data/result/Daqu bacteria genus top20.csv', index_col=0)
    df_f = pd.read_csv(config.basedir + '/data/result/Daqu fungi genus top20.csv', index_col=0)
    df_b_mean, df_b_std = raw(df_b, -1, 'int')
    df_f_mean, df_f_std = raw(df_f, -1, 'int')
    order(df_b_mean).to_csv(config.basedir + '/data/result/micro/mean/bacteria genus top20.csv')
    order(df_b_std).to_csv(config.basedir + '/data/result/micro/std/bacteria genus top20.csv')
    order(df_f_mean).to_csv(config.basedir + '/data/result/micro/mean/fungi genus top20.csv')
    order(df_f_std).to_csv(config.basedir + '/data/result/micro/std/fungi genus top20.csv')


def AAs_mean_std():
    df = pd.read_csv(config.basedir + '/data/raw/AAs.csv', index_col=0)
    df_mean, df_std = raw(df, -1, 'float')
    order(df_mean).to_csv(config.basedir + '/data/result/AAs/AAs mean.csv')
    order(df_std).to_csv(config.basedir + '/data/result/AAs/AAs std.csv')

    df_stage_mean, df_stage_std = raw(df, 2, 'float')
    order(df_stage_mean).to_csv(config.basedir + '/data/result/AAs/AAs stage mean.csv')
    order(df_stage_std).to_csv(config.basedir + '/data/result/AAs/AAs stage std.csv')


def asv_top_30_percent_mean_std():
    asv_b = pd.read_csv(config.basedir + "/data/raw/Daqu bacteria asv.csv", index_col=0)
    asv_f = pd.read_csv(config.basedir + "/data/raw/Daqu fungi asv.csv", index_col=0)
    # 去除物种分类那一列
    asv_b = asv_b.iloc[:, :-1]
    asv_f = asv_f.iloc[:, :-1]
    asv_b.index = ['B_' + i for i in asv_b.index]
    asv_f.index = ['F_' + i for i in asv_f.index]

    asv_b['sum'] = asv_b.sum(axis=1)
    asv_f['sum'] = asv_f.sum(axis=1)
    asv_b.sort_values('sum', ascending=False, inplace=True)
    asv_f.sort_values('sum', ascending=False, inplace=True)
    asv_b = asv_b.iloc[:int(len(asv_b) * 0.3), :-1].T
    asv_f = asv_f.iloc[:int(len(asv_f) * 0.3), :-1].T
    asv = pd.concat([asv_b, asv_f], axis=1)
    df_mean, df_std = raw(asv, -1, 'int')
    order(df_mean).to_csv(config.basedir + '/data/result/micro/mean/asv 30% mean.csv')
    order(df_std).to_csv(config.basedir + '/data/result/micro/std/asv 30% std.csv')


def fermentation_parameters_mean_std():
    df = pd.read_csv(config.basedir + '/data/raw/fermentation parameters.csv', index_col=0)
    df_mean, df_std = raw(df, -1, 'float')
    order(df_mean).to_csv(config.basedir + '/data/result/fermentation parameters/fermentation parameters mean.csv')
    order(df_std).to_csv(config.basedir + '/data/result/fermentation parameters/fermentation parameters std.csv')


def alpha_mean_std():
    df = pd.read_csv(config.basedir + '/data/result/diversity/alpha.csv', index_col=0)
    df_mean, df_std = raw(df, 2, 'float')
    order(df_mean).to_csv(config.basedir + '/data/result/diversity/alpha mean.csv')
    order(df_std).to_csv(config.basedir + '/data/result/diversity/alpha std.csv')


if __name__ == '__main__':
    micro_asv_mean_std()
    micro_genus_top_20_mean_std()
    AAs_mean_std()
    asv_top_30_percent_mean_std()
    fermentation_parameters_mean_std()
    alpha_mean_std()
