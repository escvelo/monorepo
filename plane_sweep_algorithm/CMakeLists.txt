cmake_minimum_required (VERSION 2.6)
project (planesweep)

add_executable(planesweep src/segment.cpp)
target_include_directories(planesweep PRIVATE
                            include
			    )
