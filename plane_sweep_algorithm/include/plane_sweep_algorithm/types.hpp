



template <typename T> int sgn(T val) {
    return (T(0) < val) - (val < T(0));
}

template<typename T>
class Vector2 {
public:
  /// Default init to zeros
  Vector2() : m_x(T(0)), m_y(T(0)){}
  /// Init with same value
  Vector2(T xx) : m_x(xx), m_y(xx){}
  /// Init with 2 different values
  Vector2(T xx , T yy): m_x(xx), m_y(yy){}

  /// returns true if Vector B lies left of Vector A
  bool isLeft(const Vector2<T>& vector_B){
    if (sgn(cross_product(vector_B)) > 0){
      return true;
    }else {
      return false;
    }
  }    
  /// returns true if Vector B lies left of Vector A
  bool isRight(const Vector2<T>& vector_B){
    if (sgn(cross_product(vector_B)) < 0){
      return true;
    }else {
      return false;
    }
  }    

  float cross_product(const Vector2<T>& vector_B){
    return m_x * vector_B.y() - m_y * vector_B.x();
  }

  /// Getters for x and y coordinate values
  T x(){return m_x;}
  T y(){return m_y;}
 private:
     T m_x, m_y;
};


template<typename T>
class Point2 {
public:
  /// Default init to zeros
  Point2() : m_x(T(0)), m_y(T(0)){}
  /// Init with same value
  Point2(T xx) : m_x(xx), m_y(xx){}
  /// Init with 2 different values
  Point2(T xx , T yy): m_x(xx), m_y(yy){}

  /// when two points A and B are substracted, result is a vector with
  /// its head at A and tail at B.
  Vector2<T> operator - (const Point2<T>& a_pointB){
    return Vector2<T>(m_x - a_pointB.x(), m_y - a_pointB.y());
  }
  /// Getters for x and y coordinate values
  T x(){return m_x;}
  T y(){return m_y;}
 private:
     T m_x, m_y;
};


typedef Vector2<float> Vec2f;
typedef Point2<float> Point2f;
