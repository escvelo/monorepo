#include<cstdio>
using namespace std;

template <class T>
class SegmentHV {
  
public:
  enum class Result{Sucess,InValid};
    
  SegmentHV(const T& x1, const T& y1, const T& x2, const T& y2):
    m_x1(x1), m_y1(y1), m_x2(x2), m_y2(y2) {}
  bool isHorizontal() const {
    return (m_y1 == m_y2 ? true:false);
  }
  bool isVertical() const {
    return (m_x1 == m_x2 ? true:false);
  }
  bool operator > (const SegmentHV<T>&  b){ // compare x coordinate
                                           // if ties look for y 
    if (m_x1 > b.m_x1){
      return true;
    } else if (m_x1 == b.m_x1 && m_y1 > b.m_y1){
      return true;
    } else {
      return false;
    }
  }

bool operator < (const SegmentHV<T>&  b){ // compare x coordinate
                                           // if ties look for y 
    if (m_x1 < b.m_x1){
      return true;
    } else if (m_x1 == b.m_x1 && m_y1 < b.m_y1){
      return true;
    } else {
      return false;
    }
  }

private:
  T m_x1, m_y1, m_x2, m_y2;  
  
};


int main(){
  SegmentHV<int> line_segment(1,2,3,4);
}
