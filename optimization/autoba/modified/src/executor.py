# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/11 12:49
@Auth ： Juexiao Zhou
@File ：executor.py
@IDE ：PyCharm
@Page: www.joshuachou.ink
"""

import subprocess
import time

class CodeExecutor:
    def __init__(self):
        self.bash_code_path = None
        self.code_prefix = [
            'mamba activate abc_runtime',
        ]
        self.code_postfix = [
        ]

    def execute(self, bash_code_path):

        self.bash_code_path = bash_code_path
        with open(self.bash_code_path, 'r') as input_file:
            bash_content = input_file.read()

        self.bash_code_path_execute = self.bash_code_path + '.execute.sh'

        # 打开新生成的 Bash 文件以供写入
        with open(self.bash_code_path_execute, 'w') as output_file:
            for code in self.code_prefix:
                output_file.write(code + '\n')
            # 写入原始内容
            output_file.write(bash_content)
            output_file.write('\n')  # 确保在新行开始
            for code in self.code_postfix:
                output_file.write(code + '\n')

        # 使用 subprocess 执行 Bash 文件，将输出捕获到一个字符串中
        process = subprocess.Popen(['bash', '-i', '-e', self.bash_code_path_execute],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            text=True)

        # Drain both pipes concurrently: sequential reads can deadlock on stderr.
        stdout, stderr = process.communicate()
        print(stdout, end='')
        print(stderr, end='')
        executor_info = (f'exit_code={process.returncode}\n'
                         f'stdout_tail:\n{stdout[-5000:]}\n'
                         f'stderr_tail:\n{stderr[-5000:]}')
        return executor_info