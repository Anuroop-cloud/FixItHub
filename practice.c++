#include <iostream>
using namespace std;

class parameter{
    private:
        int len;
    public:
        static int count;
        parameter(int l):len(l){
            count++;
        }

        int value(){
            return len*len;
        }
};

int parameter::count = 0;

int main(){
    parameter p1(10);
    parameter p2(20);
    cout<<p1.value()<<endl;
    cout<<parameter::count<<endl;
}
