/*****************************************************************************************
 ** FileName:       BigInt.c
 ** Author:         Jiawei Hawkins
 ** Date:           2019-05-04 星期六 10:10:43
 ** Description:    实现大数运算
 *****************************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define init 128



char *tmp_bigint;




struct BIGINT {
    int length;
    char *value;
    int capacity;
    char ismin;
};

typedef struct BIGINT Bigint;

//数字是正序、除去多余的0
void check_0(Bigint *ptr) {
    int index = 0, left = 0, num = ptr->length;
    for(;left < num; left++) {
        if(ptr->value[left]) {
            ptr->length = num - left;
            for(index = 0; left < num;)
                ptr->value[index++] = ptr->value[left++];
            return ;
        }
    }
    ptr->length = 1;    ptr->value[0] = 0;
}

void reverse(Bigint *ptr) {
    int left, right, tmp;
    for(left = 0, right = ptr->length - 1; left < right;) {
        tmp = ptr->value[left];
        ptr->value[left++] = ptr->value[right];
        ptr->value[right--] = tmp;
    }
}


void initial_Bigint(Bigint *ptr) {
    int index, ch;
    ptr->value = (char *)malloc(sizeof(char) * init);   ptr->ismin = 0;

    for(index = 0; index < init; index++)
        ptr->value[index] = 0;

    ptr->capacity = init;
    ptr->length = 0;
    printf("Enter the Number:");
    while( (ch = getchar()) > '9' && ch < '0'  && ch != '-' && ch != '+');
    if(ch == '-') {
        ptr->ismin = 1;
        ch = getchar();
    }
    else if(ch == '+')
        ch = getchar();

    do {
        if(ptr->length >= ptr->capacity) {
            ptr->capacity *= 2;
            tmp_bigint = (char *)malloc(sizeof(char) * ptr->capacity);
            for(index = 0; index < ptr->length; index++)
                tmp_bigint[index] = ptr->value[index];
            for(;index < ptr->capacity; index++)
                tmp_bigint[index] = 0;
            
            free(ptr->value);   
            ptr->value = tmp_bigint;
        }
        ptr->value[(ptr->length)++] = ch - '0';
    }while( (ch = getchar()) <= '9' && ch >= '0');

    check_0(ptr);
    reverse(ptr);  
}

void show(Bigint *ptr) {
    if(ptr == NULL) {
        printf("Error\n");
        return;
    }
    int index;
    reverse(ptr);
    if(ptr->ismin)
        printf("(-");
    for(index = 0; index < ptr->length; index++)
        putchar(ptr->value[index] + '0');
	if(ptr->ismin)
        putchar(')');
    reverse(ptr);
}

// 比较a和b比较前len位的绝对值大小，a>b返回1, a==b返回0
int abs_compare(Bigint *a, Bigint *b, int len) {
    int index, tmp, a_len = a->length - 1, b_len = b->length - 1;
    if(len > a->length && len > b->length) {
        if(a_len > b_len)   return 1;
        if(a_len < b_len)   return -1;
        len = a_len;
    }else if(len > a->length)  return -1;
    else if(len > b->length)   return 1;
    for(index = 0; index < len; index++) {
        if(a->value[a_len] > b->value[b_len])   return 1;
        if(b->value[b_len--] > a->value[a_len--])   return -1;
    }
    return 0;
}

//将b加到a,并以out输出

Bigint *add(Bigint *a, Bigint *b) {
    int index, cin = 0, length = a->length > b->length?a->length:b->length, ind1;
    Bigint *out = (Bigint*)malloc(sizeof(Bigint));  out->value = (char*)malloc(sizeof(char) * (length + 1));
    out->capacity = length + 1;
    for(index = 0; index < out->capacity; index++)
        out->value[index] = 0;
    if(a->ismin == b->ismin) {
        out->ismin = a->ismin;
        for(index = 0; index <= length; index++) {
            if( (index >= a->length) && (index >= b->length) ) {
                if(cin)
                    out->value[index++] = cin;
                out->length = index;
            }    
            else if(index >= a->length) {
                cin += b->value[index];
                out->value[index] = cin % 10;
                if(cin > 9)
                    cin = 1;
                else 
                    cin = 0;
            }else if(index >= b->length) {
                cin += a->value[index];
                out->value[index] = cin % 10;
                if(cin > 9)
                    cin = 1;
                else 
                    cin = 0;
            }else {
                cin += b->value[index] + a->value[index];
                out->value[index] = cin % 10;
                if(cin > 9)
                    cin = 1;
                else 
                    cin = 0;
            }
        }
    }else {
        if(abs_compare(a, b, a->length>b->length?a->length:b->length) > 0) {
            out->ismin = a->ismin;
            for(index = 0; index < length; index++) {
                if(index >= a->length) {
                    cin = -b->value[index] - cin;
                    if(cin < 0) {
                        out->value[index] = cin + 10;
                        cin = 1;
                    }else {
                        out->value[index] = cin;
                        cin = 0;
                    }
                }else if(index >= b->length) {
                    cin = a->value[index] - cin;
                    if(cin < 0) {
                        out->value[index] = cin + 10;
                        cin = 1;
                    }else {
                        out->value[index] = cin;
                        cin = 0;
                    }
                }else {
                    cin = a->value[index] - cin - b->value[index];
                    if(cin < 0) {
                        out->value[index] = cin + 10;
                        cin = 1;
                    }else {
                        out->value[index] = cin;
                        cin = 0;
                    }
                }
            }
        }else {
            out->ismin = b->ismin;
            for(index = 0; index < length; index++) {
                if(index >= a->length) {
                    cin = b->value[index] - cin;
                    if(cin < 0) {
                        out->value[index] = cin + 10;
                        cin = 1;
                    }else {
                        out->value[index] = cin;
                        cin = 0;
                    }
                }else if(index >= b->length) {
                    cin = -a->value[index] - cin;
                    if(cin < 0) {
                        out->value[index] = cin + 10;
                        cin = 1;
                    }else {
                        out->value[index] = cin;
                        cin = 0;
                    }
                }else {
                    cin = b->value[index] - a->value[index] - cin;
                    if(cin < 0) {
                        out->value[index] = cin + 10;
                        cin = 1;
                    }else {
                        out->value[index] = cin;
                        cin = 0;
                    }

                }
            } 
        }
        out->length = index;
        reverse(out);
        check_0(out);
        reverse(out);
    }
    return out;
}


Bigint *min(Bigint *a, Bigint *b) {
    Bigint tmp = *b;
    tmp.ismin = !tmp.ismin;
    return add(a, &tmp);
}


Bigint *mul_one(Bigint *a, char b, int shiftrow) {
    int index, cin = 0, ind1;
    Bigint *tmp = (Bigint*)malloc(sizeof(Bigint));
    tmp->capacity = a->length + shiftrow + 2;  tmp->ismin = a->ismin;
    tmp->value = (char*)malloc(sizeof(char) * tmp->capacity);

    for(index = 0; index < tmp->capacity; index++)
        tmp->value[index] = 0;
    
    for(index = 0, tmp->length = a->length; index < a->length; index++) {
        cin += a->value[index] * b;
        tmp->value[index] = cin % 10;
        cin /= 10;
    }
    if(cin) {
        tmp->value[ (tmp->length)++] = cin;
    }
    if(shiftrow == 0)
        return tmp;
    for(index = tmp->length - 1; index >= 0; index--) {
        tmp->value[index + shiftrow] = tmp->value[index];
        tmp->value[index] = 0;
    }
    tmp->length += shiftrow;
    return tmp;
}

Bigint *mul(Bigint *a, Bigint *b) {
    int index, ismin = a->ismin ^ b->ismin;
    Bigint *out, *tmp, *tmp1;
    a->ismin = 0;
    out = mul_one(a, b->value[0], 0);   out->ismin = 0;
    for(index = 1; index < b->length; index++) {
        tmp = mul_one(a, b->value[index], index);
        tmp1 = out;
        out = add(out, tmp);
        free(tmp1->value);   free(tmp1);
        free(tmp->value);   free(tmp);
    }
    out->ismin = ismin;
    return out;
}


void divide(Bigint *a, Bigint *b, Bigint *q, Bigint *r) {
    if( (b->length == 1 && b->value[0] == 0) || b->ismin) {
        printf("Error! b > 0\n");
        return;
    }
    int index, tmp = a->length - b->length;
    Bigint *tmp_delete, *r_delete;
    q->value = (char*)malloc(sizeof(char) * a->length);   q->capacity = a->length;  q->ismin = a->ismin;
    r->value = (char*)malloc(sizeof(char) * a->length); r->capacity = a->length;    r->ismin = a->ismin;

    for(index = 0; index < q->capacity; index++)
        q->value[index] = 0;

    for(index = 0, r->length = a->length; index < r->capacity; index++)
        r->value[index] = a->value[index];

    if(abs_compare(a, b, a->length > b->length?a->length:b->length) < 0){
        q->length = 1;
        return;
    }
    if(abs_compare(a, b, b->length) < 0)    tmp--;
    index = a->length;  q->length = tmp + 1;
    tmp_delete = mul_one(b, 1, tmp);    tmp_delete->ismin = a->ismin;
    while( abs_compare(r, b, r->length > b->length?r->length:b->length) >= 0) {
        q->value[tmp]++;
        r_delete = min(r, tmp_delete);
        //show(r_delete); putchar(' ');  show(tmp_delete);  putchar(' ');  show(q);    putchar('\n');//
        r->length = r_delete->length;   r->value = r_delete->value;
        r->value = r_delete->value;
        free(r_delete);
        if(index < r->length || abs_compare(r, tmp_delete, tmp_delete->length) < 0) {
            tmp = r->length - b->length;    
            free(tmp_delete->value);    free(tmp_delete);
            if(tmp < 0)
                break;
            tmp_delete = mul_one(b, 1, tmp);    tmp_delete->ismin = a->ismin;
            if(abs_compare(r, tmp_delete, tmp_delete->length) < 0) {
                free(tmp_delete->value);    free(tmp_delete);
                if( (--tmp) < 0)
                    break;
                tmp_delete = mul_one(b, 1, tmp);    tmp_delete->ismin = a->ismin;
            }
            index = tmp;
        }
    }
    if(r->ismin) {
        r_delete = add(r, b);
        free(r->value);
        r->length = r_delete->length;   r->ismin = r_delete->ismin;
        r->value = r_delete->value; free(r_delete);

        tmp_delete = (Bigint*)malloc(sizeof(Bigint));
        tmp_delete->value = (char*)malloc(sizeof(char));
        tmp_delete->value[0] = 1;   tmp_delete->ismin = 1;  tmp_delete->capacity = tmp_delete->length = 1;
        r_delete = add(q, tmp_delete);
        free(q->value);
        q->length = r_delete->length;  q->value = r_delete->value;
        free(r_delete); free(tmp_delete->value);    free(tmp_delete);
    }
    return;  
}

void divide_2(Bigint *a) {
    int index, len = a->length, cin = 0;
    if(a->value[len - 1] < 2)
        a->length--;
    for(int index = len - 1; index >= 0; index--) {
        cin += a->value[index];
        a->value[index] = cin >> 1;
        cin = (cin & 1) * 10;
    }
}

//计算a^b
Bigint* qexp(Bigint *base, Bigint *exp) {
    if(exp->ismin) {
        printf("Error exp<0\n");
        return NULL;
    }
    int flag = (exp->value[0] & 1) && base->ismin;
    Bigint *tmp = (Bigint*)malloc(sizeof(Bigint)), *delete_tmp, *delete_base = base;
    tmp->capacity = 1;  tmp->ismin = base->ismin;   tmp->value = (char*)malloc(sizeof(char));
    tmp->length = 1;    tmp->value[0] = 1;  delete_tmp = tmp;  
    while( exp->length || exp->value[0]) {
        if( (exp->value[0] & 1)) {
            tmp = mul(tmp, base);
            free(delete_tmp->value);    free(delete_tmp);   delete_tmp = tmp;
        }
        base = mul(base, base);
        free(delete_base->value);  free(delete_base);   delete_base = base;
        divide_2(exp);
    }
    tmp->ismin = 0;
    if(flag)
        tmp->ismin = 1;
    return tmp;
}


void add_show(){
    Bigint *a = (Bigint*)malloc(sizeof(Bigint)), *b = (Bigint*)malloc(sizeof(Bigint)),\
    *c = (Bigint*)malloc(sizeof(Bigint));
    initial_Bigint(a);
    initial_Bigint(b);
    c = add(a, b);
    show(a);    printf(" + ");  show(b);    printf(" = ");  show(c);
    free(a->value); free(a);
    free(b->value); free(b);
    free(c->value); free(c);
}

void min_show(){
    Bigint *a = (Bigint*)malloc(sizeof(Bigint)), *b = (Bigint*)malloc(sizeof(Bigint)),\
    *c = (Bigint*)malloc(sizeof(Bigint));
    initial_Bigint(a);
    initial_Bigint(b);
    c = min(a, b);
    show(a);    printf(" - ");  show(b);    printf(" = ");  show(c);
	putchar('\n');
    free(a->value); free(a);
    free(b->value); free(b);
    free(c->value); free(c);
}

void mul_show(){
    Bigint *a = (Bigint*)malloc(sizeof(Bigint)), *b = (Bigint*)malloc(sizeof(Bigint)),\
    *c = (Bigint*)malloc(sizeof(Bigint));
    initial_Bigint(a);
    initial_Bigint(b);
    c = mul(a, b);
    show(a);    printf(" * ");  show(b);    printf(" = ");  show(c);
	putchar('\n');
    free(a->value); free(a);
    free(b->value); free(b);
    free(c->value); free(c);
}

void divide_show(){
    Bigint *a = (Bigint*)malloc(sizeof(Bigint)), *b = (Bigint*)malloc(sizeof(Bigint)),\
    *c = (Bigint*)malloc(sizeof(Bigint)), *d = (Bigint*)malloc(sizeof(Bigint));
    initial_Bigint(a);
    initial_Bigint(b);
    divide(a, b, c, d);
    show(a);    printf(" / ");  show(b);    printf(" = \n");  
    show(c);    printf(" * ");  show(b);    printf(" + ");  show(d);
	putchar('\n');
    free(a->value); free(a);
    free(b->value); free(b);
    free(c->value); free(c);
    free(d->value); free(d);
}

void exp_show(){
    Bigint *a = (Bigint*)malloc(sizeof(Bigint)), *b = (Bigint*)malloc(sizeof(Bigint)),\
    *c = (Bigint*)malloc(sizeof(Bigint));
    initial_Bigint(a);
    initial_Bigint(b);
	show(a);	printf(" ^ ");	show(b);
    c = qexp(a, b);
    printf(" = ");  show(c);
	putchar('\n');
    free(c->value); free(c);
}

int main(void) {
    int ch;
    printf("\nEnter the mode\n");
    printf("a. add\n");
    printf("b. min\n");
    printf("c. mul\n");
    printf("d. divide\n");
    printf("e. exp\n");
    printf("q. quit\n");
    printf("Enter the mode:");
    while( (ch = getchar()) != 'q') {
		getchar();
        switch (ch)
        {
        case 'a':
            add_show();
            break;
        
        case 'b':
            min_show();
            break;
        
        case 'c':
            mul_show();
            break;
        
        case 'd':
            divide_show();
            break;
        
        case 'e':
            exp_show();
            break;
        default:
            system("pause");
			return 0;
        }
        printf("\nEnter the mode\n");
        printf("a. add\n");
        printf("b. min\n");
        printf("c. mul\n");
        printf("d. divide\n");
        printf("e. exp\n");
        printf("q. quit\n");
        printf("Enter the mode:");
    }

    system("pause");
    return 0;
}