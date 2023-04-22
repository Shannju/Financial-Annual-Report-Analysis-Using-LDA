import os
import re
from pdfminer.converter import LTChar, TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from io import StringIO
from io import open

import os
# 获取当前脚本的运行路径
current_path = os.getcwd()

#读取pdf文件文本内容
def read(path):
    parser = PDFParser(path)
    doc = PDFDocument(parser, '')
    parser.set_document(doc)
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF聚合器，包含资源管理器与参数分析器
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 循环遍历列表，每次处理一个page的内容
        page0 = ''
        for i, page in enumerate(PDFPage.create_pages(doc)):
            interpreter.process_page(page)
            print("START PAGE %d\n" % i)
            if page is not None:
                interpreter.process_page(page)
            print("END PAGE %d\n" % i)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            print(layout)
            # 这里layout是一个LTPage对象，里面存放着这个 page 解析出的各种对象
            # 包括 LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等
            line0 = ''
            for x in layout:
                if isinstance(x, LTTextBox):
                    line0 = line0 + x.get_text().strip()
            page0 = page0 + line0
        return page0 #返回pdf文件中所有提取到的文本内容

if __name__ == '__main__':
    path = current_path
    pdfList = os.listdir(path)
    #批量读取存储
    pdf_num = 0
    for li in pdfList:
        try:
            pdffile = open(path + '/' + li, "rb")
            content = read(pdffile)
        except:
            continue
        str = re.sub('.pdf', '.txt', li)
        file1 = path+ str
        with open(file1, 'w+', encoding='utf8') as f:
            f.write(content)
        pdf_num = pdf_num + 1
        # handleData(str)
        print("DONE:" + str )
    print('number of done-article:',end = "")
    print(pdf_num)
