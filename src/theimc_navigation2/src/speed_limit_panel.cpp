#include "theimc_navigation2/speed_limit_panel.hpp"

#include <cmath>

#include <QDoubleSpinBox>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QSlider>
#include <QVBoxLayout>

#include <pluginlib/class_list_macros.hpp>
#include <rviz_common/display_context.hpp>
#include <rviz_common/ros_integration/ros_node_abstraction_iface.hpp>

namespace theimc_navigation2
{

SpeedLimitPanel::SpeedLimitPanel(QWidget * parent)
: rviz_common::Panel(parent)
{
  auto * main_layout = new QVBoxLayout(this);
  main_layout->addWidget(new QLabel("Nav2 maximum linear speed", this));

  speed_slider_ = new QSlider(Qt::Horizontal, this);
  speed_slider_->setRange(
    static_cast<int>(kMinSpeed * kSliderScale),
    static_cast<int>(kMaxSpeed * kSliderScale));
  speed_slider_->setSingleStep(5);
  speed_slider_->setPageStep(25);
  speed_slider_->setValue(static_cast<int>(current_speed_ * kSliderScale));
  main_layout->addWidget(speed_slider_);

  auto * input_layout = new QHBoxLayout();
  speed_spin_box_ = new QDoubleSpinBox(this);
  speed_spin_box_->setRange(kMinSpeed, kMaxSpeed);
  speed_spin_box_->setDecimals(3);
  speed_spin_box_->setSingleStep(0.01);
  speed_spin_box_->setSuffix(" m/s");
  speed_spin_box_->setValue(current_speed_);
  input_layout->addWidget(speed_spin_box_);

  clear_button_ = new QPushButton("Remove limit", this);
  input_layout->addWidget(clear_button_);
  main_layout->addLayout(input_layout);

  status_label_ = new QLabel("Waiting for RViz initialization", this);
  status_label_->setWordWrap(true);
  main_layout->addWidget(status_label_);
  main_layout->addStretch();

  connect(speed_slider_, &QSlider::valueChanged, this, [this](int value) {
    setSpeedFromSlider(value);
  });
  connect(
    speed_spin_box_, qOverload<double>(&QDoubleSpinBox::valueChanged), this,
    [this](double value) {setSpeedFromSpinBox(value);});
  connect(clear_button_, &QPushButton::clicked, this, [this]() {clearSpeedLimit();});
}

void SpeedLimitPanel::onInitialize()
{
  auto node_abstraction = getDisplayContext()->getRosNodeAbstraction().lock();
  if (!node_abstraction) {
    status_label_->setText("ROS node is unavailable");
    return;
  }

  node_ = node_abstraction->get_raw_node();
  publisher_ = node_->create_publisher<nav2_msgs::msg::SpeedLimit>(topic_, rclcpp::QoS(10));
  updateStatus(current_speed_, false);
}

void SpeedLimitPanel::setSpeedFromSlider(int slider_value)
{
  if (updating_widgets_) {
    return;
  }
  const double speed = static_cast<double>(slider_value) / kSliderScale;
  updating_widgets_ = true;
  speed_spin_box_->setValue(speed);
  updating_widgets_ = false;
  publishSpeedLimit(speed);
}

void SpeedLimitPanel::setSpeedFromSpinBox(double speed)
{
  if (updating_widgets_) {
    return;
  }
  updating_widgets_ = true;
  speed_slider_->setValue(static_cast<int>(std::round(speed * kSliderScale)));
  updating_widgets_ = false;
  publishSpeedLimit(speed);
}

void SpeedLimitPanel::publishSpeedLimit(double speed)
{
  current_speed_ = speed;
  if (!publisher_) {
    status_label_->setText("Publisher is not initialized");
    return;
  }

  nav2_msgs::msg::SpeedLimit message;
  message.percentage = false;
  message.speed_limit = speed;
  publisher_->publish(message);
  updateStatus(speed, false);
}

void SpeedLimitPanel::clearSpeedLimit()
{
  if (!publisher_) {
    status_label_->setText("Publisher is not initialized");
    return;
  }

  nav2_msgs::msg::SpeedLimit message;
  message.percentage = false;
  message.speed_limit = 0.0;
  publisher_->publish(message);
  updateStatus(0.0, true);
}

void SpeedLimitPanel::updateStatus(double speed, bool unlimited)
{
  if (unlimited) {
    status_label_->setText("Limit removed (MPPI vx_max still applies)");
  } else {
    status_label_->setText(
      QString("Published %1 m/s to %2")
      .arg(speed, 0, 'f', 3)
      .arg(QString::fromStdString(topic_)));
  }
}

void SpeedLimitPanel::load(const rviz_common::Config & config)
{
  rviz_common::Panel::load(config);
  float saved_speed = static_cast<float>(current_speed_);
  if (config.mapGetFloat("Speed", &saved_speed)) {
    saved_speed = std::max(
      static_cast<float>(kMinSpeed),
      std::min(static_cast<float>(kMaxSpeed), saved_speed));
    current_speed_ = saved_speed;
    updating_widgets_ = true;
    speed_spin_box_->setValue(current_speed_);
    speed_slider_->setValue(static_cast<int>(std::round(current_speed_ * kSliderScale)));
    updating_widgets_ = false;
  }
}

void SpeedLimitPanel::save(rviz_common::Config config) const
{
  rviz_common::Panel::save(config);
  config.mapSetValue("Speed", current_speed_);
}

}  // namespace theimc_navigation2

PLUGINLIB_EXPORT_CLASS(theimc_navigation2::SpeedLimitPanel, rviz_common::Panel)
