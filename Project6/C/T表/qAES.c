/*****************************************************************************************
 ** FileName:       qAES.c
 ** Author:         Jiawei Hawkins
 ** Date:           2019-04-23 星期二 11:56:43
 ** Description:    实现软件AES加解密
                    接口都为state数组
 *****************************************************************************************/



#include <stdio.h>
#include <time.h>
#include "qAES_math.h"
#define TIMES 100000

unsigned char state[][4] = {
    {0x01, 0x89, 0xfe, 0x76},
    {0x23, 0xab, 0xdc, 0x54},
    {0x45, 0xcd, 0xba, 0x32},
    {0x67, 0xef, 0x98, 0x10},
};


unsigned char key[][4] = {
    {0x0f, 0x47, 0x0c, 0xaf},
    {0x15, 0xd9, 0xb7, 0x7f},
    {0x71, 0xe8, 0xad, 0x67},
    {0xc9, 0x59, 0xd6, 0x98},
};


unsigned char state_show[][4] = {
    {0x01, 0x89, 0xfe, 0x76},
    {0x23, 0xab, 0xdc, 0x54},
    {0x45, 0xcd, 0xba, 0x32},
    {0x67, 0xef, 0x98, 0x10},
};


unsigned __int32 a;
unsigned __int32 * tmp3 = &a;
unsigned char out[4][4];
unsigned char (*tmp1)[4];
unsigned char (*tmp2)[4];



unsigned char keys[11][4][4];


/*****************************************************************************************
 ** Date:           2019-04-23 星期二 12:04:11
 ** Description:    加密算法，输入的state的行与实际AES算法中的state矩阵的列
 *****************************************************************************************/
void key_generate(unsigned __int32 *key, unsigned __int32 (*keys)[4]) {

    keys[0][0] = key[0]; keys[0][1] = key[1]; keys[0][2] = key[2]; keys[0][3] = key[3];
    for(int index = 1; index < 11; index++) {
        *tmp3 = keys[index - 1][3];
        keys[index][0] = keys[index - 1][0] ^ rc[index] ^ s_box[(*tmp3 & 0xff00)>>8]\
        ^ (s_box[(*tmp3 & 0xff0000)>>16] << 8) ^ (s_box[(*tmp3 & 0xff000000)>>24] << 16)\
        ^ (s_box[*tmp3 & 0xff]<<24);
        keys[index][1] = keys[index - 1][1] ^ keys[index][0];
        keys[index][2] = keys[index - 1][2] ^ keys[index][1];
        keys[index][3] = keys[index - 1][3] ^ keys[index][2];
    }
}



void encode(unsigned __int32 *state, unsigned __int32 *out, unsigned __int32(*key)[4]) {

    state[0] = state[0] ^ key[0][0]; state[1] = state[1] ^ key[0][1];
    state[2] = state[2] ^ key[0][2]; state[3] = state[3] ^ key[0][3];

    for(int index = 1; index < 10; index++) {
        out[0] = T0[state[0] & 0xff] ^ T1[(state[1] & 0xff00)>>8]\
        ^ T2[(state[2] & 0xff0000)>>16] ^ T3[(state[3] & 0xff000000)>>24] ^ key[index][0];

        out[1] = T0[state[1] & 0xff] ^ T1[(state[2] & 0xff00)>>8]\
        ^ T2[(state[3] & 0xff0000)>>16] ^ T3[(state[0] & 0xff000000)>>24] ^ key[index][1];

        out[2] = T0[state[2] & 0xff] ^ T1[(state[3] & 0xff00)>>8]\
        ^ T2[(state[0] & 0xff0000)>>16] ^ T3[(state[1] & 0xff000000)>>24] ^ key[index][2];

        out[3] =  T0[state[3] & 0xff] ^ T1[(state[0] & 0xff00)>>8]\
        ^ T2[(state[1] & 0xff0000)>>16] ^ T3[(state[2] & 0xff000000)>>24] ^ key[index][3];


        tmp3 = state;
        state = out;
        out = tmp3;
    }
    
    tmp1 = (unsigned char (*)[4])state; tmp2 = (unsigned char (*)[4])out;
    tmp2[0][0] = s_box[tmp1[0][0]]; tmp2[0][1] = s_box[tmp1[1][1]]; tmp2[0][2] = s_box[tmp1[2][2]]; tmp2[0][3] = s_box[tmp1[3][3]];
    tmp2[1][0] = s_box[tmp1[1][0]]; tmp2[1][1] = s_box[tmp1[2][1]]; tmp2[1][2] = s_box[tmp1[3][2]]; tmp2[1][3] = s_box[tmp1[0][3]];
    tmp2[2][0] = s_box[tmp1[2][0]]; tmp2[2][1] = s_box[tmp1[3][1]]; tmp2[2][2] = s_box[tmp1[0][2]]; tmp2[2][3] = s_box[tmp1[1][3]];
    tmp2[3][0] = s_box[tmp1[3][0]]; tmp2[3][1] = s_box[tmp1[0][1]]; tmp2[3][2] = s_box[tmp1[1][2]]; tmp2[3][3] = s_box[tmp1[2][3]];
    

    out[0] = out[0] ^ key[10][0];
    out[1] = out[1] ^ key[10][1];
    out[2] = out[2] ^ key[10][2];
    out[3] = out[3] ^ key[10][3];   
}



void decode(unsigned __int32 *state, unsigned __int32 *out, unsigned __int32(*key)[4]) {

    state[0] = state[0] ^ key[10][0]; state[1] = state[1] ^ key[10][1];
    state[2] = state[2] ^ key[10][2]; state[3] = state[3] ^ key[10][3];


    for(int index = 9; index > 0; index--) {
        out[0] = T0_inv[state[0] & 0xff] ^ T1_inv[(state[3] & 0xff00)>>8]\
        ^ T2_inv[(state[2] & 0xff0000)>>16] ^ T3_inv[(state[1] & 0xff000000)>>24]\
        ^ Col0_inv[key[index][0] & 0xff] ^ Col1_inv[(key[index][0] & 0xff00)>>8]\
        ^ Col2_inv[(key[index][0] & 0xff0000)>>16] ^ Col3_inv[(key[index][0] & 0xff000000)>>24];

        out[1] = T0_inv[state[1] & 0xff] ^ T1_inv[(state[0] & 0xff00)>>8]\
        ^ T2_inv[(state[3] & 0xff0000)>>16] ^ T3_inv[(state[2] & 0xff000000)>>24] \
        ^ Col0_inv[key[index][1] & 0xff] ^ Col1_inv[(key[index][1] & 0xff00)>>8]\
        ^ Col2_inv[(key[index][1] & 0xff0000)>>16] ^ Col3_inv[(key[index][1] & 0xff000000)>>24];

        out[2] = T0_inv[state[2] & 0xff] ^ T1_inv[(state[1] & 0xff00)>>8]\
        ^ T2_inv[(state[0] & 0xff0000)>>16] ^ T3_inv[(state[3] & 0xff000000)>>24] \
        ^ Col0_inv[key[index][2] & 0xff] ^ Col1_inv[(key[index][2] & 0xff00)>>8]\
        ^ Col2_inv[(key[index][2] & 0xff0000)>>16] ^ Col3_inv[(key[index][2] & 0xff000000)>>24];

        out[3] = T0_inv[state[3] & 0xff] ^ T1_inv[(state[2] & 0xff00)>>8]\
        ^ T2_inv[(state[1] & 0xff0000)>>16] ^ T3_inv[(state[0] & 0xff000000)>>24]\
        ^ Col0_inv[key[index][3] & 0xff] ^ Col1_inv[(key[index][3] & 0xff00)>>8]\
        ^ Col2_inv[(key[index][3] & 0xff0000)>>16] ^ Col3_inv[(key[index][3] & 0xff000000)>>24];


        tmp3 = state;
        state = out;
        out = tmp3;
    }
    
    tmp1 = (unsigned char (*)[4])state; tmp2 = (unsigned char (*)[4])out;
    tmp2[0][0] = s_box_inv[tmp1[0][0]]; tmp2[0][1] = s_box_inv[tmp1[3][1]]; 
    tmp2[0][2] = s_box_inv[tmp1[2][2]]; tmp2[0][3] = s_box_inv[tmp1[1][3]];
    tmp2[1][0] = s_box_inv[tmp1[1][0]]; tmp2[1][1] = s_box_inv[tmp1[0][1]]; 
    tmp2[1][2] = s_box_inv[tmp1[3][2]]; tmp2[1][3] = s_box_inv[tmp1[2][3]];
    tmp2[2][0] = s_box_inv[tmp1[2][0]]; tmp2[2][1] = s_box_inv[tmp1[1][1]];
    tmp2[2][2] = s_box_inv[tmp1[0][2]]; tmp2[2][3] = s_box_inv[tmp1[3][3]];
    tmp2[3][0] = s_box_inv[tmp1[3][0]]; tmp2[3][1] = s_box_inv[tmp1[2][1]]; 
    tmp2[3][2] = s_box_inv[tmp1[1][2]]; tmp2[3][3] = s_box_inv[tmp1[0][3]];
    

    out[0] = out[0] ^ key[0][0];
    out[1] = out[1] ^ key[0][1];
    out[2] = out[2] ^ key[0][2];
    out[3] = out[3] ^ key[0][3];

    
}

void swap(unsigned char (*matrix)[4]) {
    unsigned char z;
    for(int row = 0; row < 4; row++) {
        for(int col = row + 1; col < 4; col++) {
            z = matrix[row][col];
            matrix[row][col] = matrix[col][row];
            matrix[col][row] = z;
        }
    }
}

int main(void){

    swap(state);  swap(key);
    time_t start, finish;

    key_generate((unsigned __int32 *)key, (unsigned __int32 (*)[4])keys);
    start = clock();
    for(int index = 0; index < TIMES; index++)
        encode((unsigned __int32 *)state, (unsigned __int32 *)out, (unsigned __int32 (*)[4])keys);
    double t = clock() - start;
    printf("%d encode for %lfs, each average time for %lfus\n", TIMES, (double)t/CLOCKS_PER_SEC, 1000000.0*(double)t/TIMES/CLOCKS_PER_SEC);

    printf("Plaintext:\n");
    for(int row = 0; row < 4; row++) {
        for(int col = 0; col < 4; col++) {
            printf("%02x ", state_show[row][col]);
        }
        printf("\n");
    }
    putchar('\n');

    swap(state_show);
    encode((unsigned __int32 *)state_show, (unsigned __int32 *)out, (unsigned __int32 (*)[4])keys);

    printf("Cipher:\n");
    swap(state);
    for(int row = 0; row < 4; row++) {
        for(int col = 0; col < 4; col++) {
            printf("%02x ", state_show[row][col]);
        }
        printf("\n");
    }
    putchar('\n');

    swap(state);
    decode((unsigned __int32 *)state_show, (unsigned __int32 *)out, (unsigned __int32 (*)[4])keys);
    printf("Plaintext:\n");
    swap(state_show);
    for(int row = 0; row < 4; row++) {
        for(int col = 0; col < 4; col++) {
            printf("%02x ", state_show[row][col]);
        }
        printf("\n");
    }

    printf("%s","Press any key to exit");
    getchar();
    return 0;
}