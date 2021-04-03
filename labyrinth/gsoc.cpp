#include<bits/stdc++.h>

using namespace std;

typedef char (&matrix)[5][7];

//function to print the solution
matrix printSolution(matrix a){
  for (int i =0; i<5 ; i++ )
  {
    for(int j = 0 ; j<7 ; j++){
      cout << a[i][j];
    }
    cout << endl;
  }
  cout << "\n";
}



matrix recursion(matrix mz, int start,int i, int step){

  char digits[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };
  char c = '\0';

  if(start!=6){
    if(mz[i][start+1]== '.'){
      c = digits[step];
      mz[i][start+1]= c;
      printSolution(mz);
      recursion(mz,start+1, i, step+1);
    }
  }

  if(start!=0){
    if(mz[i][start-1]=='.'){
      c = digits[step];
      mz[i][start-1]= c;
      recursion(mz, start-1, i, step+1);
    }
  }

  if(i!=4){
    if(mz[i+1][start]=='.'){
      c = digits[step];
      mz[i+1][start]= c;
      recursion(mz,start, i+1, step+1);
    }
  }
  return mz;
}

matrix findLongestPath(matrix mz){

  char digits[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9' };
  char c;

  for (int start = 0; start<7 ; start++){
    if (mz[0][start]=='.'){
      mz[0][start]=digits[0];

      if(mz[1][start]=='.'){
        mz[1][start]= digits[1];
        recursion(mz, start, 1, 2);
      }
    }
  }
  return mz;
}


int main()
{
   char matrix[5][7];

  //file open
    ifstream fp("input.txt");

    // if the file doesn't exist, alert the user and end the program
    if (! fp) {
      cout << "Error, file couldn't be opened" << endl;
      return 1;
    }


    for (int i =0; i<5 ; i++ ){
      for(int j = 0 ; j<7 ; j++){
        fp >> matrix[i][j];
        if ( ! fp ) {
              // if there isn't all the characters in the given matrix,inform the user!
              cout << "Error reading file for element " << i << "," << j << endl;
              return 1;
          }
      }
    }

    //printing the question before finding the longest path
    for (int i =0; i<5 ; i++ ){
      for(int j = 0 ; j<7 ; j++){
        cout << matrix[i][j];
      }
      cout << "\n";
    }
    cout<<"\n";

    findLongestPath(matrix);

    fp.close();
    return 0;
}
