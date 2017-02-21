#include <cstdio>
#include <iostream>
#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <queue>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
//#include <opencv2/stitching/detail/blenders.hpp>
//#include <io.h>

struct info{
	int t;
	double p;
	info(const int a=0,const double b=0):
	t(a),p(b){}
};
struct inpo{
	int x,y;
	inpo(const int a=0,const int b=0):
	x(a),y(b){}
};

using namespace cv;
using namespace std;

const int MOVE[4][2]={{0,1},{0,-1},{1,0},{-1,0}};

int R=38,C=100;
int row,col;
int yz=130;
int cnt[255];
int n=4;
int belone[50][50];
queue<inpo> que;
char ans[5],ans1[5],ans2[5];
Mat img[1000];
Mat res;
Mat cha[5];
Mat t1,t2;
int MODE=0;
int DEBUG=0;
string chs="1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ";

void init(){
	freopen("res.txt","r",stdin);
	int x,y;
	scanf("%d%d",&x,&y);
	t1=Mat(x,y,CV_64FC1,Scalar(1));
	for (int i = 0; i < t1.rows; i++){
		const double* ti = t1.ptr<double>(i);
		for(int j = 0; j< t1.cols; j++) {
			scanf("%lf",&ti[j]);
		}
	}
	t1=t1.t();

	scanf("%d%d",&x,&y);
	t2=Mat(x,y,CV_64FC1,Scalar(1));
	for (int i = 0; i < t2.rows; i++){
		const double* ti = t2.ptr<double>(i);
		for(int j = 0; j< t2.cols; j++) {
			scanf("%lf",&ti[j]);
		}
	}
	t2=t2.t();
	fclose(stdin);
}
string toStr(int t){
	if (!t) return "0";
	string res="";
	for (;t;t/=10) res=res+char(48+t%10);
	reverse(res.begin(), res.end());
	return res;
}
int check(int x,int y){
	int add=0;
	if (x && res.at<Vec3b>(x,y)[0]!=res.at<Vec3b>(x-1,y)[0]) ++add;
	if (x<R-1 && res.at<Vec3b>(x,y)[0]!=res.at<Vec3b>(x+1,y)[0]) ++add;
	if (y && res.at<Vec3b>(x,y)[0]!=res.at<Vec3b>(x,y-1)[0]) ++add;
	if (y<C-1 && res.at<Vec3b>(x,y)[0]!=res.at<Vec3b>(x,y+1)[0]) ++add;
	return add>=3;
}

Mat sigmoid(Mat t){
	Mat res=t.clone();
	for (int i=0;i<res.rows;i++){
		double* ti = res.ptr<double>(i);
		for (int j=0;j<res.cols;j++){
			ti[j]=1.0 / (1.0 + exp(-ti[j]));
		}
	}
	return res;
}
info predict(Mat t1,Mat t2,Mat x){
	Mat h1=sigmoid(x*t1);
	Mat tmp(1,1,CV_64FC1,Scalar(1));
	hconcat(tmp,h1,h1);
	Mat h2=sigmoid(h1*t2);

	int res;
	double max=-1;
	for (int i=0;i<h2.cols;i++){
		double save=h2.at<double>(0,i);
		if (save>max){
			max=save;
			res=i;
		}
		if (!MODE) printf("%.3f ",save);
	}
	return info(res,max);
}
int checkPos(inpo p,Mat &t){
	if (p.x<0 || p.y<0 || p.x>=t.rows || p.y>=t.cols) return 0;
	return !t.at<Vec3b>(p.x,p.y)[0] && !belone[p.x][p.y];
}
int bfs(Mat &t,int x,int y,int num){
	int res=0;
	while (!que.empty()) que.pop();
	que.push(inpo(x,y));
	while (!que.empty()){
		++res;
		inpo now=que.front();
		que.pop();
		for (int i=0;i<4;i++){
			inpo ne=inpo(now.x+MOVE[i][0],now.y+MOVE[i][1]);
			if (checkPos(ne,t)){
				belone[ne.x][ne.y]=num;
				que.push(ne);
			}
		}
	}
	return res;
}
void denoise(Mat &t){/*
	Mat st=t.clone();
	for (int i=0;i<t.rows;i++)
		for (int j=0;j<t.cols;j++)
		if (!t.at<Vec3b>(i,j)[0]){
			if ((i && st.at<Vec3b>(i-1,j)[0]) || (i<t.rows-1 && st.at<Vec3b>(i+1,j)[0]) || (j && st.at<Vec3b>(i,j-1)[0]) || (j<t.cols-1 && st.at<Vec3b>(i,j+1)[0])){
				for (int k=0;k<3;k++) t.at<Vec3b>(i,j)[k]=255;
			}
		}
	st=t.clone();
	for (int i=0;i<t.rows;i++)
		for (int j=0;j<t.cols;j++)
		if (t.at<Vec3b>(i,j)[0]){
			if ((i && !st.at<Vec3b>(i-1,j)[0]) || (i<t.rows-1 && !st.at<Vec3b>(i+1,j)[0]) || (j && !st.at<Vec3b>(i,j-1)[0]) || (j<t.cols-1 && !st.at<Vec3b>(i,j+1)[0])){
				for (int k=0;k<3;k++) t.at<Vec3b>(i,j)[k]=0;
			}
		}*/
	int num=0,max=-1,sn=0;
	memset(belone,0,sizeof(belone));
	for (int i=0;i<t.rows;i++)
		for (int j=0;j<t.cols;j++)
		if (!belone[i][j] && !t.at<Vec3b>(i,j)[0]){
			++num;
			int save=bfs(t,i,j,num);
			if (save>max){
				max=save;
				sn=num;
			}
		}
	for (int i=0;i<t.rows;i++){
		for (int j=0;j<t.cols;j++)
		if (belone[i][j]!=sn)
			for (int k=0;k<3;k++)
			t.at<Vec3b>(i,j)[k]=255;
	}
	if (max==-1){
		for (int k=0;k<3;k++)
		t.at<Vec3b>(0,0)[k]=0;
	}
}
Mat getx(Mat &res,int lastx,int add){
	++add;
	Mat res2;
	resize(res,res2,Size(add-lastx,R),0,0,CV_INTER_LINEAR);
	for (int i=0;i<R;i++)
		for (int j=lastx;j<add;j++)
			for (int k=0;k<3;k++)
				res2.at<Vec3b>(i,j-lastx)[k]=res.at<Vec3b>(i,j)[k];

	//除杂
	denoise(res2);

	//去边
	int r=R,c=add-lastx;
	int x1=-1,x2=-1,y1=-1,y2=-1;
	for (int i=0;i<r;i++)
	for (int j=0;j<c;j++)
		if (!res2.at<Vec3b>(i,j)[0]){
			if (x1==-1) x1=i;
			x2=i;
		}
	for (int j=0;j<c;j++)
		for (int i=0;i<r;i++)
		if (!res2.at<Vec3b>(i,j)[0]){
			if (y1==-1) y1=j;
			y2=j;
		}
	Mat res3;
	resize(res2,res3,Size(y2-y1+1,x2-x1+1),0,0,CV_INTER_LINEAR);
	for (int i=x1;i<=x2;i++)
		for (int j=y1;j<=y2;j++)
			for (int k=0;k<3;k++)
				res3.at<Vec3b>(i-x1,j-y1)[k]=res2.at<Vec3b>(i,j)[k];
	
	//缩放
	Mat res4;
	resize(res3,res4,Size(32,32),0,0,CV_INTER_LINEAR);
	
	Mat t3(1,1025,CV_64FC1,Scalar(1));
	for (int j=0,nt=0;j<32;j++)
		for (int k=0;k<32;k++){
			++nt;
			//if (cha[i].at<Vec3b>(k,j)[0]!=0 && cha[i].at<Vec3b>(k,j)[0]!=255) printf("WA:%d\n",cha[i].at<Vec3b>(k,j)[0]);
			t3.at<double>(0,nt)=res4.at<Vec3b>(k,j)[0]>127 ? 1 : 0;
		}

	return t3.clone();
}
void work(int t,const char* imagename,int bo){
	int nc=n;//strlen(imagename)>8 ? 5 : 4;
	//if (nc==4) return;
	C=nc*25;
	//char a[20]="";
	char a[20]="";
	if (MODE) memcpy(a,"images\\",sizeof(char)*8);
	strcat(a,imagename);
    img[t] = imread(a);
	imshow("img",img[t]);
	//裁边
	resize(img[t],res,Size(C,R),0,0,CV_INTER_LINEAR);
	for (int i=0;i<R;i++)
		for (int j=0;j<C;j++)
			for (int k=0;k<3;k++)
				res.at<Vec3b>(i,j)[k]=img[t].at<Vec3b>(10+i,(nc==4 ? 51 : 41)+j)[k];
	//imshow("img",res);
	if (DEBUG) imwrite("out1.jpg",res);

	//二值化
	for (int i=0;i<R;i++)
		for (int j=0;j<C;j++)
			for (int k=0;k<3;k++)
			if (res.at<Vec3b>(i,j)[k]>yz) res.at<Vec3b>(i,j)[k]=255;
			else res.at<Vec3b>(i,j)[k]=0;
	if (DEBUG) imwrite("out2.jpg",res);
	
	//去噪
	bo=1;
	while (bo){
		bo=0;
		for (int i=0;i<R;i++)
			for (int j=0;j<C;j++)
				if (check(i,j)){
					//bo=1;
					for (int k=0;k<3;k++) res.at<Vec3b>(i,j)[k]=res.at<Vec3b>(i,j)[k] ? 0 : 255;
				}
	}
	if (DEBUG) imwrite("out3.jpg",res);
	
	//去线
	for (int i=0;i<R-4;i++)
		for (int j=0;j<C;j++)
			if (res.at<Vec3b>(i,j)[0] && res.at<Vec3b>(i+4,j)[0] || (!i && res.at<Vec3b>(3,j)[0]))
			for (int l=0;l<4;l++)
				for (int k=0;k<3;k++) res.at<Vec3b>(i+l,j)[k]=255;
	if (DEBUG) imwrite("out4.jpg",res);

	//分割字
	for (int l=0,lastx=0;l<nc;l++){
		//printf("%d\n",l);
		int add,min=1000;
		double max=-1;
		if (l<nc-1){
			for (int i=(l+1)*25-8;i<=(l+1)*25+6;i++){/*
				int cnt=0;
				for (int j=0;j<R;j++)
				if (!res.at<Vec3b>(j,i)[0]) ++cnt;
				if (cnt<min){
					min=cnt;
					add=i+1;
				}*/
				if (l==3){
					l=3;
				}
				info save=predict(t1,t2,getx(res,lastx,i));
				if (save.p>max){
					max=save.p;
					add=i+1;
				}
			}
			//add=lastx+25;
		}else add=C;

		Mat res2;
		resize(res,res2,Size(add-lastx,R),0,0,CV_INTER_LINEAR);
		for (int i=0;i<R;i++)
			for (int j=lastx;j<add;j++)
				for (int k=0;k<3;k++)
					res2.at<Vec3b>(i,j-lastx)[k]=res.at<Vec3b>(i,j)[k];

		string name="res2-"+toStr(l)+".jpg";
		if (DEBUG) imwrite(name,res2);

		//除杂
		denoise(res2);
		name="res3-"+toStr(l)+".jpg";
		if (DEBUG) imwrite(name,res2);

		//去边
		int r=R,c=add-lastx;
		int x1=-1,x2=-1,y1=-1,y2=-1;
		for (int i=0;i<r;i++)
			for (int j=0;j<c;j++)
			if (!res2.at<Vec3b>(i,j)[0]){
				if (x1==-1) x1=i;
				x2=i;
			}
		for (int j=0;j<c;j++)
			for (int i=0;i<r;i++)
			if (!res2.at<Vec3b>(i,j)[0]){
				if (y1==-1) y1=j;
				y2=j;
			}
		Mat res3;
		resize(res2,res3,Size(y2-y1+1,x2-x1+1),0,0,CV_INTER_LINEAR);
		for (int i=x1;i<=x2;i++)
			for (int j=y1;j<=y2;j++)
				for (int k=0;k<3;k++)
					res3.at<Vec3b>(i-x1,j-y1)[k]=res2.at<Vec3b>(i,j)[k];
		char ch=imagename[l];
		printf("%c",ch);
		++cnt[ch];
		name="ans3/";
		name+=ch;
		name+="_"+toStr(cnt[ch])+".jpg";
		//std::cout<<name<<std::endl;

		//缩放
		Mat res4;
		resize(res3,res4,Size(32,32),0,0,CV_INTER_LINEAR);
		cha[l]=res4.clone();

		if (DEBUG) imwrite(name,res4);

		lastx=add;
	}
	printf("\n");
	//printf("finish");
    //waitKey();
}
/*
void makeData(){
    _finddata_t fd;
    intptr_t pf = _findfirst("images/*.jpg",&fd);
	int add=0;
    while (!_findnext(pf,&fd)){
        printf("%d\n",++add);
		work(add,fd.name,1);
    }
    _findclose(pf);
}*/

double makeAns(){
	if (!MODE && DEBUG){
		if (n==4) freopen("ans_1.txt","w",stdout);
		else freopen("ans_2.txt","w",stdout);
	}
	//imshow("cha",cha[0]);
	double acr=0;
	for (int i=0;i<n;i++){
		Mat t3(1,1025,CV_64FC1,Scalar(1));
		for (int j=0,nt=0;j<32;j++)
			for (int k=0;k<32;k++){
				++nt;
				//if (cha[i].at<Vec3b>(k,j)[0]!=0 && cha[i].at<Vec3b>(k,j)[0]!=255) printf("WA:%d\n",cha[i].at<Vec3b>(k,j)[0]);
				t3.at<double>(0,nt)=cha[i].at<Vec3b>(k,j)[0]>127 ? 1 : 0;
			}
		info save=predict(t1,t2,t3);
		if (n==4) ans1[i]=chs[save.t];
		else ans2[i]=chs[save.t];
		acr+=save.p;
		if (!MODE) printf("\n%c\n",n==4 ? ans1[i] : ans2[i]);
	}
	acr=acr/(double)n;
	for (int i=0;i<n;i++) printf("%c",n==4 ? ans1[i] : ans2[i]);
	printf("\n");
	if (!MODE && DEBUG) fclose(stdout);
	return acr;
}

void tot_work(int t,const char* imagename){
	n=4;
	work(t*2+1,imagename,0);
	double save1=makeAns();
	n=5;
	work(t*2,imagename,0);
	double save2=makeAns();

	if (!MODE) freopen("ans.txt","w",stdout);
	if (save1>save2){
		n=4;
		for (int i=0;i<n;i++){
			ans[i]=ans1[i];
			if (!MODE) printf("%c",ans[i]);
		}
	}else{
		n=5;
		for (int i=0;i<n;i++){
			ans[i]=ans2[i];
			if (!MODE) printf("%c",ans[i]);
		}
	}
	fclose(stdin);
	if (!MODE) fclose(stdout);
}
/*
int checkAns(char* name){
	for (int i=0;i<n;i++)
	if (name[i]!=ans[i]) return 0;
	return 1;
}

void test(){
    _finddata_t fd;
    intptr_t pf = _findfirst("images/*.jpg",&fd);
	int tot=0,cor=0;
    while (!_findnext(pf,&fd)){
		//if (strlen(fd.name)==4+n){
		printf("%d\n",++tot);

		tot_work(tot,fd.name);

		if (checkAns(fd.name)) ++cor;
		//}
    }
    _findclose(pf);
	freopen("accuracy.txt","w",stdout);
	printf("total: %d\n",tot);
	printf("correct: %d\n",cor);
	printf("accuracy: %.4f\n",(double)cor/(double)tot);
	fclose(stdout);
}*/

int main(){
	init();
	//if (MODE) test();
	//else tot_work(0,"test.jpg");
	tot_work(0,"test.jpg");
	printf("\nfinish\n");
	waitKey();
}
