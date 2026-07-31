#ifndef THEIMC_NAVIGATION2__SPEED_LIMIT_PANEL_HPP_
#define THEIMC_NAVIGATION2__SPEED_LIMIT_PANEL_HPP_

#include <memory>
#include <string>

#include <nav2_msgs/msg/speed_limit.hpp>
#include <rclcpp/rclcpp.hpp>
#include <rviz_common/panel.hpp>

class QDoubleSpinBox;
class QLabel;
class QPushButton;
class QSlider;

namespace theimc_navigation2
{

class SpeedLimitPanel : public rviz_common::Panel
{
public:
  explicit SpeedLimitPanel(QWidget * parent = nullptr);

  void onInitialize() override;
  void load(const rviz_common::Config & config) override;
  void save(rviz_common::Config config) const override;

private:
  void setSpeedFromSlider(int slider_value);
  void setSpeedFromSpinBox(double speed);
  void publishSpeedLimit(double speed);
  void clearSpeedLimit();
  void updateStatus(double speed, bool unlimited);

  static constexpr double kMinSpeed = 0.01;
  static constexpr double kMaxSpeed = 0.25;
  static constexpr int kSliderScale = 1000;

  QSlider * speed_slider_;
  QDoubleSpinBox * speed_spin_box_;
  QPushButton * clear_button_;
  QLabel * status_label_;

  rclcpp::Node::SharedPtr node_;
  rclcpp::Publisher<nav2_msgs::msg::SpeedLimit>::SharedPtr publisher_;
  std::string topic_{"/speed_limit"};
  double current_speed_{kMaxSpeed};
  bool updating_widgets_{false};
};

}  // namespace theimc_navigation2

#endif  // THEIMC_NAVIGATION2__SPEED_LIMIT_PANEL_HPP_
