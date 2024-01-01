/* 1. S->TE   */
/* 2. E->+TE  */
/* 3. E->     */
/* 4. T->FH   */
/* 5. H->*FH  */
/* 6. H->     */
/* 7. F->i    */
/* 8. F->(S)  */

#include "stdio.h"
#include "conio.h"
#define MAX 20
typedef struct{
 char data[20];
 int top;
} stack;

void initstack(stack *st)
{
 st->top=0;
}

void push(stack *st,char ch)
{
 if(st->top==MAX-1) { printf("\nstack is full!"); getch();exit(0); }
 st->data[st->top]=ch;
 st->top++;
}

void pop(stack *st)
{
 if(st->top==0) { printf("\nstack is empty!"); getch();exit(0);}
  st->top--;
}

char read(stack *st)
{
  return st->data[st->top-1];
}

void error()
{
  printf("\nerror!");
  getch();
  exit(0);
}

int is_vt( char ch)
{
  int i;
  switch(ch)
  {
   case 'E':
   case 'T':
   case 'F':
   case 'S':
   case 'H':i=0; break;
   case 'i':
   case '(':
   case ')':
   case '+':
   case '*':i=1; break;
   default: printf("\ncharacter is false!");getch();exit(0);
  }
  return i;
}

int vn_to_int(char ch)
{
  int i;
  switch(ch)
  {
   case 'S':i=0;break;
   case 'E':i=1;break;
   case 'T':i=2;break;
   case 'H':i=3;break;
   case 'F':i=4;break;
   default: printf("\ncharacter is false!");getch();exit(0);
  }
  return i;
}

int vt_to_int(char ch)
{
  int i;
  switch(ch)
  {
   case 'i':i=0;break;
   case '(':i=1;break;
   case ')':i=2;break;
   case '+':i=3;break;
   case '*':i=4;break;
   case '#':i=5;break;
   default: printf("\ncharacter is false!");getch();exit(0);
  }
  return i;
}

void LL_driver(stack *input,stack *sem,int LL[5][6])
{
  int k;
  char is,ss;
  is=read(input);
  ss=read(sem);
  while( ss!='#')
  {
   if(is_vt(ss))
     {
      if(is==ss) { pop(input); pop(sem);}
       else error();
      }
    else
     {
       k=LL[vn_to_int(ss)][vt_to_int(is)];


       switch(k)
       {
        case 1: pop(sem);push(sem,'E'); push(sem,'T'); break;
        case 2: pop(sem);push(sem,'E'); push(sem,'T'); push(sem,'+');break;
        case 3: pop(sem); break;
        case 4: pop(sem);push(sem,'H'); push(sem,'F'); break;
        case 5: pop(sem);push(sem,'H'); push(sem,'F'); push(sem,'*');break;
        case 6: pop(sem); break;
        case 7: pop(sem);push(sem,'i'); break;
        case 8: pop(sem);push(sem,')'); push(sem,'S'); push(sem,'(');break;
        case -1:error();
       }
      }
   is=read(input);
   ss=read(sem);
  }
  if(is=='#'&& ss=='#') { printf("\naccept!"); getch(); }
    else error();
}

main()
{
   int LL[5][6]={1,1,-1,-1,-1,-1,-1,-1,3,2,-1,3,4,4,-1,-1,-1,-1,-1,-1,6,6,5,6,
                 7,8,7,-1,-1,-1};
  char c,ch[MAX];
  stack input,sem ;
  int i=0,j;

  initstack(&input);
  initstack(&sem);
  printf("\ninput a string:");
  scanf("%c",&c);
  while(c!='#')
   {
    ch[i]=c;
    i++;
    scanf("%c",&c);
   }

  ch[i]='#';
  for(j=i;j>=0;j--) printf("%c",ch[j]);
  for(j=i;j>=0;j--)
    push(&input,ch[j]);
  push(&sem,'#');
  push(&sem,'S');
  LL_driver(&input,&sem,LL);
}
