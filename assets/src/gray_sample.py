import random
import numpy as np

def gray_to_binary(gray):
    binary = np.zeros_like(gray)
    binary[0] = gray[0]  # 最上位ビットはそのままコピー
    for i in range(1, len(gray)):
        binary[i] = binary[i - 1] ^ gray[i]  # 直前のビットとXOR
    return binary

def main():
    a = [0, 1, 1, 0, 1, 0, 1, 0]
    a = np.array(a).reshape(2, 4)
    print(f'shape: {a.shape}')
    print(f'norm: {a[0]}')
    print(f'gray: {gray_to_binary(a[0])}')

if __name__ == '__main__':
    main()
