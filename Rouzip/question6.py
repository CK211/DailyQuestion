import os
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor

from termcolor import cprint, colored

root = os.getcwd()


def statistic_code_file(file):
    with open(file) as fp:
        files = fp.read()


def statistics_file(root=root):
    parser = argparse.ArgumentParser(
        prog='have fun', description='����С�ű���ͳ���ļ�����')
    parser.add_argument('-p', '--path', nargs='?',
                        help='ͳ���ļ���λ��', default=os.getcwd())
    parser.add_argument('-t', '--type', nargs='?', help='ͳ���ļ�����',
                        choices=['python', 'java'])
    parser.add_argument('--version', action='version', version='%(prog)s 0.01')
    kargs = parser.parse_args()
    # Ĭ���޲������
    if len(sys.argv[1:]) == 0:
        file_num = 0
        dir_num = 0
        for _, dirs, files in os.walk(kargs.path):
            file_num = file_num + len(files)
            dir_num += len(dirs)
        # cprint('�ļ�����Ϊ��' + str(file_num), 'red', attrs=['bold'])
        # cprint('�ļ��и���Ϊ��' + str(dir_num), 'red', attrs=['bold'])
    # ָ�����ļ��е�ַ��û��ѡ������ļ�
    elif kargs.path and kargs.type == None:
        if os.path.exists(kargs.path):
            file_num = 0
            dir_num = 0
            for _, dirs, files in os.walk(kargs.path):
                file_num += len(files)
                dir_num += len(dirs)
            cprint('�ļ�����Ϊ��' + str(file_num), 'blue', attrs=['bold'])
            cprint('�ļ��и���Ϊ��' + str(dir_num), 'blue', attrs=['bold'])
        else:
            cprint('�����ڸ��ļ��У�', 'red', attrs=['bold'], file=sys.stderr)
    # û��ָ����ʹ�õ�ǰ·��
    elif kargs.path == os.getcwd() and kargs.type != None:
        file_num = 0
        # ע������
        comment_num = 0
        # ��������
        code_num = 0
        # �ո�����
        blank_num = 0
        # ��Ϊ��ǣ��ж��ǲ����ڶ���ע��֮��
        in_muti_comment = False
        for _, _, files in os.walk():
            # �������е�python�ļ���ͳ��
            if kargs.type == 'python':
                for file in files:
                    # ����python��ֱ������
                    if file.split('.')[-1] != 'py':
                        continue
                    file_num += 1
                    with open(file) as f:
                        line = f.readline().strip()
                        # ��������ڶ���ע�ͽ׶�
                        if not in_muti_comment:
                            # ���ֿ��ܣ����룬����ע�ͣ�����
                            if len(line) == 0:
                                blank_num += 1
                            elif line.startswith("#"):
                                comment_num += 1
                            elif line.startswith("'''") or line.startswith('"""'):
                                in_muti_comment = True
                                comment_num += 1
                            else:
                                code_num += 1
                        else:
                            if line.endswith("'''") or line.endswith('"""'):
                                comment_num += 1
                                in_muti_comment = False
                            else:
                                comment_num += 1
            else:
                # �������е�java��ͳ��
                for file in files:
                    if file.split('.')[-1] != 'java':
                        continue
                    file_num += 1
                    with open(file) as f:
                        line = f.readline().strip()
                        # ��������ڶ���ע�ͽ׶�
                        if not in_muti_comment:
                            # ���ֿ��ܣ����룬����ע�ͣ�����
                            if len(line) == 0:
                                blank_num += 1
                            elif line.startswith("//"):
                                comment_num += 1
                            elif line.startswith("/*"):
                                in_muti_comment = True
                                comment_num += 1
                            else:
                                code_num += 1
                        else:
                            if line.endswith("*/"):
                                comment_num += 1
                                in_muti_comment = False
                            else:
                                comment_num += 1
        cprint('�ļ�����Ϊ��' + str(file_num), 'blue', attrs=['bold'])
        cprint('��������Ϊ��' + str(code_num), 'blue', attrs=['bold'])
        cprint('�ո�����Ϊ��' + str(blank_num), 'blue', attrs=['bold'])
        cprint('ע������Ϊ��' + str(comment_num), 'blue', attrs=['bold'])

if __name__ == '__main__':
    statistics_file()

'''
˼·�����Ƚ������������û��·��������������������ֱ�Ӵ�ӡ��ǰĿ¼��ͳ�Ƶ��ļ��������ļ�������
�����·����ʹ�ø�·�����޲�������µ��ļ��������ļ�������
����в�������ǰλ���£�����ָ���ļ��ĸ�����code and comment and blank
�޲���ͬ����
��-v���ӡ����
'''
