#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 起源是：因为 md5sum 不能在管道中使用
# 主要目的是：计算在管道中流的 md5sum, 并记录在指定文件中
# 实例:
#   tar -cf - *.conf | gzip -n | python md5sum.py today.md5 | openssl des3 -salt -k \$PASS | dd of=${PATH}/${NAME}.des3

import hashlib
import sys


def get_md5(i_file, out):
    m = hashlib.md5()
    while True:
        data = i_file.read(4096)
        if not data:
            break
        m.update(data)
        out(data)
    return m.hexdigest()


def main():
    n = len(sys.argv)
    if n <= 1 or n > 3:
        sys.stdout.write("usage: %s [IN_FILE] OUT_MD5_FILE" % sys.argv[0])
        sys.exit(1)

    i_file = sys.stdin if n == 2 or sys.argv[1] == '-' else open(sys.argv[1], 'rb')
    out, m_file = (lambda x: (), sys.stdout) if sys.argv[-1] == '-' else (sys.stdout.write, open(sys.argv[-1], 'w'))

    m_file.write(get_md5(i_file, out))
    if sys.argv[-1] == '-':
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()
