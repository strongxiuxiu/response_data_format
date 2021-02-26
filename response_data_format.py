"""
    time:20201229
    author : pxq
"""
import datetime

sys_code = {
    # success
    "210011": "数据添加成功",
    "210012": "数据删除成功",
    "210013": "数据修改成功",
    "210014": "获取数据成功",
    # error
    "110011": "数据重复添加",
    "110012": "数据添加失败",
    "110013": "数据删除失败",
    "110014": "数据修改失败",
    "110015": "数据查询失败",

    "410011": "请求方式错误",

    "510011": "服务内部错误",

    "610011": "数据完整性错误",

    "710011": "查询关系不存在",
    "710012": "执行出错",
}




class MyError(Exception):  # 自定义的报错信息展示 MyError
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class DataFormatBase:
    WebStatus_code = 1  # code类型为1时，操作成功

    def __init__(self, code=None, chMessage=None, enMessage=None, data=None):
        self._result = {}
        self._enMessage = enMessage  # 英文注释
        self._chMessage = chMessage  # 中文注释
        self._data = data  # body内容
        self._code = code  # 返回状态
        self.time = self.gettime()

    def __repr__(self):
        return '<%(cls)s chMessage=%(chMessage)s%(data)s code=%(code)s>' % {
            'cls': self.__class__.__name__,
            'chMessage': self._chMessage,
            'data': self._data,
            'code': self.WebStatus_code}

    @property
    def chMessage(self):
        if self._chMessage is not None:
            return self._chMessage
        return " 未设置返回信息 <<< No Settings information"

    @chMessage.setter
    def chMessage(self, value):
        self._chMessage = value

    @property
    def data(self):
        if self._data is not None:
            return self._data
        return []

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def code(self):
        if self._code is not None:
            if isinstance(self._code, int):
                return self._code
            else:
                raise MyError("code格式错误,code必须为int型")
        return 1

    @code.setter
    def code(self, value):
        self._code = value

    def joint(self):
        if self._code is not None:
            self._result["code"] = self.code
        else:
            self._result["code"] = self.WebStatus_code
        self._result["chMessage"] = self.chMessage
        self._result["Message"] = self.chMessage  # 预留的一个字段，需改进！
        self._result["enMessage"] = self._make_enMessage()
        self._result["data"] = self._data
        self._result["createtime"] = self.time
        return self._result

    def _make_enMessage(self):

        #if self._enMessage is not None:
        #    return self._enMessage
        #else:
        """
            这个位置准备使用第三方模块进行中英互换，目前还没有加入该模块
        """
        return self._enMessage is not None

    def gettime(self):
        dt = datetime.datetime.now()
        return dt.strftime('%Y%m%d %H:%M:%S')


class SuccessDataFormat(DataFormatBase):
    WebStatus_code = 1

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data

    def result(self):
        return self.joint()


class ErrorDataFormat(DataFormatBase):
    WebStatus_code = 0

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data

    def result(self):
        return self.joint()


if __name__ == '__main__':
    pass
    # import datetime
    # dt = datetime.datetime.now()
    # print(dt.strftime('%Y%m%d %H:%M:%S.%f'))
    print()
    print(MyError)
    print(ErrorDataFormat(chMessage=sys_code["110011"], code=110011).result())
    print(SuccessDataFormat(data="ddd", code=111).result())
    print(ErrorDataFormat(data="hhh", enMessage="wwww", chMessage="你好").result())
