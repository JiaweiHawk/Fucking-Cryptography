/*****************************************************************************************
 ** FileName:        BigNum.c
 ** Author:          Jiawei Hawkins
 ** Date:            2019-03-02 星期六 15:30:16
 ** Description:     实现大数的存储及一些运算等,包括乘法使用Karatsuba算法;
 *****************************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX(a, b) (a > b ? a : b)
typedef struct BigNum
{
    char *value;            //输入的字符串,value是大数的低位。
    int pos;                //是否为正数
    int len;                //数组value的长度
} bignum_t;
//定义大数结构


int inv_0(bignum_t *bignum)
{
    int ind1, ind2, ind3 = (*bignum).len;
    for(ind1 = 0, ind2 = 0; ind1 < ind3; ind1++)                         //排除无效的输入
    {
        if( (*bignum).value[ind1] < '0' || (*bignum).value[ind1] > '9')
            return 0;

        if( !ind2 && (*bignum).value[ind1] == '0')
            (*bignum).len--;
        else
            (*bignum).value[ind2++] = (*bignum).value[ind1];
    }
    for(ind1 = 0, ind2 = (*bignum).len - 1; ind1 < ind2; ind1++, ind2--)
    {
        ind3 = (*bignum).value[ind1];
        (*bignum).value[ind1] = (*bignum).value[ind2];
        (*bignum).value[ind2] = ind3;
    }
    return 1;
}
/*  如果输入字符串有效，则去掉无用0,并返回1
 *  如果输入无效，则返回0 */


bignum_t *init(void)
{
    bignum_t *in;
    int flag;
    in = (bignum_t*)malloc(sizeof(bignum_t));
    do
    {
        printf("请输入有效数据：");
        scanf("%s", (*in).value);
        getchar();
        (*in).len = strlen( (*in).value);
        flag = inv_0(in);
    }while( !flag );
    return in;
}
/*  接受有效的大数输入   */


void delete(bignum_t *bignum)
{
    free( (*bignum).value);
    free(bignum);
}
/*  删除大数结构  */

char *add(bignum_t *a, bignum_t *b)
{
    char *ans;
    int index, carry = 0, alen = (*a).len, blen = (*b).len, len = MAX(alen, blen);
    ans = (char*)new malloc( sizeof(char) * (len + 1) );
    
}
/*      大数加法实现，返回字符串      */


int main(void)
{
    bignum_t *p;
    p = init();
    for(int index = (*p).len - 1; index >= 0; index--)
    {
        printf("%c", (*p).value[index]);
    }
    delete( p );
    return 0;
}
 
 
