#include<cstdio>
#include "plane_sweep_algorithm/types.hpp"

using namespace std;

template <class T>
class SegmentHV {
  
public:
  enum class Result{Sucess,InValid};
    
  SegmentHV(const Point2<T>& a_start, const Point2<T>& a_end):
    m_start(a_start), m_end(a_end) {}
  bool isHorizontal() const {
    return (m_start.y() == m_end.y() ? true:false);
  }
  bool isVertical() const {
    return (m_start.x() == m_end.x() ? true:false);
  }
  bool operator > (const SegmentHV<T>&  lineb) const { // compare x coordinate
                                           // if ties look for y 
    if (m_start.x() > lineb.m_start.x()){
      return true;
    } else if (m_start.x() == lineb.m_start.x() && m_start.y() > lineb.m_start.y()){
      return true;
    } else {
      return false;
    }
  }

bool operator < (const SegmentHV<T>&  lineb) const { // compare x coordinate
                                           // if ties look for y 
  if (m_start.x() < lineb.start().x()){
      return true;
  } else if (m_start.x() == lineb.start().x() && m_start.y() < lineb.start().y()){
      return true;
    } else {
      return false;
    }
  }

bool isIntersecting(const SegmentHV<T>& segmentB) const {
  // vector point from start to end of segmentB
  Vector2<T> vec_segB_start_end = segmentB.end() - segmentB.start();
  Vector2<T> vec_segB_start_segA_start = m_start - segmentB.start();
  Vector2<T> vec_segB_start_segA_end = m_end - segmentB.start();

  if (vec_segB_start_end.isLeft(vec_segB_start_segA_start) &&
      vec_segB_start_end.isLeft(vec_segB_start_segA_end)) {
    return false;
  }
  if (vec_segB_start_end.isRight(vec_segB_start_segA_start) &&
      vec_segB_start_end.isRight(vec_segB_start_segA_end)) {
    return false;
  }

  Vector2<T> vec_segA_start_end = m_end() - m_start;
  Vector2<T> vec_segA_start_segB_start = segmentB.start() - m_start;
  Vector2<T> vec_segA_start_segB_end = segmentB.start() - m_end;

  if (vec_segA_start_end.isLeft(vec_segA_start_segB_start) &&
      vec_segA_start_end.isLeft(vec_segA_start_segB_end)) {
    return false;
  }
  if (vec_segA_start_end.isRight(vec_segA_start_segB_start) &&
      vec_segA_start_end.isRight(vec_segA_start_segB_end)) {
    return false;
  }
  return true;
}

Point2<T> start() const {
    return m_start;
  }
Point2<T> end() const {
    return m_end;
  }
  
private:
  Point2<T> m_start, m_end;
  
};


int main(){
  SegmentHV<float> lineA( Point2f(1,2), Point2f(3,4) );
  
}
