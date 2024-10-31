import json
import os
import re
from collections import Counter

import pandas as pd
import requests

import config


###################################################################
# 00250 M   Alanine, aspartate and glutamate metabolism
# 00260 M N Glycine, serine and threonine metabolism
# 00270 M N Cysteine and methionine metabolism
# 00280 M N Valine, leucine and isoleucine degradation
# 00290 M   Valine, leucine and isoleucine biosynthesis
# 00300 M   Lysine biosynthesis
# 00310 M N Lysine degradation
# 00220 M N Arginine biosynthesis
# 00330 M N Arginine and proline metabolism
# 00340 M N Histidine metabolism
# 00350 M N Tyrosine metabolism
# 00360 M   Phenylalanine metabolism
# 00380 M N Tryptophan metabolism
# 00400 M N Phenylalanine, tyrosine and tryptophan biosynthesis
####################################################################


def get_ec():
    map_list = [
        "00250", "00260", "00270", "00280", "00290",
        "00300", "00310", "00220", "00330", "00340",
        "00350", "00360", "00380", "00400"
    ]

    for map_num in map_list:
        print(map_num)
        results_ko = []
        results_name = []
        results_name_zh = []
        results_ec = []
        r = requests.get(f"https://www.kegg.jp/entry/ko{map_num}")
        results_row = re.findall(r'>K(.*?)</tr></table>', r.text)
        for row in results_row:
            ko = re.findall(r'(.*?)</a>&nbsp;&nbsp;', row)
            name = re.findall(r'</span></td><td>(.*?)(?:\[EC|</td>)', row)
            ec = re.findall(r'<a href="/entry/.*?">(.*?)</a>', row)
            results_ko.append("K" + ko[0])
            results_name.append("".join(name))
            name_zh = translate("".join(name))
            print(name_zh)
            results_name_zh.append(name_zh)
            results_ec.append(";".join(["EC:" + i for i in ec]))
        df = pd.DataFrame({"ko": results_ko, "name": results_name, "ec": results_ec, "name_zh": results_name_zh})
        df.to_csv(config.basedir + f"data/result/function/ko{map_num}.csv", index=False)


def get_module_name():
    return {
        "M00020": "丝氨酸生物合成，甘油酸-3P =>丝氨酸",
        "M00018": "苏氨酸生物合成，天冬氨酸 => 高丝氨酸 => 苏氨酸",
        "M00021": "半胱氨酸生物合成，丝氨酸 => 半胱氨酸",
        "M00338": "半胱氨酸生物合成，同型半胱氨酸+丝氨酸=>半胱氨酸",
        "M00609": "半胱氨酸生物合成，蛋氨酸 => 半胱氨酸",
        "M00017": "蛋氨酸生物合成，天冬氨酸=>高丝氨酸=>蛋氨酸",
        "M00019": "缬氨酸/异亮氨酸生物合成，丙酮酸 => 缬氨酸 / 2-氧代丁酸酯 => 异亮氨酸",
        "M00535": "异亮氨酸生物合成，丙酮酸 => 2-氧代丁酸酯",
        "M00570": "异亮氨酸生物合成，苏氨酸 => 2-氧代丁酸酯 => 异亮氨酸",
        "M00432": "亮氨酸生物合成，2-氧代异戊酸酯 => 2-氧代异己酸酯",
        "M00016": "赖氨酸生物合成，琥珀酰-DAP途径，天冬氨酸=>赖氨酸",
        "M00525": "赖氨酸生物合成，乙酰基-DAP途径，天冬氨酸=>赖氨酸",
        "M00526": "赖氨酸生物合成，DAP脱氢酶途径，天冬氨酸=>赖氨酸",
        "M00527": "赖氨酸生物合成，DAP转氨酶途径，天冬氨酸=>赖氨酸",
        "M00030": "赖氨酸生物合成，AAA途径，2-氧代戊二酸=>2-氨基己二酸=>赖氨酸",
        "M00433": "赖氨酸生物合成，2-氧代戊二酸 => 2-氧代己二酸",
        "M00031": "赖氨酸生物合成，由 LysW 介导，2-氨基己二酸 => 赖氨酸",
        "M00844": "精氨酸生物合成，鸟氨酸=>精氨酸",
        "M00845": "精氨酸生物合成，谷氨酸=>乙酰基母酸=>精氨酸",
        "M00015": "脯氨酸生物合成，谷氨酸=>脯氨酸",
        "M00026": "组氨酸生物合成，PRPP =>组氨酸",
        "M00023": "色氨酸生物合成，绒毛膜 => 色氨酸",
        "M00024": "苯丙氨酸生物合成，绒毛膜=>苯丙酮酸=>苯丙氨酸",
        "M00910": "苯丙氨酸生物合成，绒毛膜 => 芳烃酸酯 => 苯丙氨酸",
        "M00025": "酪氨酸生物合成，绒毛膜 => HPP => 酪氨酸",
        "M00040": "酪氨酸生物合成，绒毛膜 => arogenate =>酪氨酸"
    }


def get_module_ec():
    all_ec = []
    for key in get_amino_acid_ec_map().keys():
        # print(key, set(amino_ec[key]))
        all_ec += ["EC:" + i for i in get_amino_acid_ec_map()[key]]
    # print(Counter(all_ec))
    return all_ec


def get_amino_acid_ec_map():
    return {
        "serine": ['1.1.1.95', '2.6.1.52', '3.1.3.3'],
        "threonine": ['2.7.2.4', '1.2.1.11', '1.1.1.3', '2.7.1.39', '4.2.3.1'],
        "cysteine": ['2.5.1.47', '2.5.1.134', '4.4.1.1', '2.5.1.6', '4.2.1.22', '2.3.1.30', '3.2.2.9', '4.4.1.21'],
        "methionine": ['2.1.1.13', '2.3.1.46', '1.1.1.3', '1.2.1.11', '4.4.1.13', '2.7.2.4', '2.5.1.48'],
        "valine": ['2.2.1.6', '1.1.1.86', '4.2.1.9', '2.6.1.42'],
        "isoleucine": ['4.2.1.9', '1.1.1.85', '2.3.3.21', '2.2.1.6', '1.1.1.86', '2.6.1.42', '4.2.1.33', '4.3.1.19'],
        "leucine": ['2.3.3.13', '4.2.1.33', '1.1.1.85'],
        "lysine": ['3.5.1.47', '5.1.1.7', '1.1.1.87', '3.5.1.18', '2.7.2.4', '2.7.2.17', '2.6.1.39', '2.6.1.17',
                   '4.1.1.20', '1.17.1.8', '1.4.1.16', '1.5.1.10', '2.3.1.117', '4.3.3.7', '4.2.1.36', '2.6.1.118',
                   '1.5.1.7', '3.5.1.130', '2.3.3.14', '2.3.1.89', '1.2.1.11', '6.3.2.43', '1.2.1.95', '1.2.1.103',
                   '2.6.1.83'],
        "arginine": ['1.2.1.38', '2.1.3.3', '2.3.1.1', '3.5.1.16', '6.3.4.5', '2.6.1.11', '4.3.2.1', '2.1.3.9'],
        "proline": ['1.5.1.2', '1.2.1.41', '2.7.2.11'],
        "histidine": ['4.3.2.10', '2.6.1.9', '3.1.3.15', '5.3.1.16', '1.1.1.23', '4.2.1.19', '2.4.2.17', '3.6.1.31',
                      '3.5.4.19'],
        "tryptophan": ['4.1.3.27', '2.4.2.18', '5.3.1.24', '4.1.1.48', '4.2.1.20'],
        "phenylalanine": ['4.2.1.91', '5.4.99.5', '2.6.1.57', '2.6.1.78', '4.2.1.51'],
        "tyrosine": ['1.3.1.13', '5.4.99.5', '1.3.1.43', '2.6.1.57', '1.3.1.78', '2.6.1.78', '1.3.1.12'],
        "glycine": ['2.1.2.1', '4.1.2.48', '4.1.2.5', '2.6.1.44', '1.8.1.4', '2.1.2.10'],
        "alanine": ['2.6.1.2', '2.6.1.42', '2.8.1.7', '2.6.1.66'],
        "asparagine": ['6.1.1.23', '3.5.1.38', '3.5.1.2', '6.3.5.4', '6.3.1.1'],
        "glutamine": ['6.3.1.2'],
        "aspartate": ['2.6.1.1'],
        "glutamate": ['3.5,1.2', '3.5.1.38', '1.4.7.1', '1.2.1.88', '3.5.3.1', '1.4.1.14', '1.4.1.4', '1.4.1.3',
                      '2.6.1.13']
    }


def translate(word):
    cookies = {
        '_EDGE_V': '1',
        'MUID': '0FB1AD6542E860921A1EB9D6438E6173',
        'MUIDB': '0FB1AD6542E860921A1EB9D6438E6173',
        'SRCHD': 'AF=NOFORM',
        'SRCHUID': 'V=2&GUID=3825875306084AB994E8D684EC773FD2&dmnchg=1',
        'SnrOvr': 'X=rebateson',
        'MMCASM': 'ID=C3B210E1ECF14BCC9494619C274D766E',
        'EDGSRCHHPGUSR': 'CIBV=1.1792.0',
        'ANON': 'A=68A803DCF6AFD2B07CF950D8FFFFFFFF&E=1e07&W=1',
        'PPLState': '1',
        'KievRPSSecAuth': 'FABKBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACO+Z+HaAsIgfCAQieGz1HDO6Tg2RuW68sMl5twalnyUbZdq9MF0pGwyxKbr4k18d8Ql8hElo2Vopzraf4qLZIHupzUDGN96b4liEVU9O+Zs5WIxgm8RhD7gekfrouJZKR6QuFBBP69nhq97y4Qmfd81kZ0q/Su2smozfDEWiDemLI+nTEbfUGg2Q9eoXCuq7hGD1qyD9JUSRhJspMiZMxy3HeLFqO9G1XXMBfQJxvI2O4kyEyHcRU+i4vF9S6sCAMg6/57X7nOyArFlfh1+U5G7+P8PJZBCwb9k1SWf6Nm3/NboMffYOoqAFhEIhfMhY9jtkxx3nJmMzZ2tr83kdq1fwqS1KBR4C2XHVaqTB+zKDTC5WbmX7DhoF/hcAtCXL32sSSydM7Z8BkvQft8OKWLdOj+74ncPr2noN26frpryOoKDKjZ3MKaOydWZdBPVLOZwTVD4hl41kXqGrQCqDGjJLyZDh5XLwGT492ybN7CW+ooUhD+w58XbeVzCOdZxjpbG71PB7B50S2OEb2FIvhb+XjwwXOrFej47lduDPQ9pnDrEZd6GLYEjyNPYp0FEL7K7ne6zPkT/rNUpAiPDyCmS3AGJx4ILmp9bLtXo5k+b3QcXv4vuevvyVohQJZenjOVcHD+2gBJ/Vzr51MDc6cpBD5+TqXRrB+g58NuKxrJ/k+n5fLf4OdyvWkXP7qKDMuzaNsGdgaKjhVeeOSHEUz3XyaM/AgAPFSo3DJXsd8FKgTlkZotlekqju9SZQqg5G22O4k18IplMDBatx3mKaDbYTzWk1RIrNRnlr86R0FuUSxH+tp6jaor+wu2isVDqBsSuAJNwsDPUJDLauIeLDDc9kqPBnHOZvGExpN0x3aZLbbUQRrOCHmkx11mQMp7M87CmfCER9v1We0N8bqEvtYx8rpyNgkU3tO/PHQs6yIxKrrSKEGozORrBEBu3XD92+fPV+7HDiplyZDqlqaE9ek+HVTMe428j9Sz7o0Xr/fyaet7qY5RZfpZARY84G58snKC8EFTC58cF6FxBGKDrqTghvNVOfCZZ1Sq5ZH4dekW686IvcScbkft5u6MR70ZsuIiZlTsqtsD1V1XFKk35KviBQ+7S+NRG2GMsSBXA7wjvckopgqNz0/otRFNJIEECuvjYGjMz2wl3nDUxbBUM86jpTlU6rhihSNqN/Sy2QcRBidT9Ylxfv3SJ0Xj73pvaHg84DGfXyiwUcuH0ekAG6m3/4dw9JNakeT+8+K+fIIUOJKkCfZKdCCxFD+PmgTA1zU0nBA2TdGyyeBZRBf8mPAIflM7h1EhDpPYIEAl31RGfRsUNGj2zHIiO5LLZkuj3PtYwJPF9dZ8ndcK2SZHIc/J0sVFyNBTuM9mWMVxNSu8ODbaIUADH91q/4dLZvk8KbiVqHiZB6+9Qn',
        '_U': '1CGTPmvz3Oix5c3shts3rHajAvb7FnYaWqol_VDDuwskPkFQYd77nnvFIQ4wQL4IraHGUJoLW6ApEU6-2E3EUNUr9Wq0mOo4OzHe7BDobM1VuLOlbrUMkrf1GauMsxBQJNQeXVwdPO1ElyC4RWy7p3-tVxzbgiomvWL1ICX7t1EJXC83C5uvJ1NAlr2JKNKJ8jaa4Ccvf6ptV-b19xg9R7Q',
        'WLID': 'HoSc1ZRMRonPaFlNoJY2fofheuqFLqfDWfnWtcDF/9I/S2Y0O/jkBbQbPEZbMvENIa8mXjZQPyCSwulHUAkG6s/rUnsLKzDjhOzOICPtaJg=',
        'ABDEF': 'V=13&ABDV=13&MRNB=1721801230070&MRB=0',
        'WLS': 'C=0b538378a257a83f&N=',
        'SRCHUSR': 'DOB=20240705&T=1721809737000&POEX=W',
        '_Rwho': 'u=d&ts=2024-07-24',
        'SRCHS': 'PC=U531',
        'USRLOC': 'HS=1&ELOC=LAT=39.090354919433594|LON=117.69744110107422|N=%E6%BB%A8%E6%B5%B7%E6%96%B0%E5%8C%BA%EF%BC%8C%E5%A4%A9%E6%B4%A5%E5%B8%82|ELT=2|&CLOC=LAT=39.09035407976066|LON=117.69744238523806|A=733.4464586120832|TS=240724082539|SRC=W&BID=MjQwNzI0MTYyNTM3X2M3MDgyNTUwOTZhZWRkMGY2NGEwOGI0NDhlNWMyMzk3ZTAyNTZlNWY1NTM4NjQzYzY0MTY0NzcwMjkwODMwNjE=',
        '_tarLang': 'default=zh-Hans',
        '_TTSS_IN': 'hist=WyJlbiIsImF1dG8tZGV0ZWN0Il0=&isADRU=0',
        '_TTSS_OUT': 'hist=WyJ6aC1IYW5zIl0=',
        '_C_ETH': '1',
        'GC': '7qtkUvpmuS1tmutLgAIfpaWACiuKFBz8s6DBUx7Zb7Leg0yVXRXZkj81yE7sM3ppXVqv0anM60sQz1jLDPOaRQ',
        '_RwBf': 'r=1&mta=0&rc=2843&rb=2843&gb=0&rg=0&pc=2840&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=3&l=2024-07-24T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=2022-12-07T22:07:52.3414197-08:00&rwflt=0001-01-01T16:00:00.0000000-08:00&o=0&p=BINGTRIAL5TO250P201808&c=MY00IA&t=1382&s=2022-12-08T06:06:20.6394084+00:00&ts=2024-07-24T08:48:09.4041140+00:00&rwred=0&wls=0&wlb=0&wle=1&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&e=JsbxwbPVVSMgHukjNEt62WM7jnx-MRu9wDgmCBQeEJZqYV3Bx908wT7s4dGwpBvnLdnndb4oWB2PM-yZ-zhnYA&A=',
        '_SS': 'SID=21930B03E5316BDF23A31FC5E41F6A81&PC=U531&R=2843&RB=2843&GB=0&RG=0&RP=2840',
        'ipv6': 'hit=1721814493045',
        '_EDGE_S': 'ui=zh-cn&SID=21930B03E5316BDF23A31FC5E41F6A81',
        'SNRHOP': 'I=&TS=',
        'SRCHHPGUSR': 'SRCHLANG=zh-Hans&PV=15.0.0&BZA=0&BRW=W&BRH=M&CW=1415&CH=759&SCW=1401&SCH=3613&DPR=1.8&UTC=480&DM=1&EXLTT=31&HV=1721810895&PRVCW=1415&PRVCH=759&PR=1&WTS=63857157837',
        'btstkn': 'JL4uTuoqc1563jbGIsHqEVU15G056i9v2dgtEBe2WEnsrolf8lOu96L3c5Q0nEzZWR35Qdlp4ZjYarFW6NLMXOFMS8Ovvy286yfSecGw3bs%253D',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': '_EDGE_V=1; MUID=0FB1AD6542E860921A1EB9D6438E6173; MUIDB=0FB1AD6542E860921A1EB9D6438E6173; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=3825875306084AB994E8D684EC773FD2&dmnchg=1; SnrOvr=X=rebateson; MMCASM=ID=C3B210E1ECF14BCC9494619C274D766E; EDGSRCHHPGUSR=CIBV=1.1792.0; ANON=A=68A803DCF6AFD2B07CF950D8FFFFFFFF&E=1e07&W=1; PPLState=1; KievRPSSecAuth=FABKBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACO+Z+HaAsIgfCAQieGz1HDO6Tg2RuW68sMl5twalnyUbZdq9MF0pGwyxKbr4k18d8Ql8hElo2Vopzraf4qLZIHupzUDGN96b4liEVU9O+Zs5WIxgm8RhD7gekfrouJZKR6QuFBBP69nhq97y4Qmfd81kZ0q/Su2smozfDEWiDemLI+nTEbfUGg2Q9eoXCuq7hGD1qyD9JUSRhJspMiZMxy3HeLFqO9G1XXMBfQJxvI2O4kyEyHcRU+i4vF9S6sCAMg6/57X7nOyArFlfh1+U5G7+P8PJZBCwb9k1SWf6Nm3/NboMffYOoqAFhEIhfMhY9jtkxx3nJmMzZ2tr83kdq1fwqS1KBR4C2XHVaqTB+zKDTC5WbmX7DhoF/hcAtCXL32sSSydM7Z8BkvQft8OKWLdOj+74ncPr2noN26frpryOoKDKjZ3MKaOydWZdBPVLOZwTVD4hl41kXqGrQCqDGjJLyZDh5XLwGT492ybN7CW+ooUhD+w58XbeVzCOdZxjpbG71PB7B50S2OEb2FIvhb+XjwwXOrFej47lduDPQ9pnDrEZd6GLYEjyNPYp0FEL7K7ne6zPkT/rNUpAiPDyCmS3AGJx4ILmp9bLtXo5k+b3QcXv4vuevvyVohQJZenjOVcHD+2gBJ/Vzr51MDc6cpBD5+TqXRrB+g58NuKxrJ/k+n5fLf4OdyvWkXP7qKDMuzaNsGdgaKjhVeeOSHEUz3XyaM/AgAPFSo3DJXsd8FKgTlkZotlekqju9SZQqg5G22O4k18IplMDBatx3mKaDbYTzWk1RIrNRnlr86R0FuUSxH+tp6jaor+wu2isVDqBsSuAJNwsDPUJDLauIeLDDc9kqPBnHOZvGExpN0x3aZLbbUQRrOCHmkx11mQMp7M87CmfCER9v1We0N8bqEvtYx8rpyNgkU3tO/PHQs6yIxKrrSKEGozORrBEBu3XD92+fPV+7HDiplyZDqlqaE9ek+HVTMe428j9Sz7o0Xr/fyaet7qY5RZfpZARY84G58snKC8EFTC58cF6FxBGKDrqTghvNVOfCZZ1Sq5ZH4dekW686IvcScbkft5u6MR70ZsuIiZlTsqtsD1V1XFKk35KviBQ+7S+NRG2GMsSBXA7wjvckopgqNz0/otRFNJIEECuvjYGjMz2wl3nDUxbBUM86jpTlU6rhihSNqN/Sy2QcRBidT9Ylxfv3SJ0Xj73pvaHg84DGfXyiwUcuH0ekAG6m3/4dw9JNakeT+8+K+fIIUOJKkCfZKdCCxFD+PmgTA1zU0nBA2TdGyyeBZRBf8mPAIflM7h1EhDpPYIEAl31RGfRsUNGj2zHIiO5LLZkuj3PtYwJPF9dZ8ndcK2SZHIc/J0sVFyNBTuM9mWMVxNSu8ODbaIUADH91q/4dLZvk8KbiVqHiZB6+9Qn; _U=1CGTPmvz3Oix5c3shts3rHajAvb7FnYaWqol_VDDuwskPkFQYd77nnvFIQ4wQL4IraHGUJoLW6ApEU6-2E3EUNUr9Wq0mOo4OzHe7BDobM1VuLOlbrUMkrf1GauMsxBQJNQeXVwdPO1ElyC4RWy7p3-tVxzbgiomvWL1ICX7t1EJXC83C5uvJ1NAlr2JKNKJ8jaa4Ccvf6ptV-b19xg9R7Q; WLID=HoSc1ZRMRonPaFlNoJY2fofheuqFLqfDWfnWtcDF/9I/S2Y0O/jkBbQbPEZbMvENIa8mXjZQPyCSwulHUAkG6s/rUnsLKzDjhOzOICPtaJg=; ABDEF=V=13&ABDV=13&MRNB=1721801230070&MRB=0; WLS=C=0b538378a257a83f&N=; SRCHUSR=DOB=20240705&T=1721809737000&POEX=W; _Rwho=u=d&ts=2024-07-24; SRCHS=PC=U531; USRLOC=HS=1&ELOC=LAT=39.090354919433594|LON=117.69744110107422|N=%E6%BB%A8%E6%B5%B7%E6%96%B0%E5%8C%BA%EF%BC%8C%E5%A4%A9%E6%B4%A5%E5%B8%82|ELT=2|&CLOC=LAT=39.09035407976066|LON=117.69744238523806|A=733.4464586120832|TS=240724082539|SRC=W&BID=MjQwNzI0MTYyNTM3X2M3MDgyNTUwOTZhZWRkMGY2NGEwOGI0NDhlNWMyMzk3ZTAyNTZlNWY1NTM4NjQzYzY0MTY0NzcwMjkwODMwNjE=; _tarLang=default=zh-Hans; _TTSS_IN=hist=WyJlbiIsImF1dG8tZGV0ZWN0Il0=&isADRU=0; _TTSS_OUT=hist=WyJ6aC1IYW5zIl0=; _C_ETH=1; GC=7qtkUvpmuS1tmutLgAIfpaWACiuKFBz8s6DBUx7Zb7Leg0yVXRXZkj81yE7sM3ppXVqv0anM60sQz1jLDPOaRQ; _RwBf=r=1&mta=0&rc=2843&rb=2843&gb=0&rg=0&pc=2840&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=3&l=2024-07-24T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=2022-12-07T22:07:52.3414197-08:00&rwflt=0001-01-01T16:00:00.0000000-08:00&o=0&p=BINGTRIAL5TO250P201808&c=MY00IA&t=1382&s=2022-12-08T06:06:20.6394084+00:00&ts=2024-07-24T08:48:09.4041140+00:00&rwred=0&wls=0&wlb=0&wle=1&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&e=JsbxwbPVVSMgHukjNEt62WM7jnx-MRu9wDgmCBQeEJZqYV3Bx908wT7s4dGwpBvnLdnndb4oWB2PM-yZ-zhnYA&A=; _SS=SID=21930B03E5316BDF23A31FC5E41F6A81&PC=U531&R=2843&RB=2843&GB=0&RG=0&RP=2840; ipv6=hit=1721814493045; _EDGE_S=ui=zh-cn&SID=21930B03E5316BDF23A31FC5E41F6A81; SNRHOP=I=&TS=; SRCHHPGUSR=SRCHLANG=zh-Hans&PV=15.0.0&BZA=0&BRW=W&BRH=M&CW=1415&CH=759&SCW=1401&SCH=3613&DPR=1.8&UTC=480&DM=1&EXLTT=31&HV=1721810895&PRVCW=1415&PRVCH=759&PR=1&WTS=63857157837; btstkn=JL4uTuoqc1563jbGIsHqEVU15G056i9v2dgtEBe2WEnsrolf8lOu96L3c5Q0nEzZWR35Qdlp4ZjYarFW6NLMXOFMS8Ovvy286yfSecGw3bs%253D',
        'origin': 'https://cn.bing.com',
        'priority': 'u=1, i',
        'referer': 'https://cn.bing.com/translator/?h_text=msn_ctxt&setlang=zh-cn',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"126.0.2592.113"',
        'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.183", "Microsoft Edge";v="126.0.2592.113"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-ms-gec': 'A3288E6BB0CEDBB7B8F41DFAC9392CAA9C8D570F7B01EEDD9FEAF1C8A85329C5',
        'sec-ms-gec-version': '1-126.0.2592.113',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'x-client-data': 'eyIxIjoiNSIsIjEwIjoiXCJNaFNQcWpwMlBSU1l2QTNpbGdGUE5PLzlENWtqK0ZPWXIrdEJhUXJaakNvPVwiIiwiMiI6IjEiLCIzIjoiMCIsIjQiOiIyOTkzMDQyOTcxMzg4MTY0OTA4IiwiNSI6IlwibTlLQ3JXZnZXR2ZyT3Z0UkloamdmNkZ5eTBtcmgvZk45RlBpWEZ1ZmVnTT1cIiIsIjYiOiJzdGFibGUiLCI3IjoiMTQ2ODg3ODgxNTIzNCIsIjkiOiJkZXNrdG9wIn0=',
        'x-edge-shopping-flag': '1',
    }

    data = f'&fromLang=en&to=zh-Hans&token=bt3DpANsSrvCF09FMF4ueV_onxtU_zdM&key=1721811149704&text={word}&tryFetchingGenderDebiasedTranslations=true'

    response = requests.post(
        'https://cn.bing.com/ttranslatev3?isVertical=1&&IG=7B7CC8B1D3C942AD8B6A0806CEC7A9E6&IID=translator.5025',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    return json.loads(response.text)[0]['translations'][0]['text']


if __name__ == '__main__':
    get_ec()
