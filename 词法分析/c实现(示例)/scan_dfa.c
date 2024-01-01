/*���ʱ��뷽ʽ*/
/*  ��ʶ��: token.class=1 */
/*  ������: token.class=2 */
/*    �Ӻ�: token.class=3 */
/*    �ֺ�: token.class=4 */
/*    ð��: token.class=5 */
/*  ��ֵ��: token.class=6 */
/*  С�ں�: token.class=7 */
/*С�ڵ��ں�: token.class=8 */
/*�ļ�������'#': token.class=9*/
#include<stdio.h>
#include<conio.h>
#include<string.h>
#include<stdlib.h>
#define MAX 100
struct a{
      int class;
      char seman[10];
} token[80];

char input[MAX];
int i,k=0;

int isletter(char x)
{
  if(x>='a'&&x<='z') return 1;
    else return 0;
}

int isDigit(char x)
{
  if(x>='0'&&x<='9') 
    return 1;
  else 
    return 0;
}
     /*�����ʶ��ĵ���*/
void print_token(int k)
{
  int i;
  printf("\n token list:");
  for(i=0;i<k;i++)
     
        printf("\n %3d token.class:%5d  token.seman:%s",i+1,token[i].class,token[i].seman );
     
}

void error(int k)
{
  printf(" \n\nscanner is false! ");
  print_token(k);
  getch();
  exit(0);
}


void next_token()
{
  char ch,name[10] ;
  int state,l;
  ch=input[i];
  while(ch==' '||ch=='\t'||ch=='\n') ch=input[++i];
  state=0;
  while(1)
   {
    switch(state)
     {
       case 0:if(isletter(ch)){ l=0;name[l++]=ch;state=1;}
               else if(isDigit(ch)) { l=0;name[l++]=ch;state=2;}
                else if(ch=='+') state=3;
                 else if(ch==';') state=4;
                  else if(ch==':') state=5;
                   else if(ch=='<') state=6;
                    else if(ch=='#') {i--;return;}
                     else  error(k);  break;
       case 1:ch=input[++i];
              if(isletter(ch)||isDigit(ch)){ name[l++]=ch; state=1;}
                else state=7; break;
       case 2:ch=input[++i];
              if(isDigit(ch)) { name[l++]=ch; state=2;}
                else state=8; break;
       case 3:token[k].class=3;strcpy(token[k].seman,"+");k++;return;
       case 4:token[k].class=4;strcpy(token[k].seman,";");k++;return;
       case 5:ch=input[++i];
              if(ch=='=') state=9; else state=10; break;
       case 6:ch=input[++i];
              if(ch=='=') state=11; else state=12; break;
       case 7:token[k].class=1;name[l]='\0';strcpy(token[k].seman,name); k++;i--; return;
       case 8:token[k].class=2;name[l]='\0';strcpy(token[k].seman,name);k++;i--;return;
       case 9:token[k].class=6;strcpy(token[k].seman,":=");k++; return;
       case 10:token[k].class=5;strcpy(token[k].seman,":");k++;i--;return;
       case 11:token[k].class=8;strcpy(token[k].seman,"<=");k++;return; 
       case 12:token[k].class=7;strcpy(token[k].seman,"<");k++;i--;return; 
       default: error(k); 
     }
   }
}

void main()
{
    int j=0;
    char ch;
       /*����Դ�����,�����ո񡢻��з����ԡ�#������*/
    printf("input source program and end of #:");

    while((ch=getchar())!='#') input[j++]=ch;
    input[j]='#';
       /*�ʷ���������*/ 
    i=0;
    while(input[i]!='#')
      {
        next_token();
        i++;
      }
    if(input[i]=='#')
       { token[k].class=9; strcpy(token[k].seman,"#");
         k++;
         printf("\n\nscanner is succend!");
         print_token(k);
       }
       
  getch();
}
