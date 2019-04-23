/*****************************************************************************************
 ** FileName:       qAES.c
 ** Author:         Jiawei Hawkins
 ** Date:           2019-04-23 星期二 11:56:43
 ** Description:    实现软件AES加解密
                    接口都为state数组
 *****************************************************************************************/



#include <stdio.h>
#include <windows.h>
#include "qAES_math.h"
#define TIMES 10000


/*****************************************************************************************
 ** Date:           2019-04-23 星期二 12:04:11
 ** Description:    将state经过字节代替、行移位后赋值到out数组中
 *****************************************************************************************/


void sub_shift(int (*state)[4], int (*out)[4]) {
    int row, col, tmp, hang, lie;
    for(row = 0; row < 4; row++) {
        for(col = 0; col < 4; col++) {
            tmp = shiftrow_table[row][col];
            hang = (state[row][tmp]>>4) & 0xf;
            lie = state[row][tmp] & 0xf;
            out[row][col] = s_box[hang][lie];
        }
    }
}


void sub_shift_inv(int (*state)[4], int (*out)[4]) {
    int row, col, tmp, hang, lie;
    for(row = 0; row < 4; row++) {
        for(col = 0; col < 4; col++) {
            tmp = shiftrow_table_inv[row][col];
            hang = (state[row][tmp]>>4) & 0xf;
            lie = state[row][tmp] & 0xf;
            out[row][col] = s_box_inv[hang][lie];
        }
    }
}

/*****************************************************************************************
 ** Date:           2019-04-23 星期二 12:07:12
 ** Description:    将state经过密钥为key的列混淆和轮密钥加后输出到out
 *****************************************************************************************/



void col_xor(int (*state)[4], int (*out)[4], int (*key)[4]) {
    int col;
    for(col = 0; col < 4; col++) {
        out[0][col] = sheet_gf[state[0][col]][1] ^ sheet_gf[state[1][col]][2]\
            ^ state[2][col] ^ state[3][col] ^ key[0][col];

        out[1][col] = state[0][col] ^ sheet_gf[state[1][col]][1]\
            ^ sheet_gf[state[2][col]][2] ^ state[3][col] ^ key[1][col];

        out[2][col] = state[0][col] ^ state[1][col]\
            ^ sheet_gf[state[2][col]][1] ^ sheet_gf[state[3][col]][2] ^ key[2][col];

        out[3][col] = sheet_gf[state[0][col]][2] ^ sheet_gf[state[1][col]][0]\
            ^ sheet_gf[state[2][col]][0] ^ sheet_gf[state[3][col]][1] ^ key[3][col];
    }
}


void col_inv(int (*state)[4], int (*out)[4]) {
    int col;
    for(col = 0; col < 4; col++) {
        out[0][col] = sheet_gf[state[0][col]][6] ^ sheet_gf[state[1][col]][4]\
            ^ sheet_gf[state[2][col]][5] ^ sheet_gf[state[3][col]][3];

        out[1][col] = sheet_gf[state[0][col]][3] ^ sheet_gf[state[1][col]][6]\
            ^ sheet_gf[state[2][col]][4] ^ sheet_gf[state[3][col]][5];

        out[2][col] = sheet_gf[state[0][col]][5] ^ sheet_gf[state[1][col]][3]\
            ^ sheet_gf[state[2][col]][6] ^ sheet_gf[state[3][col]][4];

        out[3][col] = sheet_gf[state[0][col]][4] ^ sheet_gf[state[1][col]][5]\
            ^ sheet_gf[state[2][col]][3] ^ sheet_gf[state[3][col]][6];
    }
}



void col_xor_inv(int (*state)[4], int (*out)[4], int (*key)[4]) {
    int col;
    for(col = 0; col < 4; col++) {
        out[0][col] = sheet_gf[state[0][col]][6] ^ sheet_gf[state[1][col]][4]\
            ^ sheet_gf[state[2][col]][5] ^ sheet_gf[state[3][col]][3] ^ key[0][col];

        out[1][col] = sheet_gf[state[0][col]][3] ^ sheet_gf[state[1][col]][6]\
            ^ sheet_gf[state[2][col]][4] ^ sheet_gf[state[3][col]][5] ^ key[1][col];

        out[2][col] = sheet_gf[state[0][col]][5] ^ sheet_gf[state[1][col]][3]\
            ^ sheet_gf[state[2][col]][6] ^ sheet_gf[state[3][col]][4] ^ key[2][col];

        out[3][col] = sheet_gf[state[0][col]][4] ^ sheet_gf[state[1][col]][5]\
            ^ sheet_gf[state[2][col]][3] ^ sheet_gf[state[3][col]][6] ^ key[3][col];
    }
}


/*****************************************************************************************
 ** Date:           2019-04-23 星期二 12:07:12
 ** Description:    将state经过密钥为key的轮密钥加后输出到out
 *****************************************************************************************/

void _xor(int (*state)[4], int (*out)[4], int (*key)[4]) {
    int col;
    for(col = 0; col < 4; col++) {
        out[0][col] = state[0][col] ^ key[0][col];
        out[1][col] = state[1][col] ^ key[1][col];
        out[2][col] = state[2][col] ^ key[2][col];
        out[3][col] = state[3][col] ^ key[3][col];
    }
}

void key_generate(int (*key)[4], int (*keys)[4][4]) {
    int index, hang, lie, row, col;
    for(col = 0; col < 4; col++){
        for(row = 0; row < 4; row++) {
            keys[0][row][col] = key[row][col];
        }
    }

    for(index = 1; index < 11; index++) {
        hang = (key[1][3]>>4) & 0xf;
        lie = key[1][3] & 0xf;
        key[0][0] = s_box[hang][lie] ^ rc[index - 1] ^ key[0][0];

        hang = (key[2][3]>>4) & 0xf;
        lie = key[2][3] & 0xf;
        key[1][0] = s_box[hang][lie] ^ key[1][0];

        hang = (key[3][3]>>4) & 0xf;
        lie = key[3][3] & 0xf;
        key[2][0] = s_box[hang][lie] ^ key[2][0];

        hang = (key[0][3]>>4) & 0xf;
        lie = key[0][3] & 0xf;
        key[3][0] = s_box[hang][lie] ^ key[3][0];

        keys[index][0][0] = key[0][0];  keys[index][1][0] = key[1][0];
        keys[index][2][0] = key[2][0];  keys[index][3][0] = key[3][0];
        for(col = 1; col < 4; col++){
            for(row = 0; row < 4; row++) {
                key[row][col] = key[row][col] ^ key[row][col - 1];
                keys[index][row][col] = key[row][col];
            }
        }            
    }
}


void qaes_encode(int (*state)[4], int(*out)[4], int (*keys)[4][4]) {
    int index;
    _xor(state, out, keys[0]);



    for(index = 1; index < 10; index++) {
        sub_shift(out, state);
        col_xor(state, out, keys[index]);
    }

    sub_shift(out, state);
    _xor(state, out, keys[10]);
}


void qaes_decode(int (*state)[4], int(*out)[4], int (*keys)[4][4]) {
    int index, tmp[4][4];
    _xor(state, out, keys[10]);

    for(index = 9; index > 0; index--) {
        col_inv(keys[index], tmp);
        sub_shift_inv(out, state);
        col_xor_inv(state, out, tmp);
    }
    sub_shift_inv(out, state);
    _xor(state, out, keys[0]);
}

int main(void) {
    
    int key_encode[][4] = {
        {0x0f, 0x47, 0x0c, 0xaf},
        {0x15, 0xd9, 0xb7, 0x7f},
        {0x71, 0xe8, 0xad, 0x67},
        {0xc9, 0x59, 0xd6, 0x98}
    };
    

    int key_decode[][4] = {
        {0x0f, 0x47, 0x0c, 0xaf},
        {0x15, 0xd9, 0xb7, 0x7f},
        {0x71, 0xe8, 0xad, 0x67},
        {0xc9, 0x59, 0xd6, 0x98}
    };

    int state[][4] = {
        {0x01, 0x89, 0xfe, 0x76},
        {0x23, 0xab, 0xdc, 0x54},
        {0x45, 0xcd, 0xba, 0x32},
        {0x67, 0xef, 0x98, 0x10}
    };
    


    int keys[11][4][4], res[4][4];
    DWORD start = GetTickCount();
    for(int times = 0; times < TIMES; times++) {
        key_generate(key_encode, keys);
        qaes_encode(state, res, keys);


        key_generate(key_decode, keys);
        qaes_decode(res, state, keys);
    }
    DWORD end = GetTickCount();
    double runtime = 1000 * (double)(end - start);
    printf("10000 times AES encode and decode in %.0fms, average in %.5fus\n",runtime/1000, runtime/TIMES);
    
    for(int row = 0; row < 4; row++){
        for(int col = 0; col < 4; col++) {
            printf("%02x ", state[row][col]);
        }
        printf("\n");
    }


    printf("%s","Press any key to exit");
    getchar();
    return 0;
}