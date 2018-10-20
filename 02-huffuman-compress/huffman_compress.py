#-*- coding:utf-8 -*-
"""
author:huchangchun 20181020
Thanks to zhanggugu ,orgin link:https://www.jianshu.com/p/4cbbfed4160b
"""
import six
import sys

class HuffmanNode(object):
    """
    定义一个HuffmanNode虚类，包含两个虚方法：
    1、获取节点的权重函数
    2、获取此节点是否是叶节点的函数
    """
    def get_weight(self):
        raise NotImplementedError("The Abstract Node Class doesn't define 'get_weight'")
    def is_leaf(self):
        raise NotImplementedError("The Abstract Node Class doesn't define 'isLeaf'")
    
class LeafNode(HuffmanNode):
    """
    树叶节点
    """
    def __init__(self, value=0,freq=0,):
        """
        初始化叶节点：
        @param: value 值
        @param: freq 出现的频率
        """
        super(LeafNode, self).__init__()
        self.value = value
        self.weight = freq
    def is_leaf(self):
        """
        基类的方法，返回True,代表是叶节点
        """
        return True
    def get_weight(self):
        """
        基类的方法，返回对象属性weight
        """
        return self.weight
    def get_value(self):
        """
        获取叶子节点字符的值
        """
        return self.value
class MidNode(HuffmanNode):
    """
    中间节点类
    """
    def __init__(self, 
                 left_child = None, 
                 right_child = None
                 ):
        """
        初始化中间节点
        @param: left_child
        @param: right_child
        @param: weight
        """
        super(MidNode,self).__init__()
        #节点的值
        self.left_child = left_child
        self.right_child = right_child
        self.weight = left_child.get_weight() + right_child.get_weight()
    def is_leaf(self):
        """
        基类的方法，返回False,代表是中间节点
        """
        return False
    def get_weight(self):
        """
        基类的方法，返回对象属性 weight,表示对象的权重
        """
        return self.weight
    def get_left(self):
        """
        取左孩子
        """
        return self.left_child
    def get_right(self):
        """
        取右孩子
        """
        return self.right_child

class HuffmanTree(object):
    """
    构建huffman树的类
    """
    def __init__(self,
                 flag, 
                 value =0,
                 freq =0,
                 left_tree =None,
                 right_tree =None):
        super(HuffmanTree, self).__init__()
        
        if flag == 0:
            self.root = LeafNode(value, freq)
        else:
            self.root = MidNode(left_tree.get_root(),right_tree.get_root())
    def get_root(self):
        """
        获取huffman tree 的根节点
        """
        return self.root
    def get_weight(self):
        """
        获取这棵huffman树根节点的权重
        """
        return self.root.get_weight()
    def traverse_huffman_tree(self,root,code,char_freq_dict):
        """
        利用递归的方法遍历huffman树，并且以此方法得到每个字符对应的huffman编码
        保存在字典char_freq_dict中
        如果是叶子节点则保存字典
        否则遍历左右子树
        """
        if root.is_leaf():
            char_freq_dict[root.get_value()] = code
            #print("it = %c and freq = %d code = %s" %(chr(root.get_value()),root.get_weight(),code))
            return None
        else:
            self.traverse_huffman_tree(root.get_left(), code +'0',
                                       char_freq_dict)
            self.traverse_huffman_tree(root.get_right(), code +'1',
                                       char_freq_dict)

def buildHuffmanTree(list_huffmanTrees):
    """
    构造huffmanTree
    """
    while len(list_huffmanTrees)>1:
        #按照weight从小到大排序
        list_huffmanTrees.sort(key=lambda x:x.get_weight())
        #取前两个权重全最小的
        lessOne = list_huffmanTrees[0]
        lessSec = list_huffmanTrees[1]
        list_huffmanTrees = list_huffmanTrees[2:]
        #构造一个新的树
        new_huffmanTree = HuffmanTree(flag = 1, left_tree=lessOne,right_tree=lessSec)
        #放入数组中
        list_huffmanTrees.append(new_huffmanTree)
    
    #最后返回剩下的那棵树，就是构造的Huffman编码树
    return list_huffmanTrees[0]

"""
文件压缩思路：
1、对需要被压缩的文件以二进制的方式读，然后以byte为单位读取里面的值，然后将其装换
为int值(4个字节)，一共有2^8共[0-255]256个值，遍历文件的所有byte,统计出现每个值
的次数，作为我们后面叶节点里面的weight(权重)
2、使用[0-255]每个值及其对应的权重，构造对应的huffman编码树，然后分配[0-255]中每
一个值对应的Huffman编码
3、在压缩文件的开始处，将[0-255]及其对应的权重以二进制的方式保存到压缩文件中，目的是
为了方便解压时根据原文件的[0-255]出现的频率取构造相应的Huffman树，然后对压缩文件
进行解压缩的操作
4、遍历文件的每一个byte,然后以步骤2中生成的Huffman编码，将该字节转换为Huffman编码
对应的01组合
5、将步骤4中生成的01组合串，每8位为一个单位，将其转换为相应的byte,然后以二进制的方式
写入到压缩文件当中，这样压缩就完成了

"""
def compress(inputFileName,outputFileName):
    """
    压缩文件：
    @param: inputfilename被压缩的文件的路径名
    @param: outputfilename压缩后的文件的路径名
    """
    #1.以二进制的方式读取文件
    f = open(inputFileName,'rb')
    filedata = f.read()
    #获取文件的字节总数
    filesize = f.tell()
    
    #2.统计byte的取值[0-255] 的每个值出现的频率
    #保存在字典char_freq_dict中
    char_freq_dict = {}
    for i in range(filesize):
        x = filedata[i]
        if x in char_freq_dict:
            char_freq_dict[x] = char_freq_dict[x] + 1
        else:
            char_freq_dict[x] = 1
    ##输出统计结果
    #for x in char_freq_dict.keys():
        #print(x,' : ',char_freq_dict[x])
    #一个int型的数有4 byte,将其分成4个字节写入到输出文件
    def inputByte(filehandle, iValue):
        bLast = iValue & 255
        iValue = iValue >> 8 
        bThird = iValue & 255
        iValue = iValue >> 8
        bSec = iValue & 255
        iValue = iValue >> 8
        bFirst = iValue & 255
        iValue = iValue >> 8
        filehandle.write(six.int2byte(bFirst))
        filehandle.write(six.int2byte(bSec))
        filehandle.write(six.int2byte(bThird))
        filehandle.write(six.int2byte(bLast))
    #3.构造huffman编码树 数组，用户构造huffman树
    list_huffmanTrees=[]
    for x in char_freq_dict.keys():
        #定一个一棵只包含叶子节点的Huffman树
        tempTree = HuffmanTree(0, x,char_freq_dict[x],None,None)
        list_huffmanTrees.append(tempTree)
     
    #4.步骤2中获取到的每个值出现的频率的信息
    #4.1 保存叶节点的个数
    length = len(char_freq_dict.keys())
    output = open(outputFileName,'wb')
    inputByte(output, length)
   
    
    #4.2 每个值 及其出现的概率的信息
    #遍历字典 char_freq_dict
    for k,v in char_freq_dict.items():
        output.write(six.int2byte(k))
        inputByte(output, v)
    #5.构造huffman树，并且获取到每个字符对应的编码
    temp = buildHuffmanTree(list_huffmanTrees)
    temp.traverse_huffman_tree(temp.get_root(),'',char_freq_dict)
    
    #6.开始对文件进行压缩
    code = ''
    for i in range(filesize):
        key = filedata[i]
        code = code + char_freq_dict[key]
        out = 0
        while len(code)>8:
            for x in range(8):
                out = out<<1
                if code[x] == '1':
                    out = out | 1
            code = code[8:]
            output.write(six.int2byte(out))
            out = 0
    #处理剩下来的不满8位的code
    """
    压缩对齐方法：
    压缩时：根据Huffman编码对文件进行编码，最后面到的01串不一定是8的倍数，然后文件的最小单位就是8位，
    比如最后剩下101，怎么处理，我们先保存落单的位数，这里是3，则用00000011表示，然后将101左移相应的位数这里
    是5位，变成10100000，所以最后的101变成了0000001110100000
    """     
    output.write(six.int2byte(len(code)))
    out = 0
    for i in range(len(code)):
        out = out<<1
        if code[i] == '1':
            out = out | 1
    for i in range(8-len(code)):
        out = out << 1
    #把最后一位写入到文件中
    output.write(six.int2byte(out))
    output.close()

"""
解压缩思路：
1、以二进制读的方式，读出压缩文件中保存的被压缩文件中[0-255]每个值出现的频率
2、使用上面[0-255]每个值及其对应的权重，构造对应的Huffman编码树，然后分配[0-255]中每一个值对应的Huffman编码
3、接着以二进制的方式读取压缩文件的内容，读出二进制的01串
4、使用步骤3读取出来的01串在步骤2中构造的Huffman编码树中进行解压缩，进行解压缩的方法是：
   1、最开始的current指向编码树的root:
   2、循环取01串的首位；
   3、如果取出的是0，current指向左孩子，否则指向右孩子
   4、判断current是否为叶节点；
      如果是，将该叶节点对应的字符写入到解压缩文件中，并且current重置为编码树的root
      如果不是，继续2,3,4的操作
   5、知道01串被取完，此时解压缩工作完毕。
"""
def decompress(inputFileName,outputFileName):
    """
    解压缩文件
    """
    #读取文件
    f = open(inputFileName,'rb')
    filedata = f.read()
    #获取文件的字节总数
    filesize = f.tell()
    
    #1.读取压缩文件中保存的树的叶节点的个数
    """
    读取4个字节，代表一个int整型
    """
    def bytesToInt(byteslst):
        """
        每取一个字节或操作然后左移8位，取前3个字节，最后一个字节只要或操作即可
        """
        outInt = 0
        for i in byteslst[:-1]:
            outInt = outInt | i
            outInt = outInt << 8
        outInt = outInt | byteslst[-1]
        return outInt
    leaf_node_size = bytesToInt(filedata[0:4])
    #2.读取压缩文件中保存的源文件[0-255]出现的频率的信息
    #构造一个字典，然后重建Huffman编码树,从filedata[4+i*5+0](字符信息的字节)，
    #filedata[4+i*5+1]到filedata[4+i*5+4]是字的频率信息
    char_freq_dict = {}
    for i in range(leaf_node_size):
        char = filedata[4+i*5+0]
        char_freq_dict[char] = bytesToInt(filedata[4+i*5+1:4+i*5+5])
    
    #3.重建Huffman编码树
    list_huffmanTrees = []
    for x in char_freq_dict.keys():
        tempTree = HuffmanTree(0, x, char_freq_dict[x], None, None)
        list_huffmanTrees.append(tempTree)
    temp = buildHuffmanTree(list_huffmanTrees)
    temp.traverse_huffman_tree(temp.get_root(), '', char_freq_dict)
    
    #4.使用步骤3中重建的Huffman树进行解压缩
    output = open(outputFileName,'wb')
    code = ''
    currentnode = temp.get_root()
    for x in range(leaf_node_size*5+4,filesize): #表示总数的4个字节+叶节点的信息字节
        c = filedata[x]
        for i in range(8):
            if c&128: #128: c8位于10000000与操作从高位到低位取值
                code = code + '1'
            else:
                code = code + '0'
            c = c<<1
        while len(code) > 24: #这样能保证最后留下24位待处理
            if currentnode.is_leaf():
                temp_byte = six.int2byte(currentnode.get_value())
                output.write(temp_byte)
                currentnode = temp.get_root()
            if code[0] == '1':
                currentnode = currentnode.get_right()
            else:
                currentnode = currentnode.get_left()
            code = code[1:]
            
    #4.1处理最后24位
    """
    解压缩对齐方法：
    根据Huffman编码对文件进行编码，最后面到的16位可能是被处理过后的结果，
    我们需要取出0000001110100000中的00000011代表10100000前3位是有价值的，其余的舍去
    """  
    sub_code = code[-16:-8]
    last_length = 0
    for i in range(8):
        last_length = last_length <<1
        if sub_code[i] == '1':
            last_length = last_length|1
    code = code[:-16] + code[-8:-8 + last_length]#截取0-8位+最后8位中的前last_length有效位
    while len(code)>0:
        if currentnode.is_leaf():
            temp_byte = six.int2byte(currentnode.get_value())
            output.write(temp_byte)
            currentnode = temp.get_root()
        if code[0] == '1':
            currentnode = currentnode.get_right()
        else:
            currentnode = currentnode.get_left()
        code = code[1:]        
    #最后一个节点
    if currentnode.is_leaf():
        temp_byte = six.int2byte(currentnode.get_value())
        output.write(temp_byte)
        currentnode = temp.get_root()
    # 关闭文件，解压缩结束
    output.close()
if __name__ == '__main__':
    """
    @param :FLAG 0表示压缩文件，1表示解压缩文件
    @param :intputfile输入文件
    @param :outputfile输出文件
    """
    #if len(sys.argv) != 4:
        #print("please input the filename")
        #exit(0)
    #else:
        #FLAG = sys.argv[1]
        #inputFileName = sys.argv[2]
        #outputFileName = sys.argv[3]
    FLAG = '0'
    inputFileName =r'.\testcompress.pdf'
    outputFileName =r'.\fileaftercompress'
    outDecompressFileName =r'.\recoverfile.pdf'
    #压缩文件
    if FLAG == '0':
        print("compress file")
        compress(inputFileName, outputFileName)
        decompress(outputFileName,outDecompressFileName)