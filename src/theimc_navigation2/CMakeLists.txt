cmake_minimum_required(VERSION 3.8)
project(theimc_navigation2)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# =======================================================
# 1. 의존성 패키지 찾기
# =======================================================
find_package(ament_cmake REQUIRED)
find_package(nav2_bringup REQUIRED)

# [추가됨] C++ BT 플러그인을 빌드하기 위한 패키지들
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(behaviortree_cpp_v3 REQUIRED)
find_package(nav2_behavior_tree REQUIRED)

# =======================================================
# 2. 커스텀 C++ BT 플러그인 빌드
# =======================================================
# src/check_button_condition.cpp 파일을 공유 라이브러리(.so)로 빌드
add_library(check_button_condition_plugin SHARED src/check_button_condition.cpp)

# 빌드한 라이브러리에 의존성 연결
ament_target_dependencies(check_button_condition_plugin
  rclcpp
  std_msgs
  behaviortree_cpp_v3
  nav2_behavior_tree
)

# =======================================================
# 3. 설치 (Install) 설정
# =======================================================
# [추가됨] 플러그인 라이브러리를 Nav2가 찾을 수 있도록 lib 폴더에 설치
install(TARGETS check_button_condition_plugin
  DESTINATION lib
)

# [추가됨] 파이썬 스크립트를 ros2 run으로 실행할 수 있도록 설치
install(PROGRAMS scripts/button_publisher.py
  DESTINATION lib/${PROJECT_NAME}
)

# 기존 디렉토리들 + [추가됨] behavior_trees 디렉토리 설치
install(
  DIRECTORY launch maps params rviz scripts behavior_trees
  DESTINATION share/${PROJECT_NAME}
)

# =======================================================
# 4. 테스트 설정 (기존 코드 유지)
# =======================================================
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
