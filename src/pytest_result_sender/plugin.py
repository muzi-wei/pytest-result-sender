from datetime import datetime

import pytest

data = {
    "passed": 0,
    "failed": 0,
}


def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    # 用例加载完成之后执行，包含了全部的用例
    data["total"] = len(session.items)
    print("用例的总数：", data["total"])


def pytest_configure():
    # 配置加载完毕之后执行，测试用例执行前执行
    data["start_time"] = datetime.now()
    print(f"{datetime.now()} pytest开始执行")


def pytest_unconfigure():
    # 配置卸载完毕之后执行，测试用例执行后执行
    data["end_time"] = datetime.now()
    print(f"{datetime.now()} pytest结束执行")

    data["duration"] = data["end_time"] - data["start_time"]
    data["pass_ratio"] = f"{data['passed'] / data['total'] * 100:.2f}%"

    # 要插入的测试结果内容
    test_result = f"""
# pytest自动化测试结果
测试时间： {data['end_time']}<br />
用例数量：{data['total']} <br />
执行时长：{data['duration']} <br />
测试通过：<font color='green'> {data['passed']} </font> <br />
测试失败：<font color='red'> {data['failed']} </font> <br />
测试通过率：{data['pass_ratio']} <br />
测试报告地址：http://baidu.com
    """

    # 写入到recipient.md文件中，如果文件不存在则创建
    try:
        with open("test_report\\report.md", "w", encoding="utf-8") as f:
            f.write(test_result)
        print("内容已成功写入 report.md 文件。")
    except Exception as e:
        print(f"写入文件时出现错误: {e}")
