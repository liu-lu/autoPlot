
import requests  # pip install requests
import json
import pandas as pd
import pyecharts.options as opts  # pip install pyecharts
from pyecharts.charts import Line


# 请求相应函数
def getTextFromUrl(url):
    headers = {
        "Referer": "https://www.chinamoney.com.cn/chinese/bkfrr/",
        "User-Agent": "Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome / 57.0.2987.133 Safari/537.36"
        }
    response = requests.post(url=url,headers=headers)  # 发送HTTP请求
    response.encoding = "UTF-8"  # 设置页面编码
    return response


# 解析URL返回值，并且转换为Json数据
def parseResText2JsonList(text):
    # 1.在字符串中找到需要去掉的内容，"records"
    startIndex = text.find("records")
    print('截取起始索引：',startIndex)
    # 2.找到最后1个"}]"的位置
    endIndex = text.find("}]")
    print('截取结束索引：',endIndex)
    # 3.通过起始位置和结束位置，截取到"[]"之间的数据
    str = text[startIndex:endIndex+2].replace("records", "")
    # 4.将数据解析成JSON列表
    jsonlist = json.loads(str[2:])
    return jsonlist

# 将获取的数据进行可视化展示
def Repo_line(data_list) -> Line:
        repo_date = data_list.index.tolist()
        y1 = data_list['FDR001']
        y2 = data_list['FDR007']
        y3 = data_list['FDR014']
        y4 = data_list['FR001']
        y5 = data_list['FR007']
        y6 = data_list['FR014']
        line_repo = (
            Line()
                .add_xaxis(xaxis_data=repo_date)
                .add_yaxis(series_name="FDR001", y_axis=y1, is_smooth=True)
                .add_yaxis(series_name="FDR007", y_axis=y2, is_smooth=True)
                .add_yaxis(series_name="FDR014", y_axis=y3, is_smooth=True)
                .add_yaxis(series_name="FR001", y_axis=y4, is_smooth=True)
                .add_yaxis(series_name="FR007", y_axis=y5, is_smooth=True)
                .add_yaxis(series_name="FR014", y_axis=y6, is_smooth=True)
                .set_global_opts(title_opts=opts.TitleOpts(title="回购利率对比趋势图"),
                                 datazoom_opts=opts.DataZoomOpts(range_start=0, range_end=100),
                                 yaxis_opts=opts.AxisOpts(name='回购利率%')))
        line_repo.render('.\htmlDoc\回购利率对比趋势折线图.html')
        return line_repo
    

if __name__ == "__main__":  #主函数入口
    URL = "https://www.chinamoney.com.cn/ags/ms/cm-u-bk-currency/FrrHis?lang=CN&startDate=2022-01-21&endDate=2023-01-20&t=1674466755277"  #要爬取的页面
    res=getTextFromUrl(url=URL)   # 调用主函数
    print('初始响应返回的数据：',res.text)

    #调用函数解析URL返回值
    jsonList = parseResText2JsonList(res.text)
    print("截取所需Json中所有数据：", jsonList)
    print("截取所需Json中字典的个数：", len(jsonList))
    

    #转换为数据框，展示所有行列数据
    Repo_data_first=pd.DataFrame(jsonList)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    # print(Repo_data_first)

    #处理数据：只获取回购利率的日期和数据
    Repo_data=pd.concat([pd.DataFrame([x]) for x in Repo_data_first["frValueMap"]], axis=0).sort_index(axis=1)
    Repo_data=Repo_data.set_index(Repo_data['date']) #将日期列作为索引
    Repo_data=Repo_data.drop(labels='date',axis=1)   #删除日期列
    Repo_data=Repo_data.astype(float)  #将文本格式存储的数据转换为数值
    Repo_data =Repo_data.sort_index(ascending=True) #按索引日期升序排序
    # print(Repo_data)

    #可视化Repo利率图形
    Repo_line(data_list=Repo_data)
    
    #以excel形式存储到本地
    Repo_data.to_excel('.\data\Repo数据.xlsx', index = True)