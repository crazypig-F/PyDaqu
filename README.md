# PyDaqu
基于python处理大曲发酵过程中的理化、微生物和氨基酸数据。

原始数据包括：理化测定数据（淀粉含量、水分、糖化力、还原糖含量、总酸、总酯），微生物测序数据（细菌和真菌丰度表），21种氨基酸测定数据。

## 样品采集

在大曲发酵入仓、一翻、二翻、出仓四个时间点采集样品。分别在传统车间和机械车间采样，每个车间包含14个曲房，曲房编号为01-14，每个曲房采集一个样品，每个样品平均分为3个平行。另外从空气，母曲，稻草，小麦中采集环境微生物样品，每个样品平均分为3个平行。

样品命名规则如下

发酵时间：入仓（A），一翻（B），二翻（C），出仓（D）

环境：空气（E），母曲（M），稻草（R），小麦（W）

车间：传统车间（Y），机械车间（Z）

曲房：01-14

平行：A-C

例如 AY01A、AY01B、AY01C 表示入仓阶段传统车间01曲房的3个样品，EYA、EYB、EYC 表示传统车间环境中空气的3个样品

## 理化和氨基酸数据

1. 传统和机械理化折线图

2. 氨基酸柱状图

## 微生物群落特征

1. α多样性（Chao1和Shannon）箱线图
2. β多样性（PCoA）
3. 细菌和真菌组成与演替

## 大曲发酵过程核心微生物

1. 相关性网络分析（核心微生物）
2. 不同车间的差异微生物
3. 微生物功能分析

### 理化与微生物的相关性分析

1. mantel test
2. RDA

## 核心微生物和理化构建大曲发酵阶段判别模型

通过判别模型监控大曲发酵进程

## 入仓阶段大曲微生物溯源

FEAST溯源分析

## 微生物与氨基酸的相关性分析

1. mantel test
2. RDA

## 氨基酸含量预测模型

实现发酵过程氨基酸含量的定制化生成

